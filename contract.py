"""Each tool's and task's typed input and output (see nanoagent.plugin.contract): declarations only."""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Tool(Enum):
    GET_ALLOCATION = "get_allocation"
    PIN_VIOLATIONS = "pin_violations"


class Task(Enum):
    CHECK_CONSTRAINTS = "check-constraints"


class Case(Enum):
    MAIN = "main"
    AT_LIMITS = "at-limits"
    SUM_ERROR = "sum-error"
    ALL_CASH = "all-cash"


class Rule(Enum):
    MAX_POSITION = "max-position"
    MAX_SECTOR = "max-sector"
    MIN_CASH = "min-cash"
    DISALLOWED_TICKER = "disallowed-ticker"
    NEGATIVE_WEIGHT = "negative-weight"
    WEIGHTS_SUM = "weights-sum"


CASE = "Which fixed allocation: main, at-limits, sum-error or all-cash"
SUBJECT = (
    "The ticker for max-position, disallowed-ticker and negative-weight; the sector for max-sector; CASH for "
    "min-cash; PORTFOLIO for weights-sum"
)


@dataclass
class CheckInput(Output):
    case: Annotated[Case, CASE]


@dataclass
class Profile(Output):
    max_position: Annotated[float, "The largest weight one holding may have"]
    max_sector: Annotated[float, "The largest total weight one sector may have"]
    min_cash: Annotated[float, "The smallest cash weight"]
    allowed_tickers: Annotated[list[str], "The only tickers that may be held"]


@dataclass
class Holding(Output):
    ticker: str
    sector: str
    weight: Annotated[float, "The share of the portfolio, 0.25 means 25%"]


@dataclass
class SectorTotal(Output):
    sector: str
    weight: Annotated[float, "The sum of the weights of the sector's holdings, exact to 12 decimals"]


@dataclass
class AllocationOutput(Output):
    case: Annotated[Case, "The case that was read"]
    profile: Annotated[Profile, "The investor's limits"]
    holdings: Annotated[list[Holding], "The proposed holdings"]
    cash: Annotated[float, "The proposed cash weight"]
    sector_totals: Annotated[list[SectorTotal], "Each held sector's total weight, computed by rules: use as given"]
    total_weight: Annotated[float, "The sum of all holding weights and the cash weight, exact to 12 decimals"]


@dataclass
class Violation(Output):
    rule: Annotated[Rule, "The rule that is broken"]
    subject: Annotated[str, SUBJECT]


@dataclass
class ViolationsOutput(Output):
    case: Annotated[Case, "The case this report is for, copied from the task"]
    compliant: Annotated[bool, "True only when there is no violation"]
    violations: Annotated[list[Violation], "Every broken rule, one entry per rule and subject; [] for none"]


@dataclass
class PinOutput(Output):
    case: Annotated[Case, "The case pinned"]
    expected: Annotated[ViolationsOutput, "The answer key for the case"]


TOOLS = {
    Tool.GET_ALLOCATION: (CheckInput, AllocationOutput),
    Tool.PIN_VIOLATIONS: (CheckInput, PinOutput),
}
TASKS = {
    Task.CHECK_CONSTRAINTS: (CheckInput, ViolationsOutput),
}
