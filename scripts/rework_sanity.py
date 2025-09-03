#!/usr/bin/env python3
"""
Run non-destructive sanity checks against ~/git/scrap_sam_rework using its venv.

Checks:
- Resolve rework venv python
- Print python/pip versions
- Import common libs (pandas, selenium, playwright, dash, plotly, requests, bs4, yaml)

Also writes a report to reports/rework_sanity.txt in this workspace.
Performs optional dev checks (black --check, flake8, mypy, pytest).
"""
from __future__ import annotations

import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None, timeout: int | None = None) -> tuple[int, str]:
    try:
        out = subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT,
            cwd=str(cwd) if cwd else None,
            timeout=timeout,
        )
        return 0, out.decode("utf-8", errors="replace")
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output.decode("utf-8", errors="replace")
    except subprocess.TimeoutExpired as e:
        return 124, (e.output or b"TIMEOUT").decode("utf-8", errors="replace")


def main() -> int:
    def write_report(lines: list[str]) -> Path:
        ws = Path(__file__).resolve().parents[1]
        rep_dir = ws / "reports"
        rep_dir.mkdir(parents=True, exist_ok=True)
        out_path = rep_dir / "rework_sanity.txt"
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return out_path

    base = Path.home() / "git" / "scrap_sam_rework"
    py = base / ".venv" / "bin" / "python"
    if not py.exists():
        print(f"Python do rework não encontrado: {py}")
        return 1

    out_lines = []
    out_lines.append(f"Usando: {py}")
    print(f"Usando: {py}")
    code, out = run([str(py), "-c", "import sys; import platform; print(platform.python_version()); print(sys.executable)"])
    print("Python:")
    print(out)
    out_lines.append("Python:\n" + out)

    code, out = run([str(py), "-m", "pip", "--version"])
    print("Pip:")
    print(out)
    out_lines.append("Pip:\n" + out)
    # flush early
    out_file = write_report(out_lines)

    imports = [
        ("pandas", "import pandas as m; print('pandas', m.__version__)"),
        ("selenium", "import selenium as m; print('selenium', getattr(m,'__version__','?'))"),
        ("playwright", "import playwright; print('playwright ok')"),
        ("dash", "import dash as m; print('dash', getattr(m,'__version__','?'))"),
        ("plotly", "import plotly as m; print('plotly', getattr(m,'__version__','?'))"),
        ("requests", "import requests as m; print('requests', m.__version__)"),
        ("bs4", "import bs4; import bs4 as m; print('beautifulsoup4 ok')"),
        ("yaml", "import yaml; print('pyyaml ok')"),
    ]
    for name, expr in imports:
        code, out = run([str(py), "-c", expr])
        status = "OK" if code == 0 else "FAIL"
        print(f"[{status}] {name} ->")
        print(out)
        out_lines.append(f"[{status}] {name} ->\n{out}")
    # flush after imports
    out_file = write_report(out_lines)

    # Dev tool checks (non-destructive)
    print("\nChecando ferramentas de desenvolvimento (não-destrutivo):")
    out_lines.append("\nChecando ferramentas de desenvolvimento (não-destrutivo):")
    # Versions
    for mod in ("black", "flake8", "mypy", "pytest"):
        code, out = run([str(py), "-m", mod, "--version"], cwd=base, timeout=60)
        status = "OK" if code == 0 else "FAIL"
        print(f"[{status}] {mod} --version ->")
        print(out)
        out_lines.append(f"[{status}] {mod} --version ->\n{out}")
    out_file = write_report(out_lines)

    # Run checks (no changes)
    # Paths to check (typical)
    # Only include existing paths
    paths = [p for p in ("src", "tests") if (base / p).exists()]
    if not paths:
        out_lines.append("Nenhum caminho encontrado para checagem (src/tests ausentes).")
        out_file = write_report(out_lines)
        print(f"Relatório: {out_file}")
        return 0
    out_file = write_report(out_lines)
    # black --check
    code, out = run([str(py), "-m", "black", "--check", *paths], cwd=base, timeout=120)
    print("black --check:")
    print(out)
    out_lines.append("black --check:\n" + out)
    out_file = write_report(out_lines)
    # flake8
    code, out = run([str(py), "-m", "flake8", *paths], cwd=base, timeout=120)
    print("flake8:")
    print(out)
    out_lines.append("flake8:\n" + out)
    out_file = write_report(out_lines)
    # mypy
    # emit config preview to help understand behaviors
    code_cfg, out_cfg = run([str(py), "-m", "mypy", "--show-config"], cwd=base, timeout=60)
    out_lines.append("mypy --show-config:\n" + out_cfg)
    out_file = write_report(out_lines)
    code, out = run([str(py), "-m", "mypy", *paths], cwd=base, timeout=180)
    print("mypy:")
    print(out)
    out_lines.append("mypy:\n" + out)
    out_file = write_report(out_lines)
    # pytest (quiet)
    code, out = run([str(py), "-m", "pytest", "-q"], cwd=base, timeout=300)
    print("pytest -q:")
    print(out)
    out_lines.append("pytest -q:\n" + out)
    out_file = write_report(out_lines)
    out_file = write_report(out_lines)
    print(f"Relatório: {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
