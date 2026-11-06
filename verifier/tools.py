"""Per-tool checks: what a tool's input and output must mean, beyond their types."""

from contract import Tool

from .checks import result


def get_allocation_input(value):
    return result(True, "get_allocation reads one of the fixed cases")


def get_allocation_output(input_value, output_value, workspace):
    if output_value.case != input_value.case:
        return result(False, "get_allocation returned another case than the one asked for")
    held = {holding.sector for holding in output_value.holdings}
    if {total.sector for total in output_value.sector_totals} != held:
        return result(False, "sector_totals must list exactly the held sectors")
    return result(True, "get_allocation returned the case's profile, holdings and totals")


def pin_violations_input(value):
    return result(True, "pin_violations pins one of the fixed cases")


def pin_violations_output(input_value, output_value, workspace):
    if output_value.case != input_value.case or output_value.expected.case != input_value.case:
        return result(False, "the pinned answer is for another case")
    if output_value.expected.compliant != (not output_value.expected.violations):
        return result(False, "the pinned answer's compliant flag contradicts its violations")
    return result(True, "the answer key is pinned")


INPUT_CHECKS = {Tool.GET_ALLOCATION: get_allocation_input, Tool.PIN_VIOLATIONS: pin_violations_input}
OUTPUT_CHECKS = {Tool.GET_ALLOCATION: get_allocation_output, Tool.PIN_VIOLATIONS: pin_violations_output}
