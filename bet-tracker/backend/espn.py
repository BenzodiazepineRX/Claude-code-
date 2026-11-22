"""Live game data from ESPN's public (unofficial) site API.

ESPN does not document or guarantee these feeds, so every lookup here is
defensive: anything unexpected returns None instead of raising.
"""
import datetime as dt
import gzip
import json
import re
import unicodedata
import urllib.request

BASE = "https://site.api.espn.com/apis/site/v2/sports"

# sport key -> list of ESPN "sport/league" paths to search
SPORT_PATHS = {
    "nba": ["basketball/nba"],
    "wnba": ["basketball/wnba"],
    "ncaab": ["basketball/mens-college-basketball"],
    "nfl": ["football/nfl"],
    "ncaaf": ["football/college-football"],
    "tennis": ["tennis/atp", "tennis/wta"],
    "soccer": [
        "soccer/eng.1", "soccer/esp.1", "soccer/ita.1", "soccer/ger.1", "soccer/fra.1",
        "soccer/usa.1", "soccer/uefa.champions", "soccer/uefa.europa", "soccer/uefa.europa.conf",
        "soccer/mex.1", "soccer/ned.1", "soccer/por.1", "soccer/eng.2", "soccer/sco.1",
        "soccer/bra.1", "soccer/arg.1", "soccer/tur.1", "soccer/eng.fa",
        "soccer/eng.league_cup", "soccer/fifa.world", "soccer/uefa.nations",
        "soccer/conmebol.libertadores",
    ],
}

# Canonical player-prop stats. Each maps to a list of (box score key) parts that are summed.
STAT_PARTS = {
    # basketball
    "points": ["points"], "rebounds": ["rebounds"], "assists": ["assists"],
    "threes": ["threePointFieldGoalsMade"], "steals": ["steals"], "blocks": ["blocks"],
    "turnovers": ["turnovers"],
    "pra": ["points", "rebounds", "assists"], "pr": ["points", "rebounds"],
    "pa": ["points", "assists"], "ra": ["rebounds", "assists"], "stocks": ["steals", "blocks"],
    # american football
    "passing_yards": ["passingYards"], "passing_tds": ["passingTouchdowns"],
    "completions": ["completions"], "pass_attempts": ["passingAttempts"],
    "interceptions": ["interceptions"],
    "rushing_yards": ["rushingYards"], "rushing_attempts": ["rushingAttempts"],
    "receiving_yards": ["receivingYards"], "receptions": ["receptions"],
    "rush_rec_yards": ["rushingYards", "receivingYards"],
    "touchdowns": ["rushingTouchdowns", "receivingTouchdowns"],
    # soccer
    "goals": ["totalGoals"], "shots": ["totalShots"], "shots_on_target": ["shotsOnTarget"],
    "soccer_assists": ["goalAssists"], "saves": ["saves"],
}
STAT_LABEL = {
    "points": "PTS", "rebounds": "REB", "assists": "AST", "threes": "3PM", "steals": "STL",
    "blocks": "BLK", "turnovers": "TO", "pra": "PRA", "pr": "P+R", "pa": "P+A", "ra": "R+A",
    "stocks": "STL+BLK", "passing_yards": "pass yds", "passing_tds": "pass TD",
    "completions": "comp", "pass_attempts": "pass att", "interceptions": "INT",
    "rushing_yards": "rush yds", "rushing_attempts": "carries", "receiving_yards": "rec yds",
    "receptions": "rec", "rush_rec_yards": "rush+rec yds", "touchdowns": "TD",
    "goals": "goals", "shots": "shots", "shots_on_target": "SOT", "soccer_assists": "assists",
    "saves": "saves",
}


class Fetcher:
    """Fetches ESPN JSON with a per-run cache so each URL is requested once."""

    def __init__(self):
        self.cache = {}

    def get(self, path, query=""):
        url = f"{BASE}/{path}{query}"
        if url in self.cache:
            return self.cache[url]
        data = None
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "bet-tracker/1.0", "Accept": "application/json",
                "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=8) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
                    raw = gzip.decompress(raw)
                data = json.loads(raw)
        except Exception as e:  # network/JSON errors: treat as "no data this round"
            print(f"ESPN fetch failed {url}: {e}")
        self.cache[url] = data
        return data

    def scoreboard(self, path, day):
        return self.get(f"{path}/scoreboard", f"?dates={day:%Y%m%d}&limit=300")

    def summary(self, path, event_id):
        return self.get(f"{path}/summary", f"?event={event_id}")


# ---------------------------------------------------------------- name matching

