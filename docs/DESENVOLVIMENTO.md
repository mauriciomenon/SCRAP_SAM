# Guia de Desenvolvimento - SCRAP_SAM

Este documento fornece diretrizes para desenvolvimento, contribuição e manutenção do projeto SCRAP_SAM.

## 🏗️ Arquitetura do Sistema

### Visão Geral

O SCRAP_SAM é dividido em módulos independentes:

```
├── Scrapers (src/scrapers/)     # Coleta de dados
├── Dashboard (src/dashboard/)   # Visualização
├── Utils (src/utils/)          # Utilitários
├── Config (config/)            # Configurações
└── Tests (tests/)              # Validação
```

### Princípios de Design

1. **Separação de Responsabilidades**: Cada módulo tem uma função específica
2. **Configuração Centralizada**: Todas as configurações em `config/`
3. **Cross-platform**: Compatível com Windows, macOS e Linux
4. **Tratamento de Erros**: Logging abrangente e recuperação de falhas
5. **Testabilidade**: Código estruturado para testes unitários

## 💻 Desenvolvimento

### Configuração do Ambiente

1. **Clone e setup:**
```bash
git clone <repository>
cd SCRAP_SAM
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
playwright install
```

2. **Configuração de desenvolvimento:**
```yaml
# config/config.yaml
environment:
  development: true

logging:
  level: "DEBUG"

scraping:
  headless: false
```

### Estrutura de Código

#### Padrões de Nomeação

- **Arquivos**: `snake_case.py`
- **Classes**: `CamelCase`
- **Funções/Métodos**: `snake_case`
- **Constantes**: `UPPER_CASE`
- **Variáveis**: `snake_case`

#### Exemplo de Estrutura

```python
# src/scrapers/base_scraper.py
import logging
from abc import ABC, abstractmethod
from config.settings import config

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Classe base para todos os scrapers."""

    def __init__(self):
        self.timeout = config.SCRAPING_TIMEOUT
        self.download_dir = config.DOWNLOADS_DIR
        self.logger = logger

    @abstractmethod
    def scrape(self, url: str) -> dict:
        """Método abstrato para scraping."""
        pass

    def setup_driver(self):
        """Configura o webdriver."""
        # Implementação comum
        pass
```

### Tratamento de Erros

#### Padrões de Exceção

```python
class ScraperError(Exception):
    """Erro base do scraper."""
    pass

class DriverNotFoundError(ScraperError):
    """Driver não encontrado."""
    pass

class TimeoutError(ScraperError):
    """Timeout na operação."""
    pass

# Uso
try:
    result = scraper.scrape(url)
except DriverNotFoundError as e:
    logger.error(f"Driver não encontrado: {e}")
    # Tratamento específico
except TimeoutError as e:
    logger.warning(f"Timeout: {e}")
    # Retry logic
except ScraperError as e:
    logger.error(f"Erro no scraper: {e}")
    # Tratamento genérico
```

#### Logging Estruturado

```python
import logging
from config.settings import config

# Configuração do logger
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config._get_config('logging.format'),
    handlers=[
        logging.FileHandler(config._get_config('logging.file')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Uso
logger.debug("Iniciando scraping")
logger.info("Página carregada com sucesso")
logger.warning("Elemento não encontrado, tentando alternativa")
logger.error("Falha crítica no scraping")
```

## 🧪 Testes

### Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py          # Configurações de teste
├── test_scrapers.py     # Testes de scrapers
├── test_dashboard.py    # Testes de dashboard
├── test_utils.py        # Testes de utilitários
└── fixtures/           # Dados de teste
```

### Exemplo de Teste

```python
# tests/test_scrapers.py
import pytest
from unittest.mock import Mock, patch
from src.scrapers.scrap_SAM import SamScraper

class TestSamScraper:

    @pytest.fixture
    def scraper(self):
        return SamScraper()

    @patch('selenium.webdriver.Firefox')
    def test_scraper_initialization(self, mock_driver, scraper):
        """Testa inicialização do scraper."""
        assert scraper.timeout == 30
        assert scraper.download_dir.exists()

    @patch('selenium.webdriver.Firefox')
    def test_successful_scrape(self, mock_driver, scraper):
        """Testa scraping bem-sucedido."""
        mock_driver_instance = Mock()
        mock_driver.return_value = mock_driver_instance

        result = scraper.scrape("https://example.com")

        assert result is not None
        mock_driver_instance.get.assert_called_once()

    def test_error_handling(self, scraper):
        """Testa tratamento de erros."""
        with pytest.raises(ScraperError):
            scraper.scrape("invalid-url")
```

### Executando Testes

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_scrapers.py

# Com cobertura
pytest --cov=src --cov-report=html

# Testes de integração
pytest -m integration

# Debug mode
pytest -v -s
```

