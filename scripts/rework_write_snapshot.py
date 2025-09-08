#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from datetime import datetime


def main() -> int:
    rework = Path.home() / "git" / "scrap_sam_rework"
    if not rework.exists():
        print(f"Rework repo não encontrado: {rework}")
        return 1
    today = datetime.now().strftime("%Y%m%d")
    content = f"""
# Session Snapshot – {datetime.now():%Y-%m-%d} (rework)

Repo: scrap_sam_rework

## Estado atual
- Configs atualizadas (flake8/black/mypy/pytest) sem mudanças de lógica.
- README reforçado com seção de “type stubs”: o que são, quando/como instalar; não alteram runtime.
- .gitignore endurecido; `.python-version` e `.envrc` versionados; usar apenas `.venv/` na raiz.

## Qualidade (último sanity)
- black: PASS
- pytest: PASS (7/7)
- flake8: vários avisos (unused imports, F541, espaçamento) — esperado.
- mypy: 256 erros em 17 arquivos (foco no código do projeto; terceiros suprimidos onde pertinente).

## Próximos passos (rework, opcional)
- Stubs (seguro):
  - `pip install pandas-stubs types-requests types-PyYAML types-psutil`
  - Rodar sanity novamente.
- Lint-only sweep (sem alterar comportamento): remover imports não usados, corrigir F541/whitespace.

## Entradas úteis
- Executar: `python -m src.scrapers.scrap_sam_main`
- Testar: `pytest -q`
- Lints: `flake8`, `black --check .`, `mypy`

---
Gerado para retomada pós-restart. Este snapshot está apenas no rework (por solicitação).
"""
    out_dir = rework / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"session_snapshot_{today}.md"
    out_file.write_text(content.strip() + "\n", encoding="utf-8")
    print(out_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
