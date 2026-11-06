"""The verifier runs in NanoAgent's sandbox: standard library only, no clock, files, network or reflection."""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "verifier"
ALLOWED = {"re", "json", "math", "hashlib", "pathlib", "dataclasses", "enum", "collections", "itertools",
           "statistics", "decimal", "fractions", "contract"}
BANNED_NAMES = {"open", "eval", "exec", "compile", "getattr", "setattr", "delattr", "globals", "locals", "vars",
                "input", "__import__"}


def test_verifier_folder_holds_only_python_files() -> None:
    assert {p.suffix for p in ROOT.iterdir() if p.is_file()} == {".py"}


def test_verifier_obeys_the_sandbox_rules() -> None:
    problems = []
    for path in ROOT.glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                problems += [f"{path.name}: import {a.name}" for a in node.names if a.name.split(".")[0] not in ALLOWED]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                if node.module.split(".")[0] not in ALLOWED:
                    problems.append(f"{path.name}: from {node.module}")
            elif isinstance(node, ast.Name) and node.id in BANNED_NAMES:
                problems.append(f"{path.name}: name {node.id}")
            elif isinstance(node, ast.Attribute) and node.attr.startswith("_"):
                problems.append(f"{path.name}: attribute {node.attr}")
    assert problems == []