### Fixtures e Mocks

```python
# tests/conftest.py
import pytest
from config.settings import config

@pytest.fixture
def sample_data():
    """Dados de exemplo para testes."""
    return {
        "url": "https://example.com",
        "expected_result": {"status": "success"}
    }

@pytest.fixture
def mock_driver():
    """Mock do webdriver."""
    with patch('selenium.webdriver.Firefox') as mock:
        yield mock
```

## 📦 Versionamento

### Padrão de Versionamento

Usamos [Semantic Versioning](https://semver.org/):

- **MAJOR**: Mudanças incompatíveis
- **MINOR**: Novas funcionalidades compatíveis
- **PATCH**: Correções de bug

### Branches

- `main`: Branch principal (produção)
- `develop`: Branch de desenvolvimento
- `feature/*`: Novas funcionalidades
- `bugfix/*`: Correções
- `release/*`: Preparação para release

### Workflow Git

```bash
# Desenvolvimento
git checkout develop
git pull origin develop
git checkout -b feature/nova-funcionalidade

# Commits
git add .
git commit -m "feat: adiciona nova funcionalidade"

# Merge
git checkout develop
git merge feature/nova-funcionalidade
git push origin develop

# Release
git checkout -b release/v1.1.0
# Ajustes finais
git checkout main
git merge release/v1.1.0
git tag v1.1.0
git push origin main --tags
```

## 🚀 Deploy

### Ambiente de Produção

1. **Configuração:**
```yaml
environment:
  development: false

scraping:
  headless: true

logging:
  level: "WARNING"
```

2. **Build:**
```bash
# Criar distribuição
python setup.py sdist bdist_wheel

# Ou usar Docker
docker build -t scrap-sam .
```

3. **Deploy:**
```bash
# Instalar em produção
pip install dist/scrap_sam-1.0.0.tar.gz

# Executar
python -m scrap_sam
```

## 🔒 Segurança

### Boas Práticas

1. **Nunca commite credenciais**
2. **Use variáveis de ambiente para secrets**
3. **Valide inputs de usuário**
4. **Limite acesso a arquivos**
5. **Monitore logs de segurança**

### Checklist de Segurança

- [ ] Credenciais não hardcoded
- [ ] Validação de inputs
- [ ] Sanitização de dados
- [ ] Controle de acesso
- [ ] Logs de auditoria
- [ ] Atualização de dependências

## 📊 Monitoramento

### Métricas a Monitorar

- Taxa de sucesso de scraping
- Tempo de resposta
- Uso de memória/CPU
- Erros por tipo
- Volume de dados processados

### Alertas

```python
# Exemplo de monitoramento
def monitor_scraping():
    success_rate = calculate_success_rate()
    if success_rate < 0.8:  # 80%
        alert_team("Taxa de sucesso baixa")

    response_time = get_average_response_time()
    if response_time > 30:  # 30 segundos
        alert_team("Tempo de resposta alto")
```

## 🤝 Contribuição

### Processo de Contribuição

1. **Fork** o projeto
2. **Clone** seu fork: `git clone https://github.com/YOUR_USERNAME/SCRAP_SAM.git`
3. **Crie** uma branch: `git checkout -b feature/AmazingFeature`
4. **Commit** suas mudanças: `git commit -m 'Add some AmazingFeature'`
5. **Push** para a branch: `git push origin feature/AmazingFeature`
6. **Abra** um Pull Request

### Padrões de Commit

```
feat: nova funcionalidade
fix: correção de bug
docs: atualização de documentação
style: formatação, linting
refactor: refatoração de código
test: adição ou correção de testes
chore: tarefas de manutenção
```

### Code Review

#### Checklist do Reviewer

- [ ] Código segue padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Não há vulnerabilidades de segurança
- [ ] Performance não foi degradada
- [ ] Código é legível e bem comentado

#### Checklist do Autor

- [ ] Todos os testes passam
- [ ] Linting sem erros
- [ ] Documentação atualizada
- [ ] Código revisado
- [ ] Commits seguem padrão
- [ ] Branch atualizada com main

## 📚 Recursos Adicionais

### Documentação Técnica

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Playwright Documentation](https://playwright.dev/python/docs/intro)
- [Dash Documentation](https://dash.plotly.com/)
- [BeautifulSoup Documentation](https://beautiful-soup-4.readthedocs.io/)

### Ferramentas de Desenvolvimento

- **IDE**: VSCode com extensões Python
- **Linting**: flake8, black
- **Testing**: pytest, coverage
- **Versionamento**: git, GitHub
- **CI/CD**: GitHub Actions

### Comunidade

- **Issues**: Para bugs e solicitações
- **Discussions**: Para perguntas gerais
- **Wiki**: Para documentação avançada
- **Discord/Slack**: Para comunicação em tempo real
