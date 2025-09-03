#!/usr/bin/env python3
"""
Generate a Black diff for ~/git/scrap_sam_rework (non-destructive).

Outputs:
- reports/rework_black_diff.patch (full --diff output)
- reports/rework_black_summary.txt (counts and files list)
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
    if not base.exists():
        (rep / "rework_black_summary.txt").write_text(
            f"Base não encontrada: {base}\n", encoding="utf-8"
        )
        print(rep / "rework_black_summary.txt")
        return 1

    targets = [p for p in ("src", "tests") if (base / p).exists()]
    if not targets:
        (rep / "rework_black_summary.txt").write_text(
            "Nenhum caminho (src/tests) encontrado no rework.\n", encoding="utf-8"
        )
        print(rep / "rework_black_summary.txt")
        return 0

    # --check for counts, then --diff for patch
    _, check_out = run([str(base / ".venv/bin/python"), "-m", "black", "--check", *targets], cwd=base, timeout=300)
    code, diff_out = run([str(base / ".venv/bin/python"), "-m", "black", "--diff", *targets], cwd=base, timeout=600)

    # Save patch
    (rep / "rework_black_diff.patch").write_text(diff_out, encoding="utf-8")

    # Summarize
    changed_files: list[str] = []
    for line in check_out.splitlines():
        # lines like: would reformat /path/to/file.py
        if line.startswith("would reformat "):
            changed_files.append(line.removeprefix("would reformat ").strip())

    summary = [
        f"Alvos: {', '.join(targets)}",
        f"Arquivos a formatar: {len(changed_files)}",
    ]
    if changed_files:
        summary.append("")
        summary.append("Arquivos:")
        summary.extend(f"- {p}" for p in changed_files)

    (rep / "rework_black_summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(rep / "rework_black_summary.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