def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def team_names(team):
    """All the ways a team might be written on a slip."""
    if not team:
        return []
    out = {team.get("displayName"), team.get("shortDisplayName"), team.get("name"),
           team.get("abbreviation"), team.get("nickname"),
           f"{team.get('location', '')} {team.get('name', '')}"}
    return [norm(x) for x in out if x and norm(x)]


def team_matches(wanted, team):
    w = norm(wanted)
    if not w:
        return False
    names = team_names(team)
    if w in names:
        return True
    nick = norm(team.get("name") or team.get("shortDisplayName"))
    # "LA Lakers" contains "lakers"; "Man City" etc. handled by shortDisplayName above
    if nick and len(nick) > 3 and re.search(rf"\b{re.escape(nick)}\b", w):
        return True
    disp = norm(team.get("displayName"))
    return len(w) > 4 and w in disp


SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def person_tokens(name):
    return [t for t in norm(name).split() if t not in SUFFIXES]


def person_matches(wanted, actual):
    a, b = person_tokens(wanted), person_tokens(actual)
    if not a or not b:
        return False
    if a == b:
        return True
    # same last name and same first initial ("L. James" vs "LeBron James")
    if a[-1] == b[-1] and a[0][0] == b[0][0]:
        return True
    # single-name players (e.g. soccer) or "James" alone
    return len(a) == 1 and a[0] == b[-1]


# ---------------------------------------------------------------- competitions

def iter_competitions(board):
    """Yields every competition in a scoreboard (tennis nests them in groupings)."""
    for ev in (board or {}).get("events", []) or []:
        comps = list(ev.get("competitions") or [])
        for g in ev.get("groupings") or []:
            comps.extend(g.get("competitions") or [])
        for c in comps:
            yield ev, c


def competitor_label(comp):
    if comp.get("team"):
        return comp["team"].get("shortDisplayName") or comp["team"].get("displayName")
    if comp.get("athlete"):
        return comp["athlete"].get("shortName") or comp["athlete"].get("displayName")
    if comp.get("roster"):
        return comp["roster"].get("shortDisplayName") or comp["roster"].get("displayName")
    return "?"


def competitor_matches(wanted, comp):
    if comp.get("team"):
        return team_matches(wanted, comp["team"])
    if comp.get("athlete"):
        return person_matches(wanted, comp["athlete"].get("displayName"))
    if comp.get("roster"):  # doubles: match either player or the pair name
        r = comp["roster"]
        if norm(wanted) == norm(r.get("displayName")):
            return True
        return any(person_matches(wanted, a.get("displayName")) for a in r.get("athletes", []))
    return False


def candidate_days(game_date):
    try:
        d = dt.date.fromisoformat(str(game_date)[:10])
    except ValueError:
        d = dt.datetime.now(dt.timezone.utc).date()
    return [d, d - dt.timedelta(days=1), d + dt.timedelta(days=1)]


def find_competition(f, leg):
    """Returns (path, event, competition) for the leg's game, or None."""
    m = leg.get("match") or {}
    if m.get("path") and m.get("compId") and m.get("day"):
        board = f.scoreboard(m["path"], dt.date.fromisoformat(m["day"]))
        for ev, c in iter_competitions(board):
            if str(c.get("id")) == str(m["compId"]):
                return m["path"], ev, c
    sport = (leg.get("sport") or "").lower()
    paths = list(SPORT_PATHS.get(sport, []))
    if leg.get("league"):
        lp = leg["league"] if "/" in leg["league"] else f"{(paths[0].split('/')[0] if paths else 'soccer')}/{leg['league']}"
        paths = [lp] + [p for p in paths if p != lp]
    names = [x for x in (leg.get("team"), leg.get("opponent")) if x and norm(x) not in ("draw", "tie")]
    if not names or not paths:
        return None
    for day in candidate_days(leg.get("gameDate")):
        for path in paths:
            board = f.scoreboard(path, day)
            for ev, c in iter_competitions(board):
                comps = c.get("competitors") or []
                hit = [any(competitor_matches(n, x) for x in comps) for n in names]
                if all(hit):
                    leg["match"] = {"path": path, "compId": str(c.get("id")),
                                    "eventId": str(ev.get("id")), "day": day.isoformat()}
                    return path, ev, c
    return None


