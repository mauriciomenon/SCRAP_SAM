#!/usr/bin/env python3
"""
Write ~/git/scrap_sam_rework/mypy.ini with compatible settings:
- no_implicit_optional = False
- exclude backups (bkp)
- ignore_missing_imports for third-party libs (pandas, plotly, dash, dbc, xlsxwriter, pdfkit, requests, yaml, bs4, numpy, psutil, schedule, thread, sklearn)

Idempotent overwrite. Writes summary to reports/rework_write_mypy_ini.txt
"""
from __future__ import annotations

from pathlib import Path


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"
REPORT = Path(__file__).resolve().parents[1] / "reports" / "rework_write_mypy_ini.txt"

MYPY_INI = (
    """
[mypy]
no_implicit_optional = False
python_version = 3.13
exclude = (src/dashboard/bkp/)

[mypy-pandas]
ignore_missing_imports = True
[mypy-pandas.*]
ignore_missing_imports = True
[mypy-plotly]
ignore_missing_imports = True
[mypy-plotly.*]
ignore_missing_imports = True
[mypy-dash]
ignore_missing_imports = True
[mypy-dash.*]
ignore_missing_imports = True
[mypy-dash_bootstrap_components]
ignore_missing_imports = True
[mypy-xlsxwriter]
ignore_missing_imports = True
[mypy-pdfkit]
ignore_missing_imports = True
[mypy-requests]
ignore_missing_imports = True
[mypy-yaml]
ignore_missing_imports = True
[mypy-bs4]
ignore_missing_imports = True
[mypy-numpy]
ignore_missing_imports = True
[mypy-psutil]
ignore_missing_imports = True
[mypy-schedule]
ignore_missing_imports = True
[mypy-thread]
ignore_missing_imports = True
[mypy-sklearn]
ignore_missing_imports = True
"""
    .strip()
    + "\n"
)


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    ini = REWORK_BASE / "mypy.ini"
    ini.write_text(MYPY_INI, encoding="utf-8")
    REPORT.write_text(f"mypy.ini escrito em {ini}\n", encoding="utf-8")
    print(REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
