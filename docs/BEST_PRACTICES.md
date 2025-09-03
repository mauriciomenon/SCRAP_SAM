# Boas Práticas – SCRAP_SAM

## Ambiente
- Use `direnv` e `.venv` no rework para isolar dependências.
- Evite heredoc (`<< EOF`) no terminal integrado; prefira scripts Python.
- Em fish/zsh, rode comandos simples e não interativos quando possível.

## Git/Branches
- Manter `main` estável. Rework no repositório `scrap_sam_rework` separado.
- Commits atômicos e mensagens descritivas (Português ok; foque em “o que/por quê”).

## Estilo de código
- Formatação: `black`. Lint: `flake8`. Tipos: `mypy` (quando aplicável).
- Nomes claros, funções pequenas, tratamento de erros explícito.
- Evite efeitos colaterais em import (use guarda `if __name__ == "__main__"`).

## Testes
- Use `pytest` com casos mínimos e asserts claros.
- Testes de unidade para utilitários e parsers, smoke tests para scrapers.

## Logs e Documentação
- Atualize `docs/LOG_INSTRUCOES_REWORK.md` e sincronize com o rework.
- Registre mudanças de comportamento e decisões de versão.
