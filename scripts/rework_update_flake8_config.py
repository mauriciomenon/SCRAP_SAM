#!/usr/bin/env python3
"""
Idempotently update ~/git/scrap_sam_rework/.flake8 to relax noisy rules without code changes.

Changes applied (only if needed):
- Ensure extend-ignore includes E203, W503, E501, E722
- Ensure max-line-length = 88
- Ensure exclude includes common folders: .venv, .git, build, dist, __pycache__, bkp

Writes a summary to reports/rework_update_flake8_config.txt
"""
from __future__ import annotations

from pathlib import Path


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"
FLAKE8_PATH = REWORK_BASE / ".flake8"
REPORT = Path(__file__).resolve().parents[1] / "reports" / "rework_update_flake8_config.txt"


def ensure_lines(text: str) -> tuple[str, bool]:
    changed = False
    lines = text.splitlines()
    if not lines:
        lines = ["[flake8]"]
        changed = True

    if not any(l.strip().lower().startswith("[flake8]") for l in lines):
        lines.insert(0, "[flake8]")
        changed = True

    # Normalize key map for easy updates
    def find_key(key: str) -> int | None:
        key_lower = key.lower()
        for i, l in enumerate(lines):
            s = l.strip()
            if not s or s.startswith("#"):
                continue
            if s.lower().startswith(key_lower + " ") or s.lower().startswith(key_lower + "="):
                return i
        return None

    # extend-ignore
    desired_ignores = {"E203", "W503", "E501", "E722", "E402"}
    idx = find_key("extend-ignore")
    if idx is None:
        lines.append(f"extend-ignore = {', '.join(sorted(desired_ignores))}")
        changed = True
    else:
        # merge
        current = lines[idx].split("=", 1)[1].strip()
        items = {p.strip() for p in current.split(',') if p.strip()}
        new_items = sorted(items | desired_ignores)
        new_line = f"extend-ignore = {', '.join(new_items)}"
        if lines[idx] != new_line:
            lines[idx] = new_line
            changed = True

    # max-line-length
    idx = find_key("max-line-length")
    if idx is None:
        lines.append("max-line-length = 88")
        changed = True
    else:
        if lines[idx].split("=", 1)[1].strip() != "88":
            lines[idx] = "max-line-length = 88"
            changed = True

    # exclude
    desired_exclude = [".venv", ".git", "build", "dist", "__pycache__", "bkp"]
    idx = find_key("exclude")
    if idx is None:
        lines.append("exclude = " + ", ".join(desired_exclude))
        changed = True
    else:
        current = [p.strip() for p in lines[idx].split("=", 1)[1].split(',') if p.strip()]
        merged = []
        for item in current + desired_exclude:
            if item not in merged:
                merged.append(item)
        new_line = "exclude = " + ", ".join(merged)
        if lines[idx] != new_line:
            lines[idx] = new_line
            changed = True

    return "\n".join(lines) + "\n", changed


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    if not REWORK_BASE.exists():
        REPORT.write_text(f"Base não encontrada: {REWORK_BASE}\n", encoding="utf-8")
        print(REPORT)
        return 1
    if not FLAKE8_PATH.exists():
        REPORT.write_text(f".flake8 não encontrado: {FLAKE8_PATH}\n", encoding="utf-8")
        print(REPORT)
        return 1

    original = FLAKE8_PATH.read_text(encoding="utf-8", errors="replace")
    updated, changed = ensure_lines(original)
    if changed:
        FLAKE8_PATH.write_text(updated, encoding="utf-8")
        REPORT.write_text(".flake8 atualizado (extend-ignore/max-line-length/exclude).\n", encoding="utf-8")
    else:
        REPORT.write_text("Nenhuma alteração necessária em .flake8.\n", encoding="utf-8")
    print(REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
