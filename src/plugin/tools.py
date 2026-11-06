"""The two tools: get_allocation (what the agent sees) and pin_violations (the answer key, out of its sight)."""

from pathlib import Path

from contract import (
    AllocationOutput,
    CheckInput,
    Holding,
    PinOutput,
    Profile,
    Rule,
    SectorTotal,
    Violation,
    ViolationsOutput,
)
from plugin import rules
from plugin.data import CASES


def get_allocation(given: CheckInput, workspace: Path) -> AllocationOutput:
    case = CASES[given.case.value]
    return AllocationOutput(
        case=given.case,
        profile=Profile(**case["profile"]),
        holdings=[Holding(**holding) for holding in case["holdings"]],
        cash=case["cash"],
        sector_totals=[SectorTotal(sector=s, weight=w) for s, w in rules.sector_totals(case).items()],
        total_weight=rules.total_weight(case),
    )


def pin_violations(given: CheckInput, workspace: Path) -> PinOutput:
    found = [Violation(rule=Rule(rule), subject=subject) for rule, subject in rules.violations(CASES[given.case.value])]
    return PinOutput(case=given.case, expected=ViolationsOutput(case=given.case, compliant=not found, violations=found))
