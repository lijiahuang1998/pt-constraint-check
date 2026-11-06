"""Checks shared by the verifier modules. Pure functions of their arguments."""

import math


def result(valid, message, *, score=None, **details):
    return {
        "valid": valid,
        "score": float(valid) if score is None else score,
        "message": message,
        "details": details,
    }


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def close(got, want, tolerance):
    """Both None, or both numbers within ``tolerance``."""
    if want is None or got is None:
        return want is None and got is None
    return is_number(got) and abs(got - want) <= tolerance


def finish(checks, headline):
    """Turn a list of (name, ok, message) checks into a verdict: valid only when every check holds."""
    passed = sum(1 for _, ok, _ in checks if ok)
    failed = [(name, message) for name, ok, message in checks if not ok]
    details = {"checks": [{"name": name, "ok": ok, "message": message} for name, ok, message in checks]}
    if not failed:
        return result(True, f"All {len(checks)} checks hold: {headline}.", score=1.0, **details)
    first = failed[0]
    more = f" ({len(failed) - 1} more failed)" if len(failed) > 1 else ""
    return result(False, f"{first[0]}: {first[1]}{more}", score=min(passed / len(checks), 0.99), **details)
