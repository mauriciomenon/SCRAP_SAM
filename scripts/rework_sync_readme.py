#!/usr/bin/env python3
"""
Sync this workspace's README.md into ~/git/scrap_sam_rework/README.md
Writes a small summary to reports/rework_sync_readme.txt
"""
from __future__ import annotations

from pathlib import Path


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep = ws / "reports"
    rep.mkdir(parents=True, exist_ok=True)
    base = Path.home() / "git" / "scrap_sam_rework"
    src = ws / "README.md"
    dst = base / "README.md"
    if not src.exists():
        (rep / "rework_sync_readme.txt").write_text("README.md de origem não encontrado.\n", encoding="utf-8")
        return 1
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    (rep / "rework_sync_readme.txt").write_text(
        f"README sincronizado: {dst}\n", encoding="utf-8"
    )
    print(rep / "rework_sync_readme.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
