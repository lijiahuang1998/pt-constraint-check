"""The fixed investor profiles and proposed allocations, one per case. Synthetic tickers; nothing is fetched."""

UNIVERSE = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG"]
SECTORS = {"AAA": "Tech", "BBB": "Tech", "CCC": "Tech", "DDD": "Health", "EEE": "Health", "FFF": "Energy",
           "GGG": "Energy", "HHH": "Finance"}


def case(limits, weights, cash):
    """limits: (max_position, max_sector, min_cash). HHH is never an allowed ticker."""
    return {
        "profile": {"max_position": limits[0], "max_sector": limits[1], "min_cash": limits[2], "allowed_tickers": UNIVERSE},
        "holdings": [{"ticker": t, "sector": SECTORS[t], "weight": w} for t, w in weights],
        "cash": cash,
    }


CASES = {
    # four violations at once (moderate investor)
    "main": case((0.25, 0.45, 0.05),
                 [("AAA", 0.28), ("BBB", 0.20), ("CCC", 0.10), ("DDD", 0.15), ("FFF", 0.12), ("HHH", 0.12)], 0.03),
    # every value exactly at its limit: compliant
    "at-limits": case((0.25, 0.45, 0.05), [("AAA", 0.25), ("BBB", 0.20), ("DDD", 0.25), ("FFF", 0.25)], 0.05),
    # a negative weight, and holdings plus cash add up to 0.70
    "sum-error": case((0.40, 0.70, 0.0), [("AAA", -0.10), ("BBB", 0.30), ("DDD", 0.30)], 0.20),
    # nothing held: compliant
    "all-cash": case((0.15, 0.35, 0.10), [], 1.0),
}
