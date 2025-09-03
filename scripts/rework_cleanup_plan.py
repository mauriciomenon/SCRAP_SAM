#!/usr/bin/env python3
"""
Analyze ~/git/scrap_sam_rework for noisy files (copies, temp runners, backups) and
emit a move/rename plan WITHOUT performing changes. Output -> reports/rework_cleanup_plan.txt
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"
SCAN_DIRS = ("src",)

COPY_SUFFIX = re.compile(r" - Copia( \(\d+\))?\.py$")
TEMP_FILES = re.compile(r"tempCodeRunnerFile.*\.py$")


@dataclass
class PlanItem:
    src: Path
    dst: Path
    reason: str


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep_dir = ws / "reports"
    rep_dir.mkdir(parents=True, exist_ok=True)
    out_path = rep_dir / "rework_cleanup_plan.txt"

    if not REWORK_BASE.exists():
        out_path.write_text(f"Base não encontrada: {REWORK_BASE}\n", encoding="utf-8")
        print(out_path)
        return 1

    bkp = REWORK_BASE / "bkp"
    plans: list[PlanItem] = []

    for rel in SCAN_DIRS:
        root = REWORK_BASE / rel
        if not root.exists():
            continue
        for fp in root.rglob("*.py"):
            s = str(fp)
            if COPY_SUFFIX.search(s):
                dst = bkp / fp.relative_to(REWORK_BASE)
                plans.append(PlanItem(fp, dst, "Cópia redundante"))
            elif TEMP_FILES.search(s):
                dst = bkp / fp.relative_to(REWORK_BASE)
                plans.append(PlanItem(fp, dst, "Temp de editor"))

    lines = [f"Base: {REWORK_BASE}", f"Itens planejados: {len(plans)}", ""]
    for it in plans:
        lines.append(f"mv '{it.src}' '{it.dst}'  # {it.reason}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
