#!/usr/bin/env python3
"""
Ensure pyproject.toml in ~/git/scrap_sam_rework has a mypy exclude for backup paths.
Adds [tool.mypy] section with exclude if missing, or merges exclude list conservatively.
Writes a summary to reports/rework_update_mypy_exclude.txt
"""
from __future__ import annotations

from pathlib import Path


def ensure_mypy_exclude(pyproject: Path, pattern: str) -> bool:
    text = pyproject.read_text(encoding="utf-8", errors="replace") if pyproject.exists() else ""
    changed = False
    if "[tool.mypy]" not in text:
        # Create a minimal mypy tool section
        block = f"\n[tool.mypy]\nexclude = [\n    \"{pattern}\",\n]\n"
        text = (text + "\n" if text and not text.endswith("\n") else text) + block
        changed = True
    else:
        # Try to find an existing exclude array; if not present, append it
        if "exclude =" not in text.split("[tool.mypy]")[1]:
            insert = f"exclude = [\n    \"{pattern}\",\n]\n"
            text = text.replace("[tool.mypy]", "[tool.mypy]\n" + insert)
            changed = True
        elif pattern not in text:
            # naive append inside the array
            text = text.replace(
                "]\n", f"    \"{pattern}\",\n]\n", 1
            )
            changed = True
    if changed:
        pyproject.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep = ws / "reports"
    rep.mkdir(parents=True, exist_ok=True)
    base = Path.home() / "git" / "scrap_sam_rework"
    pyproject = base / "pyproject.toml"
    if not pyproject.exists():
        (rep / "rework_update_mypy_exclude.txt").write_text(
            f"pyproject.toml não encontrado em {base}\n", encoding="utf-8"
        )
        return 1
    changed = ensure_mypy_exclude(pyproject, "src/dashboard/bkp/")
    msg = "mypy exclude atualizado" if changed else "mypy exclude já presente"
    (rep / "rework_update_mypy_exclude.txt").write_text(msg + "\n", encoding="utf-8")
    print(rep / "rework_update_mypy_exclude.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
