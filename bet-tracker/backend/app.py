"""Bet Tracker API + live tracker (AWS Lambda, Python 3.13).

Routes (all require a Cognito ID token; the user id comes from the verified JWT):
  GET    /slips              list your slips
  POST   /slips              save a slip
  PUT    /slips/{id}         update a slip (edit legs, mark results)
  DELETE /slips/{id}         delete a slip
  POST   /parse              read a bet slip screenshot with Amazon Bedrock
  POST   /refresh            re-check your open slips against live ESPN data now
  GET    /settings           daily goal etc.
  PUT    /settings
The scheduled handler `tracker_handler` re-checks every open slip every few minutes.
"""
import base64
import datetime as dt
import json
import os
import re
import uuid

import boto3
from boto3.dynamodb.conditions import Key

import espn
import slips as slipmath

TABLE = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
S3 = boto3.client("s3")
BUCKET = os.environ["UPLOAD_BUCKET"]
BEDROCK = boto3.client("bedrock-runtime")
MODEL_IDS = [m for m in (os.environ.get("MODEL_ID"), os.environ.get("FALLBACK_MODEL_ID")) if m]

MAX_SLIPS = 2000
SPORTS = ["nba", "wnba", "ncaab", "nfl", "ncaaf", "soccer", "tennis", "other"]
TYPES = ["moneyline", "spread", "total", "team_total", "player_prop"]


# ---------------------------------------------------------------- helpers