def find_player_game(f, leg):
    """For a player prop with no team on the slip: scan that day's games' box scores."""
    sport = (leg.get("sport") or "").lower()
    for day in candidate_days(leg.get("gameDate"))[:2]:
        for path in SPORT_PATHS.get(sport, [])[:3]:
            board = f.scoreboard(path, day)
            checked = 0
            for ev, c in iter_competitions(board):
                if c.get("status", {}).get("type", {}).get("state") == "pre":
                    continue
                checked += 1
                if checked > 16:
                    break
                summ = f.summary(path, ev.get("id"))
                if player_stat(summ, leg.get("player"), None) is not None:
                    leg["match"] = {"path": path, "compId": str(c.get("id")),
                                    "eventId": str(ev.get("id")), "day": day.isoformat()}
                    return path, ev, c
    return None


# ---------------------------------------------------------------- box scores

def _num(v):
    try:
        return float(str(v).split("-")[0].split("/")[0])
    except (ValueError, TypeError):
        return 0.0


def player_stats(summary, player):
    """Returns {statKey: value} for a player from an ESPN summary, or None if not found."""
    if not summary:
        return None
    found, stats = False, {}
    for team in (summary.get("boxscore") or {}).get("players") or []:
        for group in team.get("statistics") or []:
            keys = group.get("keys") or []
            for a in group.get("athletes") or []:
                if not person_matches(player, (a.get("athlete") or {}).get("displayName")):
                    continue
                found = True
                for k, v in zip(keys, a.get("stats") or []):
                    # split "made-attempted" / "comp/att" style keys into both parts
                    parts = re.split(r"[-/]", k)
                    vals = re.split(r"[-/]", str(v))
                    if len(parts) == 2 and len(vals) == 2:
                        stats.setdefault(parts[0], _num(vals[0]))
                        stats.setdefault(parts[1], _num(vals[1]))
                    else:
                        stats.setdefault(k, _num(v))
    for team in summary.get("rosters") or []:  # soccer
        for p in team.get("roster") or []:
            if person_matches(player, (p.get("athlete") or {}).get("displayName")):
                found = True
                for s in p.get("stats") or []:
                    stats.setdefault(s.get("name"), _num(s.get("value")))
    return stats if found else None


def player_stat(summary, player, stat):
    stats = player_stats(summary, player)
    if stats is None:
        return None
    if stat is None:
        return 0.0
    parts = STAT_PARTS.get(stat)
    if not parts:
        return None
    return sum(stats.get(p, 0.0) for p in parts)


# ---------------------------------------------------------------- evaluation

def game_state(comp):
    t = (comp.get("status") or {}).get("type") or {}
    return t.get("state") or "pre", t.get("shortDetail") or t.get("detail") or ""


def score_of(c):
    s = c.get("score")
    if isinstance(s, dict):
        s = s.get("value") or s.get("displayValue")
    return _num(s) if s not in (None, "") else 0.0


def tennis_sets(comp):
    """Returns (sets won A, sets won B, games A, games B, set score text)."""
    a, b = comp["competitors"][0], comp["competitors"][1]
    la, lb = a.get("linescores") or [], b.get("linescores") or []
    sa = sb = ga = gb = 0
    txt = []
    for x, y in zip(la, lb):
        vx, vy = _num(x.get("value")), _num(y.get("value"))
        ga += vx
        gb += vy
        txt.append(f"{int(vx)}-{int(vy)}")
        if x.get("winner"):
            sa += 1
        elif y.get("winner"):
            sb += 1
    return sa, sb, ga, gb, " ".join(txt)


def over_under(value, line, side, final):
    """Stats and scores only go up, so overs can be won early and unders lost early."""
    if side == "under":
        if value > line:
            return "lost"
        if final:
            return "push" if value == line else "won"
        return "winning"
    if value > line:
        return "won"
    if final:
        return "push" if value == line else "lost"
    return "live"


def margin_result(margin, final):
    if final:
        return "won" if margin > 0 else ("push" if margin == 0 else "lost")
    return "winning" if margin > 0 else ("tied" if margin == 0 else "losing")


