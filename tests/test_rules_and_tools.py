import pytest

from contract import Case, CheckInput
from plugin import IMPLEMENTATIONS, rules
from plugin.data import CASES, case
from plugin.tools import get_allocation, pin_violations


def pairs(a):
    return [tuple(x) for x in rules.violations(a)]


def test_main_matches_the_hand_derived_answer() -> None:
    # AAA 0.28 > 0.25; Tech = 0.28 + 0.20 + 0.10 = 0.58 > 0.45; HHH not allowed; cash 0.03 < 0.05; sum = 1.00
    assert pairs(CASES["main"]) == [
        ("disallowed-ticker", "HHH"),
        ("max-position", "AAA"),
        ("max-sector", "Tech"),
        ("min-cash", "CASH"),
    ]


def test_other_cases() -> None:
    assert pairs(CASES["at-limits"]) == []  # exactly at every limit
    assert pairs(CASES["all-cash"]) == []
    assert pairs(CASES["sum-error"]) == [("negative-weight", "AAA"), ("weights-sum", "PORTFOLIO")]


def test_just_over_a_limit_is_a_violation() -> None:
    over = case((0.25, 0.45, 0.05), [("AAA", 0.2501), ("DDD", 0.25), ("FFF", 0.25), ("GGG", 0.1999)], 0.05)
    assert pairs(over) == [("max-position", "AAA")]


def test_sector_can_break_its_cap_without_a_single_position_doing_so() -> None:
    many = case((0.15, 0.35, 0.10), [("AAA", 0.15), ("BBB", 0.15), ("CCC", 0.15), ("DDD", 0.15)], 0.40)
    assert pairs(many) == [("max-sector", "Tech")]


def test_tools() -> None:
    assert len(IMPLEMENTATIONS) == 2
    out = get_allocation(CheckInput(case=Case.MAIN), None)
    assert {t.sector: t.weight for t in out.sector_totals} == {"Tech": 0.58, "Health": 0.15, "Energy": 0.12, "Finance": 0.12}
    assert out.total_weight == 1.0
    pin = pin_violations(CheckInput(case=Case.MAIN), None).expected
    assert pin.compliant is False and len(pin.violations) == 4
    assert pin_violations(CheckInput(case=Case.ALL_CASH), None).expected.compliant is True


@pytest.mark.parametrize("name", list(CASES))
def test_every_case_has_a_consistent_answer(name: str) -> None:
    pin = pin_violations(CheckInput(case=Case(name)), None).expected
    assert pin.compliant == (not pin.violations)
