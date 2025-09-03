#!/usr/bin/env python3
"""
Generate README.md and harden .gitignore in ~/git/scrap_sam_rework.

Idempotent: README is fully rewritten; .gitignore merges required patterns if missing.
Writes a short report to SCRAP_SAM/reports/rework_write_readme_gitignore.txt.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import re
from datetime import datetime
from typing import Iterable, Tuple


EXCLUDE_DIRS = {".git", ".venv", "venv", "env", "__pycache__", "logs", "downloads", "drivers", "node_modules", "bkp"}
COUNTABLE_EXTS = {".py", ".toml", ".ini", ".yml", ".yaml", ".md", ".txt"}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def list_files(root: Path) -> set[Path]:
    files: set[Path] = set()
    for p in root.rglob("*"):
        if p.is_dir():
            # Skip excluded dirs
            rel = p.relative_to(root)
            parts = set(rel.parts)
            if parts & EXCLUDE_DIRS:
                continue
            continue
        rel = p.relative_to(root)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        files.add(rel)
    return files


def summarize_diffs(orig: Path, rework: Path) -> Tuple[str, list[str], list[str], list[str]]:
    oset = list_files(orig)
    rset = list_files(rework)
    added = sorted([str(p) for p in (rset - oset)])
    removed = sorted([str(p) for p in (oset - rset)])
    common = sorted([p for p in (rset & oset)])
    modified: list[str] = []
    for rel in common:
        op = orig / rel
        rp = rework / rel
        try:
            if op.stat().st_size != rp.stat().st_size:
                modified.append(str(rel))
            else:
                if op.suffix in COUNTABLE_EXTS or rp.suffix in COUNTABLE_EXTS:
                    if sha256_of(op) != sha256_of(rp):
                        modified.append(str(rel))
        except FileNotFoundError:
            # Race or permissions; skip
            continue
    # Summary text
    summary = (
        f"Arquivos (rework vs original): adicionados={len(added)}, removidos={len(removed)}, modificados={len(modified)}, comuns={len(common)}"
    )
    return summary, added, removed, modified


def maturity_metrics(rework: Path) -> Tuple[str, dict[str, int]]:
    py_files = [p for p in rework.rglob("*.py") if not any(part in EXCLUDE_DIRS for part in p.relative_to(rework).parts)]
    test_files = [p for p in py_files if "tests" in p.parts]
    loc = 0
    defs = 0
    hinted = 0
    for p in py_files:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        loc += sum(1 for _ in text.splitlines())
        for m in re.finditer(r"^\s*def\s+\w+\s*\(.*?\)\s*(:|->)", text, flags=re.MULTILINE | re.DOTALL):
            defs += 1
            sig = m.group(0)
            if "->" in sig or ":" in sig:
                hinted += 1
    ratio = (hinted / defs * 100.0) if defs else 0.0
    metrics = {
        "py_files": len(py_files),
        "test_files": len(test_files),
        "loc": loc,
        "defs": defs,
        "hinted_defs": hinted,
        "hint_ratio_pct": int(ratio),
    }
    summary = (
        f"Maturidade: arquivos .py={metrics['py_files']}, testes={metrics['test_files']}, LOC~{metrics['loc']}, "
        f"funs={metrics['defs']}, anotadas~{metrics['hinted_defs']} (~{metrics['hint_ratio_pct']}%)."
    )
    return summary, metrics


def discover_entry_points(rework: Path) -> list[tuple[str, str]]:
    """Return a list of (module, command) for likely entry points."""
    entries: list[tuple[str, str]] = []
    for path in rework.rglob("*.py"):
        rel = path.relative_to(rework)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        # Consider scripts in src/ and top-level dashboard files
        if rel.parts and (rel.parts[0] == "src" or rel.parts[0] == "src" or rel.parts[0] == "src"):
            # Create module path
            mod = ".".join(rel.with_suffix("").parts)
            if rel.name.lower() in {"scrap_sam_main.py", "dashboard_sm.py", "report_from_excel.py"}:
                entries.append((mod, f"python -m {mod}"))
        elif rel.name in {"Dashboard_SM.py", "Report_from_excel.py"}:
            mod = rel.with_suffix("").name
            entries.append((mod, f"python {rel.as_posix()}"))
    # Deduplicate
    seen = set()
    uniq: list[tuple[str, str]] = []
    for mod, cmd in entries:
        if mod not in seen:
            uniq.append((mod, cmd))
            seen.add(mod)
    return uniq


def read_sanity_summary(scrap_sam_ws: Path) -> str:
    report = scrap_sam_ws / "reports" / "rework_sanity.txt"
    if not report.exists():
        return "Sanity: relatório não encontrado."
    try:
        txt = report.read_text(encoding="utf-8")
    except Exception:
        return "Sanity: relatório não legível."
    # Heuristic extraction
    lines = []
    for line in txt.splitlines():
        if any(k in line.lower() for k in ["black", "flake8", "pytest", "mypy", "syntax", "erros"]):
            lines.append(line.strip())
    if not lines:
        lines = ["Sanity: relatório presente mas sem resumo detectável."]
    return "\n".join(lines)


def generate_readme(scrap_sam_ws: Path, rework: Path) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    orig = scrap_sam_ws
    summary, added, removed, modified = summarize_diffs(orig, rework)

    # Write full diff into rework/reports for reference
    (rework / "reports").mkdir(parents=True, exist_ok=True)
    full_diff = rework / "reports" / "diff_files.txt"
    full_diff.write_text(
        "\n".join(
            ["# Diff de arquivos (gerado)", summary, "", "## Adicionados:"]
            + added
            + ["", "## Removidos:"]
            + removed
            + ["", "## Modificados:"]
            + modified
        )
        + "\n",
        encoding="utf-8",
    )

    matur_txt, metrics = maturity_metrics(rework)
    entries = discover_entry_points(rework)
    sanity = read_sanity_summary(scrap_sam_ws)

    added_preview = "\n".join(f"- {p}" for p in added[:50]) or "(nenhum)"
    removed_preview = "\n".join(f"- {p}" for p in removed[:50]) or "(nenhum)"
    modified_preview = "\n".join(f"- {p}" for p in modified[:50]) or "(nenhum)"

    commands = "\n".join(f"- {m}: `{c}`" for m, c in entries[:10]) or "- Exemplos: `python -m src.scrapers.scrap_sam_main`"

    return f"""
