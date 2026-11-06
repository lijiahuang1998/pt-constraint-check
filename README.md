# Constraint Check

Give the agent a fixed investor profile and a proposed allocation; it lists every constraint the allocation breaks. This is the deterministic risk layer of PersonalTrader as a checkable task.

## Tools

- `get_allocation`: read one of four fixed cases (`main`, `at-limits`, `sum-error`, `all-cash`) with the profile, the holdings and exact sector totals.
- `pin_violations`: the answer key. NanoAgent runs it out of the model's sight; its output is the ground truth the verifier compares with. Not in the task's tools.

Task `check-constraints` (agent): read the allocation with `get_allocation`, then list every broken rule with its subject. The verifier compares the (rule, subject) pairs exactly and names missed violations and false alarms separately.

Rules: `max-position`, `max-sector`, `min-cash`, `disallowed-ticker`, `negative-weight`, `weights-sum`. A value exactly at its limit is not a violation.

## Layout

- `nanoagent.yaml`: the manifest (tools, task, instructions).
- `contract.py`: typed input and output of every tool and task.
- `src/plugin/`: the MCP server (`__main__.py`), the tools (`tools.py`), the rules (`rules.py`) and the fixed data (`data.py`).
- `verifier/`: the deterministic verifier: one module for the tools (`tools.py`), one for the task (`task.py`), shared `checks.py`.
- `tests/`: tests of the rules, the tools and the verifier (correct, wrong, missing, malformed and boundary results).
- `ui/`, `product/`: how outputs are drawn, and the product page.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
```

The data is fixed and there is no network access, so every run gives the same result.
