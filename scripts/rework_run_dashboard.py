#!/usr/bin/env python3
"""
Start the dashboard from the rework repo (~/git/scrap_sam_rework) non-destructively.

What it does:
- Picks a likely entry file (src/dashboard/Dashboard_SM.py, DashboardSM/Dashboard_SM.py, Dashboard_SM.py, or first match).
- Uses the rework venv's Python (~/git/scrap_sam_rework/.venv/bin/python).
- Sets PYTHONPATH to include rework/src to help imports.
- Writes logs to ~/git/scrap_sam_rework/logs/dashboard_YYYYmmdd_HHMMSS.log.
- Optionally runs in background with --background and prints PID.

It does not modify project code.
"""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path


REWORK = Path.home() / "git" / "scrap_sam_rework"
VENV_PY = REWORK / ".venv" / "bin" / "python"


def find_entry() -> Path | None:
    candidates = [
        REWORK / "src" / "dashboard" / "Dashboard_SM.py",
        REWORK / "DashboardSM" / "Dashboard_SM.py",
        REWORK / "Dashboard_SM.py",
    ]
    for c in candidates:
        if c.exists():
            return c
    # Fallback: shallow search for common filenames
    for name in ("Dashboard_SM.py", "app.py", "dashboard.py"):
        for fp in REWORK.rglob(name):
            try:
                rel = fp.relative_to(REWORK)
            except Exception:
                rel = fp
            # skip backups and venv/git
            s = str(rel)
            if any(p in s for p in (".venv/", ".git/", "/backups/", "Dashboard.zip")):
                continue
            return fp
    return None


def ensure_paths() -> None:
    if not REWORK.exists():
        sys.exit(f"Rework repo not found: {REWORK}")
    if not VENV_PY.exists():
        sys.exit(f"Rework venv Python not found: {VENV_PY}")


