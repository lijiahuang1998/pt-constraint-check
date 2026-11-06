import pytest
from slimconfig import build_output, plain_output

import verifier
from contract import TASKS, TOOLS, Case, CheckInput, Task, Tool, ViolationsOutput
from plugin.tools import get_allocation, pin_violations


# The verifier gets contract instances, as NanoAgent's sandbox builds them from JSON.
def verify_task(arguments: dict, output: dict, reference) -> dict:
    given, made = TASKS[Task.CHECK_CONSTRAINTS]
    return verifier.verify_task("check-constraints", build_output(arguments, given), build_output(output, made), reference, "ws")


def pinned(case: str):
    return pin_violations(CheckInput(case=Case(case)), None)


def perfect(case: str) -> dict:
    return plain_output(pinned(case).expected)


def failed(verdict: dict) -> set:
    return {c["name"] for c in verdict["details"]["checks"] if not c["ok"]}


@pytest.mark.parametrize("case", ["main", "at-limits", "sum-error", "all-cash"])
def test_the_answer_key_passes_in_every_case(case: str) -> None:
    verdict = verify_task({"case": case}, perfect(case), pinned(case))
    assert verdict["valid"] is True and verdict["score"] == 1.0


def test_order_of_violations_does_not_matter() -> None:
    out = perfect("main")
    out["violations"].reverse()
    assert verify_task({"case": "main"}, out, pinned("main"))["valid"] is True


def test_a_missed_violation_is_named() -> None:
    out = perfect("main")
    out["violations"] = [v for v in out["violations"] if v["rule"] != "max-sector"]
    verdict = verify_task({"case": "main"}, out, pinned("main"))
    assert verdict["valid"] is False and failed(verdict) == {"no-missed-violations"}
    assert "max-sector" in verdict["message"]


def test_a_false_alarm_is_named() -> None:
    out = perfect("main")
    out["violations"].append({"rule": "max-position", "subject": "BBB"})
    assert failed(verify_task({"case": "main"}, out, pinned("main"))) == {"no-false-alarms"}


def test_a_wrong_subject_is_both_a_miss_and_a_false_alarm() -> None:
    out = perfect("main")
    out["violations"][1]["subject"] = "BBB"
    assert failed(verify_task({"case": "main"}, out, pinned("main"))) == {"no-missed-violations", "no-false-alarms"}


def test_a_wrong_rule_fails() -> None:
    out = perfect("sum-error")
    out["violations"][1]["rule"] = "min-cash"
    assert verify_task({"case": "sum-error"}, out, pinned("sum-error"))["valid"] is False


def test_the_compliant_flag_must_match() -> None:
    out = perfect("main") | {"compliant": True}
    assert failed(verify_task({"case": "main"}, out, pinned("main"))) == {"compliant-flag", "flag-matches-list"}
    assert failed(verify_task({"case": "all-cash"}, perfect("all-cash") | {"compliant": False}, pinned("all-cash"))) == {
        "compliant-flag",
        "flag-matches-list",
    }


def test_a_duplicate_entry_fails() -> None:
    out = perfect("main")
    out["violations"].append(out["violations"][0])
    assert "no-duplicates" in failed(verify_task({"case": "main"}, out, pinned("main")))


def test_inventing_a_violation_when_compliant_fails() -> None:
    out = {"case": "at-limits", "compliant": False, "violations": [{"rule": "max-position", "subject": "AAA"}]}
    verdict = verify_task({"case": "at-limits"}, out, pinned("at-limits"))
    assert verdict["valid"] is False and "no-false-alarms" in failed(verdict)


def test_a_report_for_another_case_fails() -> None:
    assert "case" in failed(verify_task({"case": "main"}, perfect("all-cash"), pinned("main")))


@pytest.mark.parametrize(
    "bad",
    [
        {"compliant": "no"},  # not a bool
        {"violations": [{"rule": "too-risky", "subject": "AAA"}]},  # unknown rule
        {"violations": [{"rule": "max-position"}]},  # missing subject
        {"violations": "none"},  # not a list
        {"case": "weekly"},
    ],
)
def test_malformed_outputs_cannot_even_be_built(bad: dict) -> None:
    with pytest.raises(Exception):  # noqa: B017 - the sandbox refuses a value of the wrong type
        build_output(perfect("main") | bad, ViolationsOutput)


def test_tool_checks() -> None:
    given = CheckInput(case=Case.MAIN)
    assert verifier.verify_input("get_allocation", given)["valid"] is True
    assert verifier.verify_output("get_allocation", given, get_allocation(given, None), "ws")["valid"] is True
    other = get_allocation(CheckInput(case=Case.ALL_CASH), None)
    assert verifier.verify_output("get_allocation", given, other, "ws")["valid"] is False
    assert verifier.verify_output("pin_violations", given, pinned("main"), "ws")["valid"] is True
    assert verifier.verify_output("pin_violations", given, pinned("at-limits"), "ws")["valid"] is False
    assert set(TOOLS) == set(verifier.tools.INPUT_CHECKS) == set(verifier.tools.OUTPUT_CHECKS) == {
        Tool.GET_ALLOCATION,
        Tool.PIN_VIOLATIONS,
    }
