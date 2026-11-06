"""The six constraint rules, in code."""

EPS = 1e-9  # a weight exactly at its limit is not a violation


def sector_totals(case):
    totals = {}
    for holding in case["holdings"]:
        totals[holding["sector"]] = totals.get(holding["sector"], 0.0) + holding["weight"]
    return {sector: round(total, 12) for sector, total in totals.items()}


def total_weight(case):
    return round(sum(h["weight"] for h in case["holdings"]) + case["cash"], 12)


def violations(case):
    """The (rule, subject) pairs the case breaks, sorted."""
    profile, found = case["profile"], set()
    for holding in case["holdings"]:
        if holding["ticker"] not in profile["allowed_tickers"]:
            found.add(("disallowed-ticker", holding["ticker"]))
        if holding["weight"] < 0:
            found.add(("negative-weight", holding["ticker"]))
        if holding["weight"] > profile["max_position"] + EPS:
            found.add(("max-position", holding["ticker"]))
    for sector, total in sector_totals(case).items():
        if total > profile["max_sector"] + EPS:
            found.add(("max-sector", sector))
    if case["cash"] < profile["min_cash"] - EPS:
        found.add(("min-cash", "CASH"))
    if abs(total_weight(case) - 1.0) > 1e-6:
        found.add(("weights-sum", "PORTFOLIO"))
    return sorted(found)
