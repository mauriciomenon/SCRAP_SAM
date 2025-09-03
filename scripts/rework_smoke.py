#!/usr/bin/env python3
"""
Lightweight, non-destructive smoke checks against ~/git/scrap_sam_rework.

What it does:
- Walks the rework "src/" and (optionally) "tests/" trees and AST-parses all .py files
  to catch syntax errors without executing any code.
- Skips obvious noise and heavy files: backups, copies, temp files, zip, etc.
- Writes a report to this workspace at reports/rework_smoke.txt.

It DOES NOT import or run code from the rework project, so it's safe.
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"
SCAN_DIRS = ("src", "tests")

# Exclude patterns: directories or filenames matching any of these regexes will be skipped
EXCLUDE_RES = [
    re.compile(r"(^|/)\.venv(/|$)"),
    re.compile(r"(^|/)\.git(/|$)"),
    re.compile(r"(^|/)build(/|$)"),
    re.compile(r"(^|/)dist(/|$)"),
    re.compile(r"(^|/)Dashboard\.zip$"),
    re.compile(r"(^|/)bkp(/|$)"),
    re.compile(r" - Copia( \(\d+\))?\.py$"),
    re.compile(r"tempCodeRunnerFile.*\.py$"),
]


@dataclass
class SyntaxIssue:
    path: Path
    line: int
    col: int
    msg: str


def should_exclude(p: Path) -> bool:
    s = str(p)
    return any(r.search(s) for r in EXCLUDE_RES)


def iter_py_files(root: Path, rels: Iterable[str]) -> Iterable[Path]:
    for rel in rels:
        base = root / rel
        if not base.exists():
            continue
        for fp in base.rglob("*.py"):
            if should_exclude(fp):
                continue
            yield fp


def ast_check_file(fp: Path) -> list[SyntaxIssue]:
    try:
        text = fp.read_text(encoding="utf-8", errors="replace")
    except Exception as e:  # IO issues
        return [SyntaxIssue(fp, 0, 0, f"IOError: {e}")]
    try:
        ast.parse(text, filename=str(fp))
        return []
    except SyntaxError as e:
        return [SyntaxIssue(fp, getattr(e, 'lineno', 0) or 0, getattr(e, 'offset', 0) or 0, e.msg or "SyntaxError")]


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep_dir = ws / "reports"
    rep_dir.mkdir(parents=True, exist_ok=True)
    out_path = rep_dir / "rework_smoke.txt"

    if not REWORK_BASE.exists():
        out_path.write_text(f"Base não encontrada: {REWORK_BASE}\n", encoding="utf-8")
        print(out_path)
        return 1

    files = list(iter_py_files(REWORK_BASE, SCAN_DIRS))
    issues: list[SyntaxIssue] = []
    for fp in files:
        issues.extend(ast_check_file(fp))

    lines: list[str] = []
    lines.append(f"Base: {REWORK_BASE}")
    lines.append(f"Arquivos verificados: {len(files)}")
    lines.append(f"Erros de sintaxe: {len(issues)}")
    lines.append("")
    if issues:
        lines.append("Detalhes:")
        for it in issues:
            lines.append(f"- {it.path}: L{it.line} C{it.col}: {it.msg}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
