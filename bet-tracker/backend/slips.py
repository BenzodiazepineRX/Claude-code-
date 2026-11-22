"""Slip math and settlement."""
import datetime as dt

FINAL_STATES = ("won", "lost", "push", "void")


def american_to_decimal(odds):
    try:
        o = float(str(odds).replace("+", "").strip())
    except (TypeError, ValueError):
        return None
    if o == 0:
        return None
    if -100 < o < 100 and o > 1:  # already decimal (e.g. 2.5)
        return o
    return 1 + (o / 100 if o > 0 else 100 / abs(o))


def money(x):
    try:
        return round(float(x), 2)
    except (TypeError, ValueError):
        return 0.0


def expected_payout(slip, legs=None):
    """Total return if the slip wins. Prefers the payout printed on the slip."""
    legs = slip.get("legs", []) if legs is None else legs
    stake = money(slip.get("stake"))
    if legs is slip.get("legs") and slip.get("payout"):
        return money(slip["payout"])
    dec = 1.0
    for leg in legs:
        d = american_to_decimal(leg.get("odds"))
        if d is None:
            # fall back to slip-level odds or printed payout
            so = american_to_decimal(slip.get("odds"))
            if so and legs is slip.get("legs"):
                return money(stake * so)
            return money(slip.get("payout")) or 0.0
        dec *= d
    return money(stake * dec)


def leg_result(leg):
    if leg.get("manualResult") in FINAL_STATES:
        return leg["manualResult"]
    live = leg.get("live") or {}
    st = live.get("status")
    if st in ("won", "lost", "push") and (live.get("final") or st in ("won", "lost")):
        return st
    return None


def settle(slip, now=None):
    """Sets status/profit when the slip is decided. Returns True if it changed."""
    if slip.get("manualStatus") in FINAL_STATES:
        status = slip["manualStatus"]
    else:
        results = [leg_result(l) for l in slip.get("legs", [])]
        if not results:
            return False
        if "lost" in results:
            status = "lost"          # one losing leg kills a parlay right away
        elif all(r is not None for r in results):
            live_legs = [l for l, r in zip(slip["legs"], results) if r not in ("push", "void")]
            status = "won" if live_legs else "push"
        else:
            status = "open"
    if status == "open":
        changed = slip.get("status") not in (None, "open")
        slip["status"] = "open"
        slip.pop("settledAt", None)
        slip["profit"] = 0.0
        return changed
    stake = money(slip.get("stake"))
    if status == "won":
        live_legs = [l for l in slip["legs"] if leg_result(l) not in ("push", "void")]
        payout = expected_payout(slip) if len(live_legs) == len(slip["legs"]) else expected_payout(slip, live_legs)
        # no payout or odds on file: don't record a fake loss, wait for the user to add the payout
        profit = money(payout - stake) if payout > 0 else 0.0
        slip["needsPayout"] = payout <= 0
    elif status == "lost":
        profit = -stake
    else:  # push / void: stake returned
        profit = 0.0
    changed = slip.get("status") != status or slip.get("profit") != profit
    slip["status"] = status
    slip["profit"] = profit
    if changed or not slip.get("settledAt"):
        slip["settledAt"] = (now or dt.datetime.now(dt.timezone.utc)).isoformat(timespec="seconds")
    return changed


def summarize_live(slip):
    """A one-line headline for the slip card: how many legs are hitting."""
    legs = slip.get("legs", [])
    good = sum(1 for l in legs if (l.get("live") or {}).get("status") in ("won", "winning"))
    bad = sum(1 for l in legs if (l.get("live") or {}).get("status") in ("lost", "losing"))
    slip["liveSummary"] = {"legs": len(legs), "hitting": good, "missing": bad}
