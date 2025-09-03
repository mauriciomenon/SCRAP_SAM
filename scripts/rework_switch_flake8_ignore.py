#!/usr/bin/env python3
"""
Switch ~/git/scrap_sam_rework/.flake8 to use 'ignore' (E203,W503,E402,E501,E722)
instead of 'extend-ignore', preserving max-line-length and exclude entries.
Idempotent and non-destructive. Writes summary to reports/rework_switch_flake8_ignore.txt
"""
from __future__ import annotations

from pathlib import Path


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"
FLAKE8_PATH = REWORK_BASE / ".flake8"
REPORT = Path(__file__).resolve().parents[1] / "reports" / "rework_switch_flake8_ignore.txt"


DEF_IGNORES = ["E203", "W503", "E402", "E501", "E722"]


def switch_to_ignore(text: str) -> tuple[str, bool]:
    changed = False
    lines = text.splitlines()
    if not any(l.strip().lower().startswith("[flake8]") for l in lines):
        lines.insert(0, "[flake8]")
        changed = True

    # Remove any extend-ignore lines and merge into ignore
    ignore_set = set()
    new_lines: list[str] = []
    for l in lines:
        s = l.strip()
        if s.lower().startswith("extend-ignore"):
            parts = l.split("=", 1)[1].split(",")
            for p in parts:
                p = p.strip()
                if p:
                    ignore_set.add(p)
            changed = True
            continue
        if s.lower().startswith("ignore"):
            parts = l.split("=", 1)[1].split(",")
            for p in parts:
                p = p.strip()
                if p:
                    ignore_set.add(p)
            # skip; we'll rewrite later
            changed = True
            continue
        new_lines.append(l)

    for p in DEF_IGNORES:
        ignore_set.add(p)

    # Append/replace ignore line at end of section
    # Find first [flake8] index to place ignore right after it if possible
    inserted = False
    for i, l in enumerate(new_lines):
        if l.strip().lower().startswith("[flake8]"):
            new_lines.insert(i + 1, f"ignore = {', '.join(sorted(ignore_set))}")
            inserted = True
            break
    if not inserted:
        new_lines.append(f"ignore = {', '.join(sorted(ignore_set))}")

    out = "\n".join(new_lines) + "\n"
    return out, changed


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    if not FLAKE8_PATH.exists():
        REPORT.write_text(f".flake8 não encontrado: {FLAKE8_PATH}\n", encoding="utf-8")
        print(REPORT)
        return 1
    original = FLAKE8_PATH.read_text(encoding="utf-8", errors="replace")
    updated, changed = switch_to_ignore(original)
    if changed:
        FLAKE8_PATH.write_text(updated, encoding="utf-8")
        REPORT.write_text(".flake8: chave 'ignore' aplicada com E203,W503,E402,E501,E722.\n", encoding="utf-8")
    else:
        REPORT.write_text(".flake8: nenhuma alteração necessária.\n", encoding="utf-8")
    print(REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