def run(background: bool, inject_compat: bool, driver: bool, excel: str | None) -> int:
    ensure_paths()
    entry = find_entry()
    if not entry:
        print("No dashboard entry found (looked for Dashboard_SM.py/app.py/dashboard.py).", file=sys.stderr)
        return 2

    logs_dir = REWORK / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    logfile = logs_dir / f"dashboard_{ts}.log"
    pidfile = logs_dir / "dashboard.pid"

    env = os.environ.copy()
    # Prepend rework/src to PYTHONPATH to make local imports work regardless of CWD
    src_dir = REWORK / "src"
    py_path = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (str(src_dir) + os.pathsep + py_path) if py_path else str(src_dir)

    # Build command: optionally inject small compat shim without changing project files
    if driver:
        # Driver mode: import the entry module, get SSADashboard, load DataFrame from Excel (or fallback), run app
        # This avoids executing the entry's __main__ which may expect external side effects.
        shim = (
            "import sys, os, importlib.util, types\n"
            "import pandas as pd\n"
            "from datetime import timedelta as _dt_timedelta\n"
            f"_entry = r'{entry}'\n"
            f"_src = r'{REWORK / 'src'}'\n"
            "_edir = os.path.dirname(_entry)\n"
            "for _p in (_edir, _src):\n"
            "    if _p and _p not in sys.path:\n"
            "        sys.path.insert(0, _p)\n"
            "# Provide a lightweight 'timedelta' module if the project imports it as a package\n"
            "_td_mod = types.ModuleType('timedelta')\n"
            "setattr(_td_mod, 'timedelta', _dt_timedelta)\n"
            "try:\n"
            "    from pandas import Timedelta as _pd_Timedelta\n"
            "    setattr(_td_mod, 'Timedelta', _pd_Timedelta)\n"
            "except Exception:\n"
            "    pass\n"
            "sys.modules.setdefault('timedelta', _td_mod)\n"
            "# If Report_from_excel exists but renamed analyzer, alias it before loading entry\n"
            "try:\n"
            "    import Report_from_excel as _ref\n"
            "    if not hasattr(_ref, 'SSAAnalyzer') and hasattr(_ref, 'SSAWeekAnalyzer'):\n"
            "        _ref.SSAAnalyzer = _ref.SSAWeekAnalyzer\n"
            "except Exception:\n"
            "    pass\n"
            "# Load entry module\n"
            "_spec = importlib.util.spec_from_file_location('rework_entry', _entry)\n"
            "if _spec is None or _spec.loader is None:\n"
            "    raise RuntimeError('Cannot load entry module')\n"
            "rework_entry = importlib.util.module_from_spec(_spec)\n"
            "_spec.loader.exec_module(rework_entry)\n"
            "SSACls = getattr(rework_entry, 'SSADashboard', None)\n"
            "if SSACls is None:\n"
            "    raise RuntimeError('SSADashboard not found in entry')\n"
            "# Load DataFrame: try Report_from_excel.DataLoader, else pandas.read_excel(header=2), else fallback\n"
            f"_excel = r'{excel or str(REWORK / 'downloads' / 'Report.xlsx')}'\n"
            "df = None\n"
            "# Prefer DataLoader if available so column positions match SSAColumns\n"
            "try:\n"
            "    import Report_from_excel as RFE\n"
            "    DL = getattr(RFE, 'DataLoader', None)\n"
            "    if DL is not None and os.path.exists(_excel):\n"
            "        df = DL(_excel).load_data()\n"
            "except Exception:\n"
            "    df = None if df is None else df\n"
            "if df is None and os.path.exists(_excel):\n"
            "    try:\n"
            "        df = pd.read_excel(_excel, header=2)\n"
            "    except Exception:\n"
            "        df = None\n"
            "if df is None:\n"
            "    # Build a minimal DataFrame sized by SSAColumns to avoid IndexError on iloc\n"
            "    SSAColumns = None\n"
            "    try:\n"
            "        import Report_from_excel as RFE2\n"
            "        SSAColumns = getattr(RFE2, 'SSAColumns', None)\n"
            "    except Exception:\n"
            "        pass\n"
            "    if SSAColumns is None:\n"
            "        SSAColumns = getattr(rework_entry, 'SSAColumns', None)\n"
            "    ncols = 30\n"
            "    idxs = []\n"
            "    if SSAColumns is not None:\n"
            "        try:\n"
            "            idxs = [getattr(SSAColumns, n) for n in dir(SSAColumns) if not n.startswith('_') and isinstance(getattr(SSAColumns, n), int)]\n"
            "            if idxs:\n"
            "                ncols = max(idxs) + 1\n"
            "        except Exception:\n"
            "            pass\n"
            "    data = [['' for _ in range(ncols)] for __ in range(2)]\n"
            "    # Try to fill commonly used columns if indices known\n"
            "    def _safe_set(r, idx, val):\n"
            "        try:\n"
            "            data[r][idx] = val\n"
            "        except Exception:\n"
            "            pass\n"
            "    try:\n"
            "        SITUACAO = getattr(SSAColumns, 'SITUACAO')\n"
            "        SEMANA_PROGRAMADA = getattr(SSAColumns, 'SEMANA_PROGRAMADA')\n"
            "        RESPONSAVEL_PROGRAMACAO = getattr(SSAColumns, 'RESPONSAVEL_PROGRAMACAO')\n"
            "        RESPONSAVEL_EXECUCAO = getattr(SSAColumns, 'RESPONSAVEL_EXECUCAO')\n"
            "        GRAU_PRIORIDADE_EMISSAO = getattr(SSAColumns, 'GRAU_PRIORIDADE_EMISSAO')\n"
            "        SETOR_EXECUTOR = getattr(SSAColumns, 'SETOR_EXECUTOR')\n"
            "        EMITIDA_EM = getattr(SSAColumns, 'EMITIDA_EM')\n"
            "        _safe_set(0, SITUACAO, 'Aberta')\n"
            "        _safe_set(1, SITUACAO, 'Em Execução')\n"
            "        _safe_set(0, SEMANA_PROGRAMADA, '2024-W45')\n"
            "        _safe_set(1, SEMANA_PROGRAMADA, '2024-W46')\n"
            "        _safe_set(0, RESPONSAVEL_PROGRAMACAO, 'Alice')\n"
            "        _safe_set(1, RESPONSAVEL_PROGRAMACAO, 'Carlos')\n"
            "        _safe_set(0, RESPONSAVEL_EXECUCAO, 'Bob')\n"
            "        _safe_set(1, RESPONSAVEL_EXECUCAO, 'Daniel')\n"
            "        _safe_set(0, GRAU_PRIORIDADE_EMISSAO, 'S3.7')\n"
            "        _safe_set(1, GRAU_PRIORIDADE_EMISSAO, 'S2')\n"
            "        _safe_set(0, SETOR_EXECUTOR, 'MANUT')\n"
            "        _safe_set(1, SETOR_EXECUTOR, 'ELETR')\n"
            "        _safe_set(0, EMITIDA_EM, '2024-11-01 08:00:00')\n"
            "        _safe_set(1, EMITIDA_EM, '2024-11-05 10:30:00')\n"
            "    except Exception:\n"
            "        pass\n"
            "    df = pd.DataFrame(data)\n"
            "app = SSACls(df)\n"
            "dash_app = getattr(app, 'app', None)\n"
            "if dash_app is None:\n"
            "    raise RuntimeError('SSADashboard missing app attribute')\n"
            "dash_app.run(debug=False, port=8050)\n"
        )
        cmd = [str(VENV_PY), "-u", "-c", shim]
    elif inject_compat:
        # Ensure both the script directory and REWORK/src are in sys.path, then inject a light alias.
        shim = (
            "import sys, os, runpy\n"
            f"_entry = r'{entry}'\n"
            f"_src = r'{REWORK / 'src'}'\n"
            "_edir = os.path.dirname(_entry)\n"
            "for _p in (_edir, _src):\n"
            "    if _p and _p not in sys.path:\n"
            "        sys.path.insert(0, _p)\n"
            "try:\n"
            "    import Report_from_excel as _ref\n"
            "    if not hasattr(_ref, 'SSAAnalyzer') and hasattr(_ref, 'SSAWeekAnalyzer'):\n"
            "        _ref.SSAAnalyzer = _ref.SSAWeekAnalyzer\n"
            "except Exception:\n"
            "    pass\n"
            "runpy.run_path(_entry, run_name='__main__')\n"
        )
        cmd = [str(VENV_PY), "-u", "-c", shim]
    else:
        # Respect common port/host defaults used by Dash; we don't force change runtime behavior
        cmd = [str(VENV_PY), "-u", str(entry)]

    # Print what we'll do
    print(f"Rework: {REWORK}")
    print(f"Entry : {entry.relative_to(REWORK)}")
    print(f"Using : {VENV_PY}")
    print(f"Log   : {logfile}")
    print(f"PYTHONPATH prepended: {src_dir}")
    print(f"Command: {shlex.join(cmd)}")

    stdout = open(logfile, "ab")
    stderr = subprocess.STDOUT

    if background:
        proc = subprocess.Popen(cmd, cwd=str(REWORK), env=env, stdout=stdout, stderr=stderr)
        pidfile.write_text(str(proc.pid), encoding="utf-8")
        print(f"Started in background, PID {proc.pid}")
        # Show first log lines
        try:
            proc.poll()
            stdout.flush()
        except Exception:
            pass
        try:
            with open(logfile, "rb") as fh:
                head = fh.read(4096)
            sys.stdout.write(head.decode("utf-8", errors="replace"))
        except Exception:
            pass
        return 0
    else:
        # Foreground: stream output
        with subprocess.Popen(cmd, cwd=str(REWORK), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            out = p.stdout
            if out is None:
                return p.wait()
            while True:
                chunk = out.read(4096)
                if not chunk:
                    break
                sys.stdout.buffer.write(chunk)
                stdout.write(chunk)
                sys.stdout.flush()
                stdout.flush()
            return p.wait()


def main() -> int:
    ap = argparse.ArgumentParser(description="Run dashboard from rework repo")
    ap.add_argument("--background", action="store_true", help="Run in background and print PID")
    ap.add_argument("--inject-compat", action="store_true", help="Inject runtime compat shims (alias SSAAnalyzer→SSAWeekAnalyzer) without modifying code")
    ap.add_argument("--driver", action="store_true", help="Import SSADashboard and run with DataFrame from Excel (or fallback) without executing __main__")
    ap.add_argument("--excel", help="Path to Excel file to load (defaults to rework/downloads/Report.xlsx)")
    args = ap.parse_args()
    return run(background=args.background, inject_compat=args.inject_compat, driver=args.driver, excel=args.excel)


if __name__ == "__main__":
    raise SystemExit(main())
