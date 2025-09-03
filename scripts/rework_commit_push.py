#!/usr/bin/env python3
"""
Stage, commit, and push non-destructive changes for this repo (SCRAP_SAM)
and the forked rework at ~/git/scrap_sam_rework.

Writes a detailed log to reports/rework_commit_push.txt.

Behavior:
- SCRAP_SAM: stages scripts/, docs/, tests/
- scrap_sam_rework: stages .flake8, pyproject.toml, mypy.ini, log_instrucoes.md, tests/
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable, Tuple


def run(cmd: Iterable[str], cwd: Path | None = None, timeout: int | None = None) -> Tuple[int, str]:
    try:
        out = subprocess.check_output(
            list(cmd), stderr=subprocess.STDOUT, cwd=str(cwd) if cwd else None, timeout=timeout
        )
        return 0, out.decode("utf-8", errors="replace")
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output.decode("utf-8", errors="replace")
    except Exception as e:  # generic
        return 1, f"ERROR: {e}"


def git_commit_and_push(repo: Path, add_paths: list[str], message: str) -> list[str]:
    lines: list[str] = []
    lines.append(f"Repo: {repo}")
    code, out = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo)
    branch = out.strip() if code == 0 else "(unknown)"
    lines.append(f"Branch: {branch}")
    code, out = run(["git", "status", "-sb"], cwd=repo)
    lines.append("-- status -sb --\n" + out)

    # Stage paths
    for p in add_paths:
        code, out = run(["git", "add", "-A", p], cwd=repo)
        if code != 0:
            lines.append(f"add {p}: FAILED\n{out}")

    # Show staged
    code, out = run(["git", "diff", "--cached", "--name-only"], cwd=repo)
    staged = [ln for ln in out.splitlines() if ln.strip()]
    lines.append("-- staged --\n" + ("\n".join(staged) or "(none)"))
    if staged:
        code, out = run(["git", "commit", "-m", message], cwd=repo)
        lines.append("-- commit --\n" + out)
        # Push current HEAD to its upstream
        code, out = run(["git", "push", "-u", "origin", "HEAD"], cwd=repo)
        lines.append("-- push --\n" + out)
    else:
        lines.append("Nothing to commit.")

    return lines


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep_dir = ws / "reports"
    rep_dir.mkdir(parents=True, exist_ok=True)
    out_path = rep_dir / "rework_commit_push.txt"

    lines: list[str] = []

    # SCRAP_SAM (this repo)
    lines.append("== SCRAP_SAM ==")
    lines.extend(
        git_commit_and_push(
            repo=ws,
            add_paths=["scripts", "docs", "tests"],
            message=(
                "chore(rework): add rework automation scripts, update instruction log, and test scaffolds; "
                "no runtime behavior changes"
            ),
        )
    )

    # Rework repo
    rework = Path.home() / "git" / "scrap_sam_rework"
    lines.append("")
    lines.append("== scrap_sam_rework ==")
    if rework.exists():
        lines.extend(
            git_commit_and_push(
                repo=rework,
                add_paths=[".flake8", "pyproject.toml", "mypy.ini", "log_instrucoes.md", "tests"],
                message=(
                    "chore(config): normalize flake8/mypy/black configs and sync instruction log; "
                    "no code changes"
                ),
            )
        )
    else:
        lines.append(f"Rework base not found: {rework}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
