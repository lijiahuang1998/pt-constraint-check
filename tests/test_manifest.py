"""The manifest, the contract, the README and pyproject.toml agree with each other."""

import re
from pathlib import Path

from contract import TASKS, TOOLS

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = (ROOT / "nanoagent.yaml").read_text()
README = (ROOT / "README.md").read_text()
PYPROJECT = (ROOT / "pyproject.toml").read_text()


def section(name: str) -> str:
    """The indented block under a top-level key of the manifest."""
    match = re.search(rf"^{name} > .*?:\n(.*?)(?=^\S|\Z)", MANIFEST, re.DOTALL | re.MULTILINE)
    assert match, name
    return match.group(1)


def test_every_tool_and_task_is_in_the_manifest_and_the_readme() -> None:
    tools = set(re.findall(r"^  ([a-z_]+):$", section("tools"), re.MULTILINE))
    tasks = set(re.findall(r"^  ([a-z-]+):$", section("tasks"), re.MULTILINE))
    assert tools == {tool.value for tool in TOOLS}
    assert tasks == {task.value for task in TASKS}
    for name in tools | tasks:
        assert f"`{name}`" in README


def test_versions_and_ids_match() -> None:
    version = re.search(r"^version: (\S+)$", MANIFEST, re.MULTILINE).group(1)
    plugin_id = re.search(r"^id: (\S+)$", MANIFEST, re.MULTILINE).group(1)
    assert f'version = "{version}"' in PYPROJECT and f'name = "nanoagent-{plugin_id}"' in PYPROJECT
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", plugin_id)
    assert "spec: nanoagent.plugin/v0001" in MANIFEST
    assert "runtime" in MANIFEST and "[uv, run, --frozen, python, -m, plugin]" in MANIFEST


def test_every_task_names_a_reference_and_known_tools() -> None:
    names = {tool.value for tool in TOOLS}
    for block in re.findall(r"^    tools: \[(.*?)\]$", MANIFEST, re.MULTILINE):
        assert {part.strip() for part in block.split(",")} <= names
    for reference in re.findall(r"^    reference: (\S+)$", MANIFEST, re.MULTILINE):
        assert reference in names


def test_readme_keeps_the_required_sections_in_order() -> None:
    positions = [README.index(title) for title in ("## Tools", "## Layout", "## Develop and run")]
    assert positions == sorted(positions) and README.startswith("# ")
