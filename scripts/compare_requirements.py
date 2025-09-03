#!/usr/bin/env python3
"""
Compare requirements.txt between this repo and ~/git/scrap_sam_rework.

Usage:
  python scripts/compare_requirements.py [--write-report]

Outputs a unified summary to stdout and optionally writes to reports/requirements_diff.txt.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def load_reqs(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    return lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-report", action="store_true")
    args = ap.parse_args()

    base = Path(__file__).resolve().parents[1]
    legacy = base / "requirements.txt"
    rework = Path.home() / "git" / "scrap_sam_rework" / "requirements.txt"

    legacy_reqs = set(load_reqs(legacy))
    rework_reqs = set(load_reqs(rework))

    only_in_legacy = sorted(legacy_reqs - rework_reqs)
    only_in_rework = sorted(rework_reqs - legacy_reqs)
    in_both = sorted(legacy_reqs & rework_reqs)

    lines: list[str] = []
    lines.append(f"Legacy:  {legacy}")
    lines.append(f"Rework:  {rework}")
    lines.append("")
    lines.append("== Apenas no LEGADO ==")
    lines.extend(only_in_legacy or ["(nenhum)"])
    lines.append("")
    lines.append("== Apenas no REWORK ==")
    lines.extend(only_in_rework or ["(nenhum)"])
    lines.append("")
    lines.append("== Em ambos ==")
    lines.extend(in_both or ["(nenhum)"])

    output = "\n".join(lines)
    print(output)

    if args.write_report:
        report_dir = base / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        (report_dir / "requirements_diff.txt").write_text(output + "\n", encoding="utf-8")
        print(f"\nRelatório salvo em: {report_dir / 'requirements_diff.txt'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
