#!/usr/bin/env python3
"""
Apply approved cleanup moves in ~/git/scrap_sam_rework by relocating noisy files
(editor temps and " - Copia*.py") into bkp/ with preserved subpaths.

This is idempotent: if destination already exists, the source is left untouched.
Writes a report to reports/rework_cleanup_apply.txt.
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"
SCAN_DIRS = ("src",)

COPY_SUFFIX = re.compile(r" - Copia( \(\d+\))?\.py$")
TEMP_FILES = re.compile(r"tempCodeRunnerFile.*\.py$")


@dataclass
class MoveResult:
    src: Path
    dst: Path
    status: str  # moved|skipped-exists|skipped-missing|error
    reason: str


def plan_items() -> list[tuple[Path, Path, str]]:
    bkp = REWORK_BASE / "bkp"
    items: list[tuple[Path, Path, str]] = []
    for rel in SCAN_DIRS:
        root = REWORK_BASE / rel
        if not root.exists():
            continue
        for fp in root.rglob("*.py"):
            s = str(fp)
            if COPY_SUFFIX.search(s):
                dst = bkp / fp.relative_to(REWORK_BASE)
                items.append((fp, dst, "Cópia redundante"))
            elif TEMP_FILES.search(s):
                dst = bkp / fp.relative_to(REWORK_BASE)
                items.append((fp, dst, "Temp de editor"))
    return items


def apply_moves(items: list[tuple[Path, Path, str]]) -> list[MoveResult]:
    results: list[MoveResult] = []
    for src, dst, reason in items:
        if not src.exists():
            results.append(MoveResult(src, dst, "skipped-missing", reason))
            continue
        if dst.exists():
            results.append(MoveResult(src, dst, "skipped-exists", reason))
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            # use shutil.move to allow cross-device moves if any
            shutil.move(str(src), str(dst))
            results.append(MoveResult(src, dst, "moved", reason))
        except Exception as e:
            results.append(MoveResult(src, dst, "error", f"{reason}: {e}"))
    return results


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep_dir = ws / "reports"
    rep_dir.mkdir(parents=True, exist_ok=True)
    out_path = rep_dir / "rework_cleanup_apply.txt"

    if not REWORK_BASE.exists():
        out_path.write_text(f"Base não encontrada: {REWORK_BASE}\n", encoding="utf-8")
        print(out_path)
        return 1

    items = plan_items()
    results = apply_moves(items)

    moved = sum(1 for r in results if r.status == "moved")
    errors = [r for r in results if r.status == "error"]

    lines = [
        f"Base: {REWORK_BASE}",
        f"Itens analisados: {len(results)}",
        f"Movidos: {moved}",
        f"Erros: {len(errors)}",
        "",
    ]
    for r in results:
        lines.append(f"{r.status:16s}  {r.src} -> {r.dst}  # {r.reason}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