# scrap_sam_rework

Fork de modernização do SCRAP_SAM com foco em configuração e tooling atualizados (flake8/black/mypy/pytest) sem mudanças de comportamento em tempo de execução.

Atualizado: {now}

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
- Ambiente único e compartilhado no repositório: use SEMPRE o venv na raiz em `.venv/` (não crie `env/` ou `venv/` paralelos).
- Reaproveite os arquivos já existentes no repo: `.python-version` (pyenv) e `.envrc` (direnv) estão versionados e devem ser mantidos como fonte de verdade.
- A pasta do venv (`.venv/`) não é versionada; apenas os arquivos de configuração ficam no Git.

## Como rodar

{commands}

- Teste rápido: `pytest -q`.
- Lints: `flake8` e `black --check .`; tipos: `mypy`.

## Diferenças em relação ao SCRAP_SAM (original)

{summary}

Prévia (50 itens máx por seção). Listas completas: `reports/diff_files.txt`.

### Adicionados (rework):
{added_preview}

### Removidos (presentes no original, ausentes no rework):
{removed_preview}

### Modificados (presentes em ambos, conteúdo diferente):
{modified_preview}

## Maturidade e qualidade

- {matur_txt}
- Sanity recente (black/flake8/mypy/pytest):
{sanity}

Presença de tooling/config:
- `.flake8`, `pyproject.toml` (black+mypy), `mypy.ini`, `tests/test_sanity_imports.py`, `log_instrucoes.md` adicionados no rework.
- `.python-version` e `.envrc` versionados para ambiente consistente.

## Troubleshooting

- Playwright no Debian/Ubuntu: use `python -m playwright install --with-deps` para instalar navegadores e dependências do sistema.
- Certificados/SSL no macOS: se `pip` falhar, rode `Install Certificates.command` (vem com o Python.org) ou atualize o Keychain.
- Erro de display no Linux: use `xvfb-run -s "-screen 0 1280x720x24" python -m ...` se não houver display.
- Navegadores headless: confira que o binário foi instalado (`~/.cache/ms-playwright/`). Apague a pasta de cache se corrompida e reinstale.
- Permissões de arquivos: evite clonar dentro de pastas sincronizadas com permissão restrita (ex.: alguns diretórios corporativos) para não afetar playwright/chromium.
- Windows PowerShell: ative o venv com `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` se houver bloqueio de scripts.

## Matriz de versões (recomendadas)

- Python: 3.13.7 (recomendado); 3.11+ provável compatível.
- black: 25.x
- flake8: 7.x
- mypy: 1.17.x
- pytest: 8.x
- pandas: 2.3.x
- selenium: 4.3x.x (no rework: 4.35.0 observado)
- dash: 3.x (no rework)
- plotly: 6.x (no rework)

Notas:
- As versões acima refletem o alvo do rework e o que já foi observado no ambiente. Ajuste conforme o lock/constraints da sua equipe.
- Para tipagem, considere `pandas-stubs`, `types-requests`, `types-PyYAML`, `types-psutil`.

## O que são type stubs (stubs de tipos)?

Type stubs são pacotes que fornecem apenas informações de tipos (arquivos .pyi) para bibliotecas que não têm anotações de tipo completas no próprio código. Eles:

- Não mudam o comportamento em tempo de execução (não executam nada relevante no seu programa);
- Ajudam ferramentas como o mypy a entender melhor as APIs de terceiros (pandas, requests, PyYAML, etc.);
- Reduzem “ruído” de erros falsos de tipagem, deixando os avisos focados no seu código.

Quando usar:
- Se o mypy estiver reportando muitos erros vindos de bibliotecas externas, instale os stubs correspondentes.
- Alternativa: manter `ignore_missing_imports = True` por módulo no mypy (menos preciso), já configurado para alguns casos.

Como instalar (exemplos):
- `pip install pandas-stubs`
- `pip install types-requests types-PyYAML types-psutil`

Observação: instalar stubs é seguro e não altera a execução do projeto; apenas melhora a análise estática de tipos.

## Node (opcional)

Se você utilizar ferramentas Node neste repo:
- Instale Node LTS (nvm, asdf, ou instalador). Mantenha `node_modules/` fora do versionamento.
- Os arquivos `package.json`/lockfiles permanecem versionados. Rode `npm ci` (ou `pnpm i --frozen-lockfile`) quando aplicável.

## Convenções

- Ambientes: mantenha apenas UM venv em `.venv/` na raiz. Não duplique ambientes.
-- Configs: `.python-version` e `.envrc` são a base; ajustes específicos de SO podem ser documentados no `log_instrucoes.md`.

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

    # Build and write README.md
    readme = generate_readme(ws, rework)
    (rework / "README.md").write_text(readme, encoding="utf-8")
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
