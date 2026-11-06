"""The check-constraints verdict: the reported violations against the pinned answer key."""

from .checks import finish


def pairs(violations):
    return [(violation.rule.value, violation.subject) for violation in violations]


def verify_task(arguments, output, reference, workspace):
    expected = reference.expected
    want, got = pairs(expected.violations), pairs(output.violations)
    missed, extra = sorted(set(want) - set(got)), sorted(set(got) - set(want))
    checks = [
        ("case", output.case == arguments.case, f"report is for {output.case.value}, task is {arguments.case.value}"),
        ("no-duplicates", len(set(got)) == len(got), "a (rule, subject) pair is listed twice"),
        ("no-missed-violations", not missed, f"missed: {missed}"),
        ("no-false-alarms", not extra, f"reported but not broken: {extra}"),
        ("compliant-flag", output.compliant == expected.compliant, f"compliant is {output.compliant}, expected {expected.compliant}"),
        ("flag-matches-list", output.compliant == (not got), "compliant must be true exactly when no violation is listed"),
    ]
    return finish(checks, f"{len(want)} violation(s) found and reported exactly in case {arguments.case.value}")
