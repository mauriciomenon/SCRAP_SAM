# Guia de Sanidade de Código – SCRAP_SAM

Este guia descreve como verificar o projeto rapidamente. Os comandos abaixo são para fish.

## Preparação
- Ative o ambiente do rework (direnv deve ativar automaticamente em `~/git/scrap_sam_rework`).
- Evite heredoc; use scripts Python e comandos simples.

## Ferramentas
- Formatador: `black`
- Linter: `flake8`
- Tipos: `mypy`
- Testes: `pytest`

## Comandos (fish)

```fish
# No repositório legado (para gerar relatórios/roteiros):
python scripts/compare_requirements.py --write-report
python scripts/sync_rework_log.py

# No rework (executar ferramentas no código alvo):
black src tests
flake8 src tests
mypy src tests
pytest -q
```

## Smoke checks (safe, no execution)

Use the non-destructive smoke runner to parse Python files in the rework repo and report syntax errors only:

- Run: python scripts/rework_smoke.py
- Output: reports/rework_smoke.txt

Optionally propose minimal config files in the rework repo (non-destructive: only if missing):

- Run: python scripts/rework_propose_configs.py
- Output: reports/rework_propose_configs.txt

## Notas
- Se o terminal reiniciar (direnv), rode scripts a partir do repositório legado que apontam para o rework.
- Em caso de travas do shell, prefira `python -c` ou pequenos scripts.