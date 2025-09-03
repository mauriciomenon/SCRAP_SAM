#!/usr/bin/env python3
"""
Ensure mypy overrides for third-party modules without type hints in ~/git/scrap_sam_rework.

Behavior: Non-destructive. Idempotently injects a marked overrides block into pyproject.toml
under [tool.mypy]. If the block already exists, it is replaced. If [tool.mypy] is missing,
it is created. Writes a summary to reports/rework_update_mypy_overrides.txt.

Targets ignored via overrides (ignore_missing_imports = true):
- plotly, plotly.*
- dash, dash.*
- dash_bootstrap_components
- xlsxwriter
- pdfkit
- timedelta (guard for mis-imports found by mypy)

This reduces mypy noise from third-party libs without altering runtime behavior.
"""
from __future__ import annotations

from pathlib import Path


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"
PYPROJECT = REWORK_BASE / "pyproject.toml"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"


BEGIN_MARK = "# COPILOT: mypy overrides begin"
END_MARK = "# COPILOT: mypy overrides end"

OVERRIDES_BLOCK = f"""
{BEGIN_MARK}
[[tool.mypy.overrides]]
module = [
    "pandas",
    "pandas.*",
  "plotly",
  "plotly.*",
  "dash",
  "dash.*",
  "dash_bootstrap_components",
  "xlsxwriter",
  "pdfkit",
  "timedelta",
    "requests",
    "yaml",
    "bs4",
    "numpy",
    "psutil",
    "schedule",
    "thread",
    "sklearn",
]
ignore_missing_imports = true
{END_MARK}
""".strip() + "\n"


def insert_or_replace_mypy_overrides(text: str) -> tuple[str, bool]:
    """
    Append the overrides block at the very end of the file to avoid leaking
    subsequent top-level [tool.mypy] keys (e.g., 'exclude') into the last
    [[tool.mypy.overrides]] table. If an old marked block exists, remove it
    first, then append a fresh one at the end.
    """
    new_text = text
    if BEGIN_MARK in new_text and END_MARK in new_text:
        start = new_text.index(BEGIN_MARK)
        end = new_text.index(END_MARK) + len(END_MARK)
        # Remove existing block
        new_text = new_text[:start] + new_text[end:]

    # Ensure final newline
    if not new_text.endswith("\n"):
        new_text += "\n"

    # Always append overrides at the end, using fully-qualified [[tool.mypy.overrides]]
    appended = [""]
    # We don't need to ensure [tool.mypy] exists because the fully-qualified
    # path in [[tool.mypy.overrides]] is valid anywhere in the TOML file.
    appended.extend(OVERRIDES_BLOCK.rstrip("\n").splitlines())
    appended.append("")
    final_text = new_text + "\n".join(appended)
    changed = final_text != text
    return final_text, changed


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report = REPORTS_DIR / "rework_update_mypy_overrides.txt"

    if not PYPROJECT.exists():
        report.write_text(f"pyproject.toml não encontrado: {PYPROJECT}\n", encoding="utf-8")
        print(report)
        return 1

    original = PYPROJECT.read_text(encoding="utf-8", errors="replace")
    updated, changed = insert_or_replace_mypy_overrides(original)
    if changed:
        PYPROJECT.write_text(updated, encoding="utf-8")
        report.write_text(
            "Overrides do mypy inseridos/atualizados com sucesso (ignore_missing_imports para libs sem stubs).\n",
            encoding="utf-8",
        )
    else:
        report.write_text("Nenhuma alteração necessária (overrides já presentes).\n", encoding="utf-8")

    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
