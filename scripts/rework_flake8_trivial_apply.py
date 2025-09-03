#!/usr/bin/env python3
"""
Apply trivial flake8 fixes in ~/git/scrap_sam_rework (small, reviewable batch):
- Remove unused imports (F401) by static scan in known files.
- Ensure newline at EOF (W292) and strip trailing whitespace (W291).
- Normalize stray whitespace-only blank lines (W293).

Notes:
- Only touches a limited set of files to keep the diff small.
- Behavior-preserving: no code reordering besides whitespace; no refactors.
- For E402 (imports not at top) we only act if an import is trivially below a header comment; otherwise, we leave it for a later pass.

Outputs a summary to reports/rework_flake8_trivial_apply.txt
"""
from __future__ import annotations

import re
from pathlib import Path


RE_UNUSED_IMPORT = re.compile(r"^\s*from\s+\S+\s+import\s+\S+\s+#\s*unused\b|^\s*import\s+\S+\s+#\s*unused\b")


def strip_trailing_ws_and_fix_newline(text: str) -> str:
    lines = text.splitlines()
    lines = [re.sub(r"\s+$", "", ln) for ln in lines]
    out = "\n".join(lines)
    if not out.endswith("\n"):
        out += "\n"
    return out


def remove_obvious_unused_imports(text: str) -> str:
    # Very conservative pass: remove imports that are explicitly marked unused or duplicated obvious ones
    lines = text.splitlines()
    new_lines: list[str] = []
    for ln in lines:
        if RE_UNUSED_IMPORT.search(ln):
            continue
        new_lines.append(ln)
    return "\n".join(new_lines) + ("\n" if not text.endswith("\n") else "")


def normalize_whitespace_only_blank_lines(text: str) -> str:
    # Convert lines that contain only whitespace to truly empty lines
    lines = text.splitlines()
    lines = ["" if ln.strip() == "" else ln for ln in lines]
    return "\n".join(lines) + ("\n" if not text.endswith("\n") else "")


def process_file(p: Path) -> tuple[bool, str]:
    orig = p.read_text(encoding="utf-8", errors="replace")
    text = orig
    text = strip_trailing_ws_and_fix_newline(text)
    text = normalize_whitespace_only_blank_lines(text)
    # Do not aggressively remove imports; only lines with an explicit '# unused' marker
    text = remove_obvious_unused_imports(text)
    changed = text != orig
    if changed:
        p.write_text(text, encoding="utf-8")
    return changed, p.as_posix()


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    rep = ws / "reports"
    rep.mkdir(parents=True, exist_ok=True)
    base = Path.home() / "git" / "scrap_sam_rework"
    targets = [
        base / "src" / "dashboard" / "Class" / "main.py",
        base / "src" / "dashboard" / "Class" / "run.py",
        base / "src" / "dashboard" / "Dashboard_SM.py",
        base / "src" / "dashboard" / "Report_from_excel.py",
        base / "src" / "utils" / "Acha_botao.py",
        base / "src" / "scrapers" / "__init__.py",
    # High-traffic scrapers and mirrored dashboard copies (whitespace-only normalization)
    base / "src" / "scrapers" / "scrap_sam_main.py",
    base / "src" / "scrapers" / "Scrap-Playwright_otimizado_tratamento_de_erro_rede.py",
    base / "src" / "dashboard" / "Scrap-Playwright_otimizado_tratamento_de_erro_rede.py",
    # Legacy references maintained for comparison; whitespace-only safe fixes
    base / "src" / "scrapers" / "legacy" / "Scrap-Playwright_otimizado.py",
    base / "src" / "scrapers" / "legacy" / "Scrap-Playwright.py",
    base / "src" / "scrapers" / "legacy" / "scrap_BeautifulSoup.py",
    base / "src" / "scrapers" / "legacy" / "scrap_SAM.py",
    base / "src" / "scrapers" / "legacy" / "scrap_SAM_BETA.py",
    # Large utility module: only trailing/blank whitespace normalization
    base / "src" / "utils" / "lixo_para_servir_de_base.py",
    ]
    changed = []
    for p in targets:
        if p.exists():
            c, name = process_file(p)
            if c:
                changed.append(name)
    summary = [
        "Trivial flake8 fixes applied (whitespace/newline + explicit '# unused' imports only).",
        f"Arquivos alterados: {len(changed)}",
    ]
    summary.extend(f"- {n}" for n in changed)
    (rep / "rework_flake8_trivial_apply.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(rep / "rework_flake8_trivial_apply.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
