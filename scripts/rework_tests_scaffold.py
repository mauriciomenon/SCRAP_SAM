#!/usr/bin/env python3
"""
Create minimal pytest scaffold in ~/git/scrap_sam_rework/tests if missing.

Non-destructive: only writes files that do not already exist.
Writes a report to reports/rework_tests_scaffold.txt listing created files.
"""
from __future__ import annotations

from pathlib import Path


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"
TESTS_DIR = REWORK_BASE / "tests"

TEST_SANITY = """
import importlib
import pytest

@pytest.mark.parametrize("mod", [
    "pandas",
    "selenium",
    "dash",
    "plotly",
    "requests",
    "bs4",
    "yaml",
])
def test_can_import(mod):
    importlib.import_module(mod)
""".lstrip()


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep_dir = ws / "reports"
    rep_dir.mkdir(parents=True, exist_ok=True)
    out_path = rep_dir / "rework_tests_scaffold.txt"

    if not REWORK_BASE.exists():
        out_path.write_text(f"Base não encontrada: {REWORK_BASE}\n", encoding="utf-8")
        print(out_path)
        return 1

    TESTS_DIR.mkdir(parents=True, exist_ok=True)
    created = []

    sanity = TESTS_DIR / "test_sanity_imports.py"
    if not sanity.exists():
        sanity.write_text(TEST_SANITY, encoding="utf-8")
        created.append(sanity)

    if created:
        lines = ["Arquivos de teste criados:"] + [f"- {p}" for p in created]
    else:
        lines = ["Nenhum teste criado (já existiam)."]

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
