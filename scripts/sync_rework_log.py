#!/usr/bin/env python3
"""
Sync the instruction log into ~/git/scrap_sam_rework safely (no heredoc).

Usage:
  python scripts/sync_rework_log.py

This will read docs/LOG_INSTRUCOES_REWORK.md from the current repo and
write it to ~/git/scrap_sam_rework/log_instrucoes.md.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> int:
    base = Path(__file__).resolve().parents[1]
    src_file = base / "docs" / "LOG_INSTRUCOES_REWORK.md"
    dst_file = Path.home() / "git" / "scrap_sam_rework" / "log_instrucoes.md"

    if not src_file.exists():
        print(f"Fonte não encontrada: {src_file}")
        return 1

    dst_file.parent.mkdir(parents=True, exist_ok=True)
    content = src_file.read_text(encoding="utf-8")
    # Pequeno cabeçalho no destino para indicar origem
    banner = (
        "<!-- Arquivo gerado a partir de SCRAP_SAM/docs/LOG_INSTRUCOES_REWORK.md -->\n\n"
    )
    dst_file.write_text(banner + content, encoding="utf-8")
    print(f"Log sincronizado em: {dst_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
