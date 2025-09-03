# REWORK TODO – SCRAP_SAM

Este documento mantém um checklist ativo e rastreável para o rework em `~/git/scrap_sam_rework` sem afetar o legado.

## Checklist ativo

- [x] Sincronizar log de instruções para o rework (scripts/sync_rework_log.py)
- [ ] Decidir baseline de dependências (preferir versões do rework, validar execução)
- [x] Sanity de código: black/flake8/mypy/pytest (rodar e registrar resultados)
- [ ] Elaborar testes mínimos: config, parsers, utilitários
- [ ] Revisar e unificar configs YAML (apenas ajustes necessários)
- [ ] Smoke test dos scrapers (Selenium e Playwright) e dashboard
- [ ] Registrar outcomes e deltas de comportamento no log

Itens aguardando aprovação (safe/sem mudar comportamento):
- [ ] Aplicar black nos 24 arquivos reportados (reports/rework_black_summary.txt)
- [ ] Corrigir flake8 triviais (F401/E402/W291/W292/W293) em arquivos-chave
- [ ] Adicionar mypy exclude para src/dashboard/bkp/ no pyproject.toml

## Estratégia

1. Trabalhar no rework; não alterar legado a menos que seja documentação/roteiros.
2. Evitar comandos com heredoc; preferir scripts Python e execução direta de binários.
3. Aplicar somente correções necessárias; não alterar comportamento funcional.
4. Documentar cada alteração relevante.

## Comandos úteis (fish)

```fish
# Comparar requirements
python scripts/compare_requirements.py --write-report

# Sincronizar log para o rework
python scripts/sync_rework_log.py
```
