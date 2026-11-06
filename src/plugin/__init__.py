"""constraint-check: the tools and the table that maps each contract.Tool to its implementation."""

from contract import Tool
from plugin.tools import get_allocation, pin_violations

# Each tool's implementation: (its input, the workspace) -> its output, as contract.TOOLS types them.
IMPLEMENTATIONS = {
    Tool.GET_ALLOCATION: get_allocation,
    Tool.PIN_VIOLATIONS: pin_violations,
}

__all__ = ["IMPLEMENTATIONS", "get_allocation", "pin_violations"]
