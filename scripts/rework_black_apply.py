#!/usr/bin/env python3
"""
Apply Black formatting to ~/git/scrap_sam_rework using its venv.

Behavior-preserving. Targets src/ and tests/ if present.
Writes reports/rework_black_apply.txt with a summary.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None, timeout: int | None = None) -> tuple[int, str]:
    try:
        out = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, cwd=str(cwd) if cwd else None, timeout=timeout
        )
        return 0, out.decode("utf-8", errors="replace")
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output.decode("utf-8", errors="replace")


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep = ws / "reports"
    rep.mkdir(parents=True, exist_ok=True)
    base = Path.home() / "git" / "scrap_sam_rework"
    py = base / ".venv" / "bin" / "python"
    if not py.exists():
        (rep / "rework_black_apply.txt").write_text(
            f"Python do rework não encontrado: {py}\n", encoding="utf-8"
        )
        return 1

    targets = [p for p in ("src", "tests") if (base / p).exists()]
    if not targets:
        (rep / "rework_black_apply.txt").write_text(
            "Nenhum caminho (src/tests) encontrado no rework.\n", encoding="utf-8"
        )
        return 0

    # Run black in write mode
    code, out = run([str(py), "-m", "black", *targets], cwd=base, timeout=600)
    (rep / "rework_black_apply.txt").write_text(out, encoding="utf-8")
    print(rep / "rework_black_apply.txt")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
