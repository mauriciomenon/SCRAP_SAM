# Release v0.0.1-dashboard-helper

Highlights
- New dashboard helpers (non-destructive):
  - scripts/rework_run_dashboard.py — driver mode with import shims and safe fallback DataFrame
  - scripts/dashboard_quickstart.py — boot UI with minimal in-memory data
  - scripts/generate_sample_excel.py — create downloads/Report.xlsx sample
- Logs and reports updated; idempotent usage.

Usage
- Quickstart (run in rework venv):
  - Launch with minimal data: scripts/dashboard_quickstart.py
  - Driver mode (prefer real Excel at rework/downloads/Report.xlsx):
    scripts/rework_run_dashboard.py --driver --background

Notes
- Compatible with Dash 3 (uses .run on app instance when applicable).
- Import-time shims avoid breaking source: alias SSAAnalyzer→SSAWeekAnalyzer; provide lightweight timedelta.
- Fallback DataFrame built by SSAColumns indices to avoid IndexError when data is empty.

Troubleshooting
- If port 8050 busy, stop previous run (logs/dashboard.pid) or set a different port in the script when needed.
- If pandas/dash missing, activate the rework virtualenv and reinstall dependencies.
