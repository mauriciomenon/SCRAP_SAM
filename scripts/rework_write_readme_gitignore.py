#!/usr/bin/env python3
"""
Generate README.md and harden .gitignore in ~/git/scrap_sam_rework.

Idempotent: README is fully rewritten; .gitignore merges required patterns if missing.
Writes a short report to SCRAP_SAM/reports/rework_write_readme_gitignore.txt.
"""
from __future__ import annotations

from pathlib import Path


README = """# scrap_sam_rework

Fork de modernização do SCRAP_SAM com foco em configuração e tooling atualizados (flake8/black/mypy/pytest) sem mudanças de comportamento em tempo de execução.

## Visão geral

- Compatibilidade: mesmas funcionalidades do projeto original, sem refatorações de lógica.
- Atualizações: padronização de `.flake8`, `pyproject.toml` (black/mypy), `mypy.ini`, e teste mínimo de import.
- Tipagem: redução de ruído com overrides de mypy; stubs de terceiros recomendados conforme necessário.

## Requisitos

- Python 3.13 (recomendado). Projetos secundários podem operar em 3.11+ com ajustes.
- pip >= 24, virtualenv/venv.
- Playwright para Python (browsers via `playwright install`).
- Node.js: somente se você usar ferramentas Node adicionais; o Playwright para Python não requer Node.

## Setup rápido

### macOS
- Instalar Xcode CLT e Homebrew.
- Instalar Python 3.13 (pyenv recomendado):
  - `brew install pyenv` e depois `pyenv install 3.13.7`
  - `pyenv local 3.13.7` (este repo rastreia `.python-version`).
- Criar venv: `python -m venv .venv && source .venv/bin/activate`
- Atualizar pip e instalar deps: `pip install -U pip && pip install -r requirements.txt`
- Playwright: `python -m playwright install` (e no Linux: `python -m playwright install --with-deps`).

### Debian/Ubuntu
- Dependências de build (se usar pyenv): `sudo apt-get update && sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev`
- Instalar pyenv (ou use Python do sistema 3.13 se disponível).
- Criar venv: `python3 -m venv .venv && source .venv/bin/activate`
- Instalar deps: `pip install -U pip && pip install -r requirements.txt`
- Playwright: `python -m playwright install --with-deps`

### Windows
- Instalar Python 3.13 (ou pyenv-win se preferir). Com pyenv-win: `pyenv install 3.13.7` e `pyenv local 3.13.7`.
- Criar venv: `py -3.13 -m venv .venv` e ativar: `\\.venv\\Scripts\\activate`.
- Instalar deps: `python -m pip install -U pip && pip install -r requirements.txt`
- Playwright: `python -m playwright install`

Notas:
- Este repo mantém `.python-version` (pyenv) e `.envrc` (direnv) versionados para padronizar o ambiente. A pasta do venv (`.venv/`) não é versionada.

## Como rodar

- Ative o venv e execute seus scripts usuais (ex.: `python -m src.scrapers.scrap_sam_main`).
- Teste rápido: `pytest -q`.
- Lints: `flake8` e `black --check .`; tipos: `mypy`.

## Diferenças em relação ao SCRAP_SAM (original)

Arquivos e estrutura:
- Adicionados: `.flake8`, `pyproject.toml` (black+mypy), `mypy.ini`, `tests/test_sanity_imports.py`, `log_instrucoes.md`.
- Mantidos: módulos de runtime e scripts originais, sem alteração de comportamento.

Versões e tooling:
- Python alvo: 3.13.
- Ferramentas: black 25.x, flake8 7.x, mypy 1.17.x, pytest 8.x (conforme ambiente).
- Stubs opcionais sugeridos: `pandas-stubs`, `types-requests`, `types-PyYAML`, `types-psutil`.

Implementações:
- Ajustes apenas em configuração e limpeza segura (espaços/`unused imports` pontuais). Nenhuma alteração de lógica de execução.

## Node (opcional)

Se você utilizar ferramentas Node neste repo:
- Instale Node LTS (nvm, asdf, ou instalador). Mantenha `node_modules/` fora do versionamento.
- Os arquivos `package.json`/lockfiles permanecem versionados. Rode `npm ci` (ou `pnpm i --frozen-lockfile`) quando aplicável.

## Convenções

- Ambientes: `.python-version` e `.envrc` são versionados para manter paridade entre Windows/macOS/Debian. Ajustes específicos de SO podem ser documentados no `log_instrucoes.md`.
- Formatação: `black` (linhas 88). Lints: `flake8` com ignorados E203,W503,E402,E501,E722. Tipos: `mypy` com overrides por terceiro.
"""


GITIGNORE_ADD = [
    "# Python",
    "__pycache__/",
    "*.py[cod]",
    "*.egg-info/",
    "build/",
    "dist/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    "*.coverage",
    ".coverage*",
    "coverage.xml",
    "htmlcov/",
    "# Virtual envs",
    ".venv/",
    "venv/",
    "env/",
    "# OS",
    ".DS_Store",
    "Thumbs.db",
    "# pip caches (se existirem locais no repo)",
    ".pip/",
    "**/.pip/",
    "pip-wheel-metadata/",
    "# Node (opcional)",
    "node_modules/",
    ".pnpm-store/",
    "# Direnv cache",
    ".direnv/",
]


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    reports = ws / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    out = reports / "rework_write_readme_gitignore.txt"

    rework = Path.home() / "git" / "scrap_sam_rework"
    lines: list[str] = []
    if not rework.exists():
        out.write_text(f"Rework repo não encontrado: {rework}\n", encoding="utf-8")
        print(out)
        return 1

    # Write README.md
    (rework / "README.md").write_text(README, encoding="utf-8")
    lines.append("README.md escrito/atualizado.")

    # Merge .gitignore
    gi_path = rework / ".gitignore"
    existing = []
    if gi_path.exists():
        existing = gi_path.read_text(encoding="utf-8").splitlines()
    merged = list(existing)
    for pat in GITIGNORE_ADD:
        if pat not in merged:
            merged.append(pat)
    # Garantir que arquivos de config fiquem versionados
    footer = [
        "",
        "# Mantidos no repo (não ignore):",
        "!/.python-version",
        "!/.envrc",
    ]
    for pat in footer:
        if pat not in merged:
            merged.append(pat)
    gi_path.write_text("\n".join(merged) + "\n", encoding="utf-8")
    lines.append(".gitignore mesclado/atualizado.")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