def evaluate_leg(f, leg):
    """Updates leg['live'] in place from ESPN data and returns it."""
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    prev = leg.get("live") or {}
    if prev.get("final") and prev.get("status") in ("won", "lost", "push"):
        return prev  # already settled, nothing to refresh
    if leg.get("manualResult") in ("won", "lost", "push", "void"):
        leg["live"] = {"status": leg["manualResult"], "final": True, "detail": "Set by you", "updatedAt": now}
        return leg["live"]

    typ = (leg.get("type") or "").lower()
    sport = (leg.get("sport") or "").lower()
    if sport not in SPORT_PATHS:
        leg["live"] = {"status": "unsupported", "detail": "Sport not tracked live — mark it yourself", "updatedAt": now}
        return leg["live"]

    found = find_competition(f, leg)
    if not found and typ == "player_prop" and leg.get("player"):
        found = find_player_game(f, leg)
    if not found:
        leg["live"] = {"status": "unmatched", "detail": "Game not found yet (checks again soon)", "updatedAt": now}
        return leg["live"]
    path, ev, comp = found
    state, clock = game_state(comp)
    final = state == "post"
    comps = comp.get("competitors") or []
    live = {"eventId": str(ev.get("id")), "state": state, "clock": clock, "final": final, "updatedAt": now}

    if state == "pre" and typ != "player_prop":
        live.update(status="pending", detail=f"Starts {clock}")
        leg["live"] = live
        return live

    scoreline = " – ".join(f"{competitor_label(c)} {int(score_of(c))}" for c in comps) if sport != "tennis" else ""
    if sport == "tennis" and len(comps) == 2:
        sa, sb, ga, gb, txt = tennis_sets(comp)
        scoreline = f"{competitor_label(comps[0])} vs {competitor_label(comps[1])} {txt}".strip()

    try:
        if typ in ("moneyline", "spread", "team_total"):
            sel = leg.get("team") or ""
            if typ == "moneyline" and norm(sel) in ("draw", "tie"):
                diff = score_of(comps[0]) - score_of(comps[1])
                st = ("won" if diff == 0 else "lost") if final else ("winning" if diff == 0 else "losing")
                live.update(status=st, detail=scoreline)
            else:
                mine = next((c for c in comps if competitor_matches(sel, c)), None)
                other = next((c for c in comps if c is not mine), None)
                if not mine or not other:
                    live.update(status="unmatched", detail=f"Couldn't tell which side is '{sel}'")
                elif sport == "tennis":
                    sa, sb, ga, gb, txt = tennis_sets(comp)
                    me_first = mine is comps[0]
                    if typ == "moneyline":
                        if final and (mine.get("winner") is not None or other.get("winner") is not None):
                            st = "won" if mine.get("winner") else "lost"
                        else:
                            st = margin_result((sa - sb) if me_first else (sb - sa), final)
                    else:  # game handicap
                        gm = (ga - gb) if me_first else (gb - ga)
                        st = margin_result(gm + float(leg.get("line") or 0), final)
                    live.update(status=st, detail=scoreline)
                elif typ == "team_total":
                    val = score_of(mine)
                    live.update(status=over_under(val, float(leg["line"]), leg.get("side", "over"), final),
                                current=val, detail=f"{competitor_label(mine)} {int(val)} (line {leg['line']}) · {clock}")
                else:
                    margin = score_of(mine) - score_of(other)
                    if typ == "spread":
                        margin += float(leg.get("line") or 0)
                    live.update(status=margin_result(margin, final), detail=f"{scoreline} · {clock}")
        elif typ == "total":
            if sport == "tennis" and len(comps) == 2:
                _, _, ga, gb, _ = tennis_sets(comp)
                val = ga + gb
            else:
                val = sum(score_of(c) for c in comps)
            live.update(status=over_under(val, float(leg["line"]), leg.get("side", "over"), final),
                        current=val, detail=f"Total {int(val)} (line {leg['line']}) · {scoreline} · {clock}")
        elif typ == "player_prop":
            stat = leg.get("stat")
            summ = f.summary(path, ev.get("id"))
            val = player_stat(summ, leg.get("player"), stat)
            label = STAT_LABEL.get(stat, stat)
            if stat not in STAT_PARTS:
                live.update(status="unsupported", detail=f"Stat '{stat}' not tracked live — mark it yourself")
            elif val is None:
                if state == "pre":
                    live.update(status="pending", detail=f"Starts {clock}")
                elif final:
                    live.update(status="unmatched", detail=f"{leg.get('player')} not in box score (DNP?) — check & mark")
                else:
                    live.update(status="live", current=0, detail=f"{leg.get('player')}: no stats yet · {clock}")
            else:
                line = float(leg.get("line") or 0)
                side = leg.get("side", "over")
                st = over_under(val, line, side, final)
                need = int(line - val) + 1  # must go strictly over the line
                extra = f" (needs {need} more)" if side == "over" and st == "live" else ""
                live.update(status=st, current=val,
                            detail=f"{leg.get('player')} {val:g} {label} / {side} {line:g}{extra} · {clock}")
        else:
            live.update(status="unsupported", detail=f"Bet type '{typ}' not tracked live — mark it yourself")
    except Exception as e:
        print(f"evaluate_leg error: {e!r} leg={json.dumps(leg)[:500]}")
        live.update(status="error", detail="Couldn't read live data this round")
    leg["live"] = live
    return live
