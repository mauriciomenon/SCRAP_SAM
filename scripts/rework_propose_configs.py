#!/usr/bin/env python3
"""
Propose non-destructive config files for ~/git/scrap_sam_rework.

Writes suggested files ONLY if they don't already exist:
- .flake8 (sane ignores and 88 cols)
- pyproject.toml (black line-length=88)

Outputs the list of created files and their paths to reports/rework_propose_configs.txt.
"""
from __future__ import annotations

from pathlib import Path


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"

FLAKE8 = """
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .venv, .git, build, dist, __pycache__, bkp
""".strip() + "\n"

PYPROJECT = """
[tool.black]
line-length = 88
target-version = ["py313"]
include = '\\.pyi?$'
exclude = '(/\\.venv|/build|/dist|/\\.git|/bkp)'
""".strip() + "\n"


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep_dir = ws / "reports"
    rep_dir.mkdir(parents=True, exist_ok=True)
    out_path = rep_dir / "rework_propose_configs.txt"

    if not REWORK_BASE.exists():
        out_path.write_text(f"Base não encontrada: {REWORK_BASE}\n", encoding="utf-8")
        print(out_path)
        return 1

    created: list[Path] = []

    flake = REWORK_BASE / ".flake8"
    if not flake.exists():
        flake.write_text(FLAKE8, encoding="utf-8")
        created.append(flake)

    pyproj = REWORK_BASE / "pyproject.toml"
    if not pyproj.exists():
        pyproj.write_text(PYPROJECT, encoding="utf-8")
        created.append(pyproj)

    if created:
        lines = ["Arquivos criados:"] + [f"- {p}" for p in created]
    else:
        lines = ["Nenhum arquivo criado (já existiam)."]

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