def resp(code, body):
    return {"statusCode": code, "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body, default=str)}


def now_iso():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def user_id(event):
    claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
    return claims["sub"]


def body_of(event):
    raw = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode()
    return json.loads(raw)


def pk(uid):
    return f"USER#{uid}"


def to_item(uid, slip):
    item = {"pk": pk(uid), "sk": f"SLIP#{slip['slipId']}", "data": json.dumps(slip),
            "createdAt": slip["createdAt"]}
    if slip.get("status", "open") == "open":
        item["active"] = "1"   # sparse index: only open slips are scanned by the tracker
    return item


def load_slips(uid):
    items, kw = [], {"KeyConditionExpression": Key("pk").eq(pk(uid)) & Key("sk").begins_with("SLIP#")}
    while True:
        r = TABLE.query(**kw)
        items += r["Items"]
        if "LastEvaluatedKey" not in r or len(items) >= MAX_SLIPS:
            break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    return [json.loads(i["data"]) for i in items]


def clean_leg(l):
    out = {
        "id": str(l.get("id") or uuid.uuid4().hex[:8]),
        "sport": l.get("sport") if l.get("sport") in SPORTS else "other",
        "type": l.get("type") if l.get("type") in TYPES else "moneyline",
        "selection": str(l.get("selection") or "")[:200],
        "team": str(l.get("team") or "")[:80], "opponent": str(l.get("opponent") or "")[:80],
        "player": str(l.get("player") or "")[:80], "stat": str(l.get("stat") or "")[:40],
        "side": "under" if l.get("side") == "under" else "over",
        "league": str(l.get("league") or "")[:40],
        "gameDate": str(l.get("gameDate") or "")[:10],
        "odds": str(l.get("odds") or "")[:12],
    }
    try:
        out["line"] = float(l["line"]) if l.get("line") not in (None, "") else None
    except (TypeError, ValueError):
        out["line"] = None
    if l.get("manualResult") in ("won", "lost", "push", "void"):
        out["manualResult"] = l["manualResult"]
    # keep tracker state if the leg itself didn't change
    for k in ("live", "match"):
        if isinstance(l.get(k), dict):
            out[k] = l[k]
    return out


def clean_slip(s, existing=None):
    base = existing or {"slipId": uuid.uuid4().hex[:12], "createdAt": now_iso(), "status": "open"}
    slip = dict(base)
    for k in ("book", "notes", "odds"):
        if k in s:
            slip[k] = str(s.get(k) or "")[:300]
    for k in ("stake", "payout"):
        if k in s:
            slip[k] = slipmath.money(s.get(k))
    if "placedAt" in s:
        slip["placedAt"] = str(s.get("placedAt") or "")[:25]
    if "screenshotKey" in s and str(s["screenshotKey"]).startswith("uploads/"):
        slip["screenshotKey"] = s["screenshotKey"]
    if "legs" in s:
        old = {l.get("id"): l for l in (existing or {}).get("legs", [])}
        legs = []
        for raw in (s.get("legs") or [])[:25]:
            leg = clean_leg(raw)
            prev = old.get(leg["id"])
            core = ("sport", "type", "team", "opponent", "player", "stat", "side", "line", "league", "gameDate")
            if prev is None or any(str(prev.get(k)) != str(leg.get(k)) for k in core):
                leg.pop("live", None)   # the bet changed, so look the game up again
                leg.pop("match", None)
            legs.append(leg)
        slip["legs"] = legs
    if s.get("manualStatus") in ("won", "lost", "push", "void", None, ""):
        if s.get("manualStatus"):
            slip["manualStatus"] = s["manualStatus"]
        elif "manualStatus" in s:
            slip.pop("manualStatus", None)
    slip.setdefault("legs", [])
    slip.setdefault("placedAt", slip["createdAt"])
    slip["updatedAt"] = now_iso()
    slipmath.settle(slip)
    slipmath.summarize_live(slip)
    return slip


def track(slip_list, fetcher):
    """Re-checks every open slip; returns the slips that changed."""
    changed = []
    for slip in slip_list:
        if slip.get("status", "open") != "open":
            continue
        for leg in slip.get("legs", []):
            espn.evaluate_leg(fetcher, leg)
        slipmath.settle(slip)
        slipmath.summarize_live(slip)
        slip["checkedAt"] = now_iso()
        changed.append(slip)
    return changed


# ---------------------------------------------------------------- screenshot parsing

SLIP_TOOL = {
    "toolSpec": {
        "name": "record_slip",
        "description": "Record every bet on the sportsbook slip screenshot.",
        "inputSchema": {"json": {
            "type": "object",
            "properties": {
                "book": {"type": "string", "description": "Sportsbook name if visible (FanDuel, DraftKings, PrizePicks...)"},
                "stake": {"type": "number", "description": "Amount wagered in dollars"},
                "payout": {"type": "number", "description": "TOTAL return if it wins (stake + profit). If only 'to win' is shown, add the stake."},
                "odds": {"type": "string", "description": "Overall slip odds in American format, e.g. +450"},
                "placedAt": {"type": "string", "description": "Date placed, YYYY-MM-DD, if shown"},
                "legs": {"type": "array", "items": {
                    "type": "object",
                    "properties": {
                        "selection": {"type": "string", "description": "The leg exactly as written on the slip"},
                        "sport": {"type": "string", "enum": SPORTS},
                        "league": {"type": "string", "description": "For soccer, ESPN league code if known: eng.1 (Premier League), esp.1 (LaLiga), ita.1 (Serie A), ger.1 (Bundesliga), fra.1 (Ligue 1), usa.1 (MLS), uefa.champions, uefa.europa, mex.1. Else empty."},
                        "type": {"type": "string", "enum": TYPES, "description": "moneyline = win the game/match (or Draw); spread = handicap; total = game over/under; team_total = one team's points over/under; player_prop = a player's stat"},
                        "team": {"type": "string", "description": "Team or tennis player the bet is ON (for player props, the player's team if shown). Use 'Draw' for a soccer draw."},
                        "opponent": {"type": "string", "description": "The other team/player in that game, if shown"},
                        "player": {"type": "string", "description": "Player full name for player props"},
                        "stat": {"type": "string", "description": "For player props, one of: points, rebounds, assists, threes, steals, blocks, turnovers, pra, pr, pa, ra, stocks, passing_yards, passing_tds, completions, pass_attempts, interceptions, rushing_yards, rushing_attempts, receiving_yards, receptions, rush_rec_yards, touchdowns (anytime TD = touchdowns over 0.5), goals, shots, shots_on_target, soccer_assists, saves"},
                        "side": {"type": "string", "enum": ["over", "under"]},
                        "line": {"type": "number", "description": "Spread/total/prop line, e.g. -3.5 or 24.5. Anytime TD/goal scorer = 0.5"},
                        "odds": {"type": "string", "description": "This leg's American odds if shown"},
                        "gameDate": {"type": "string", "description": "Game date YYYY-MM-DD if shown or inferable"},
                    },
                    "required": ["selection", "sport", "type"],
                }},
            },
            "required": ["legs"],
        }},
    }
}


def parse_screenshot(uid, data_url):
    m = re.match(r"data:image/(png|jpeg|jpg|webp|gif);base64,(.+)", data_url or "", re.S)
    if not m:
        return resp(400, {"error": "Please upload a PNG, JPG, WEBP or GIF image."})
    fmt = "jpeg" if m.group(1) == "jpg" else m.group(1)
    img = base64.b64decode(m.group(2))
    if len(img) > 3_500_000:
        return resp(400, {"error": "Image too large (max 3.5 MB)."})
    key = f"uploads/{uid}/{uuid.uuid4().hex}.{fmt}"
    S3.put_object(Bucket=BUCKET, Key=key, Body=img, ContentType=f"image/{fmt}")
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    prompt = (f"Today is {today}. This is a screenshot of a sports betting slip. Read it carefully "
              "and call record_slip with every leg. Use full team names when you can tell them. "
              "If a value isn't visible, leave it out rather than guessing.")
    last_err = None
    for model in MODEL_IDS:
        try:
            r = BEDROCK.converse(
                modelId=model,
                messages=[{"role": "user", "content": [
                    {"image": {"format": fmt, "source": {"bytes": img}}}, {"text": prompt}]}],
                toolConfig={"tools": [SLIP_TOOL], "toolChoice": {"tool": {"name": "record_slip"}}},
                inferenceConfig={"maxTokens": 2000, "temperature": 0},
            )
            for block in r["output"]["message"]["content"]:
                if "toolUse" in block:
                    draft = block["toolUse"]["input"]
                    draft["screenshotKey"] = key
                    draft["legs"] = [clean_leg(l) for l in draft.get("legs", [])]
                    return resp(200, {"draft": draft, "model": model})
            last_err = "The AI didn't return any bets."
        except Exception as e:
            print(f"Bedrock {model} failed: {e!r}")
            last_err = str(e)
    return resp(502, {"error": "Couldn't read the slip automatically. You can type it in instead.",
                      "detail": (last_err or "")[:300], "screenshotKey": key})


# ---------------------------------------------------------------- handlers

def handler(event, context):
    route = event.get("routeKey", "")
    uid = user_id(event)
    try:
        if route == "GET /slips":
            data = load_slips(uid)
            for s in data:
                if s.get("screenshotKey"):
                    s["screenshotUrl"] = S3.generate_presigned_url(
                        "get_object", Params={"Bucket": BUCKET, "Key": s["screenshotKey"]}, ExpiresIn=3600)
            data.sort(key=lambda s: s.get("placedAt") or s.get("createdAt"), reverse=True)
            return resp(200, {"slips": data})

        if route == "POST /slips":
            slip = clean_slip(body_of(event))
            if slip["status"] == "open" and slip["legs"]:
                track([slip], espn.Fetcher())   # first live check right away
            TABLE.put_item(Item=to_item(uid, slip))
            return resp(201, {"slip": slip})

        if route in ("PUT /slips/{id}", "DELETE /slips/{id}"):
            sid = event["pathParameters"]["id"]
            key = {"pk": pk(uid), "sk": f"SLIP#{sid}"}
            cur = TABLE.get_item(Key=key).get("Item")
            if not cur:
                return resp(404, {"error": "Slip not found"})
            if route.startswith("DELETE"):
                TABLE.delete_item(Key=key)
                return resp(200, {"deleted": sid})
            slip = clean_slip(body_of(event), json.loads(cur["data"]))
            if slip["status"] == "open":
                track([slip], espn.Fetcher())
            TABLE.put_item(Item=to_item(uid, slip))
            return resp(200, {"slip": slip})

        if route == "POST /parse":
            return parse_screenshot(uid, body_of(event).get("image"))

        if route == "POST /refresh":
            open_slips = [s for s in load_slips(uid) if s.get("status", "open") == "open"]
            changed = track(open_slips, espn.Fetcher())
            for s in changed:
                TABLE.put_item(Item=to_item(uid, s))
            return resp(200, {"checked": len(changed)})

        if route == "GET /settings":
            item = TABLE.get_item(Key={"pk": pk(uid), "sk": "SETTINGS"}).get("Item")
            return resp(200, json.loads(item["data"]) if item else {"dailyGoal": 60})

        if route == "PUT /settings":
            b = body_of(event)
            settings = {"dailyGoal": slipmath.money(b.get("dailyGoal", 60)),
                        "startingBankroll": slipmath.money(b.get("startingBankroll", 0))}
            TABLE.put_item(Item={"pk": pk(uid), "sk": "SETTINGS", "data": json.dumps(settings)})
            return resp(200, settings)

        return resp(404, {"error": f"Unknown route {route}"})
    except json.JSONDecodeError:
        return resp(400, {"error": "Request body must be JSON"})


def tracker_handler(event, context):
    """Runs on a schedule: re-checks every open slip for every user."""
    fetcher = espn.Fetcher()
    items, kw = [], {"IndexName": "ActiveIndex", "KeyConditionExpression": Key("active").eq("1")}
    while True:
        r = TABLE.query(**kw)
        items += r["Items"]
        if "LastEvaluatedKey" not in r:
            break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    updated = 0
    for it in items:
        uid = it["pk"].split("#", 1)[1]
        full = TABLE.get_item(Key={"pk": it["pk"], "sk": it["sk"]}).get("Item")
        if not full:
            continue
        slip = json.loads(full["data"])
        if track([slip], fetcher):
            TABLE.put_item(Item=to_item(uid, slip))
            updated += 1
    print(json.dumps({"openSlips": len(items), "updated": updated, "espnCalls": len(fetcher.cache)}))
    return {"updated": updated}
