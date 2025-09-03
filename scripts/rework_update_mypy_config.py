#!/usr/bin/env python3
"""
Ensure ~/git/scrap_sam_rework/pyproject.toml has [tool.mypy] no_implicit_optional = false.

This reduces PEP 484-related noise without changing runtime behavior. Idempotent.
Writes summary to reports/rework_update_mypy_config.txt
"""
from __future__ import annotations

from pathlib import Path


REWORK_BASE = Path.home() / "git" / "scrap_sam_rework"
PYPROJECT = REWORK_BASE / "pyproject.toml"
REPORT = Path(__file__).resolve().parents[1] / "reports" / "rework_update_mypy_config.txt"


def upsert_no_implicit_optional(text: str) -> tuple[str, bool]:
    changed = False
    if "[tool.mypy]" not in text:
        block = "\n[tool.mypy]\nno_implicit_optional = false\n"
        text = (text + "\n" if text and not text.endswith("\n") else text) + block
        changed = True
        return text, changed

    # If present, replace or add key beneath first [tool.mypy] section
    parts = text.split("[tool.mypy]")
    head, rest = parts[0], "[tool.mypy]" + "[tool.mypy]".join(parts[1:])
    # Find end of first section: next [tool. or end
    idx_next = rest.find("\n[tool.")
    if idx_next == -1:
        body, tail = rest, ""
    else:
        body, tail = rest[:idx_next], rest[idx_next:]

    if "no_implicit_optional" in body:
        lines = body.splitlines()
        for i, l in enumerate(lines):
            if l.strip().startswith("no_implicit_optional"):
                if l.strip() != "no_implicit_optional = false":
                    lines[i] = "no_implicit_optional = false"
                    changed = True
        new_body = "\n".join(lines)
    else:
        if not body.endswith("\n"):
            body += "\n"
        new_body = body + "no_implicit_optional = false\n"
        changed = True

    return head + new_body + tail, changed


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    if not PYPROJECT.exists():
        REPORT.write_text(f"pyproject.toml não encontrado: {PYPROJECT}\n", encoding="utf-8")
        print(REPORT)
        return 1
    original = PYPROJECT.read_text(encoding="utf-8", errors="replace")
    updated, changed = upsert_no_implicit_optional(original)
    if changed:
        PYPROJECT.write_text(updated, encoding="utf-8")
        REPORT.write_text("mypy: no_implicit_optional = false atualizado.\n", encoding="utf-8")
    else:
        REPORT.write_text("mypy: no_implicit_optional já configurado para false.\n", encoding="utf-8")
    print(REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
