# SCRAP_SAM

Sistema de scraping e análise de dados do SAM (Sistema de Administração de Manutenção) da Itaipu Binacional.

## 📋 Descrição

Este projeto automatiza a coleta e análise de dados de SSAs (Solicitações de Serviço de Atividades) do sistema SAM da Itaipu, fornecendo dashboards interativos para visualização e análise dos dados.

## 🏗️ Estrutura do Projeto

```
SCRAP_SAM/
├── src/                    # Código fonte
│   ├── scrapers/          # Scripts de scraping
│   │   ├── scrap_SAM.py              # Scraper principal (Selenium)
│   │   ├── scrap_SAM_BETA.py         # Versão beta do scraper
│   │   ├── Scrap-Playwright.py       # Scraper usando Playwright
│   │   └── scrap_BeautifulSoup.py    # Parser HTML com BeautifulSoup
│   ├── dashboard/         # Interface web e visualizações
│   │   └── Dashboard_SM.py           # Dashboard principal
│   └── utils/             # Utilitários e helpers
│       ├── scrap_installer.py        # Instalador de dependências
│       └── Report_from_excel.py      # Utilitários de relatório
├── config/                # Configurações
│   ├── settings.py        # Configurações Python
│   ├── config.yaml        # Configurações YAML
│   └── error_report.json  # Relatórios de erro
├── tests/                 # Testes
├── docs/                  # Documentação
├── downloads/             # Arquivos baixados
├── drivers/               # Web drivers
└── logs/                  # Arquivos de log
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- Firefox ou Chrome instalado
- Git

### Passos de Instalação

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd SCRAP_SAM
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Instale os navegadores do Playwright:**
```bash
playwright install
```

5. **Configure os drivers:**
   - Baixe o GeckoDriver (para Firefox) ou ChromeDriver
   - Coloque na pasta `drivers/`

## ⚙️ Configuração

### Arquivo de Configuração

Edite o arquivo `config/config.yaml` para personalizar as configurações:

```yaml
scraping:
  timeout: 30
  max_retries: 3
  headless: false

dashboard:
  host: "127.0.0.1"
  port: 8050

logging:
  level: "INFO"
```

### Variáveis de Ambiente

Você pode usar variáveis de ambiente para configurações sensíveis:

```bash
export SCRAP_SAM_DOWNLOAD_DIR="/caminho/para/downloads"
export SCRAP_SAM_LOG_LEVEL="DEBUG"
```

## 📖 Uso

### Modo de Desenvolvimento

1. **Executar scraper:**
```bash
python src/scrapers/scrap_SAM.py
```

2. **Executar dashboard:**
```bash
python src/dashboard/Dashboard_SM.py
```

3. **Executar com configurações customizadas:**
```bash
python -c "from config.settings import config; print(config.SCRAPING_TIMEOUT)"
```

### Scripts Disponíveis

| Script | Descrição | Comando |
|--------|-----------|---------|
| `scrap_SAM.py` | Scraper principal usando Selenium | `python src/scrapers/scrap_SAM.py` |
| `Scrap-Playwright.py` | Scraper usando Playwright | `python src/scrapers/Scrap-Playwright.py` |
| `scrap_BeautifulSoup.py` | Parser HTML simples | `python src/scrapers/scrap_BeautifulSoup.py` |
| `Dashboard_SM.py` | Dashboard interativo | `python src/dashboard/Dashboard_SM.py` |

## 🔧 Desenvolvimento

### Estrutura de Código

- **`src/scrapers/`**: Contém todos os scripts de scraping
- **`src/dashboard/`**: Interface web e componentes visuais
- **`src/utils/`**: Funções utilitárias e helpers
- **`config/`**: Configurações centralizadas
- **`tests/`**: Testes unitários e de integração

### Adicionando Novos Scrapers

1. Crie um novo arquivo em `src/scrapers/`
2. Importe as configurações: `from config.settings import config`
3. Use os caminhos padronizados do config
4. Adicione tratamento de erros adequado

### Exemplo de Scraper

```python
from config.settings import config
from selenium import webdriver

def meu_scraper():
    driver_path = config.get_driver_path()
    download_dir = config.DOWNLOADS_DIR

    options = webdriver.FirefoxOptions()
    options.set_preference("browser.download.dir", str(download_dir))

    driver = webdriver.Firefox(executable_path=str(driver_path), options=options)
    # ... resto do código
```

## 🧪 Testes

```bash
# Executar todos os testes
python -m pytest tests/

# Executar testes específicos
python -m pytest tests/test_scrapers.py

# Com cobertura
python -m pytest --cov=src tests/
```

## 📊 Logging

Os logs são salvos em `logs/` com rotação automática:

- `scrap_sam.log`: Log principal
- `geckodriver.log`: Log do driver
- `dashboard_activity.log`: Atividades do dashboard

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de driver não encontrado:**
   - Verifique se o GeckoDriver/ChromeDriver está na pasta `drivers/`
   - Certifique-se de que tem permissões de execução

2. **Erro de Firefox não encontrado:**
   - Instale o Firefox ou configure o caminho em `config.yaml`

3. **Erro de importação:**
   - Execute: `pip install -r requirements.txt`
   - Verifique se está no ambiente virtual correto

4. **Erro de permissão:**
   - Execute: `chmod +x drivers/geckodriver`

### Debug Mode

Para modo debug, edite `config/config.yaml`:

```yaml
logging:
  level: "DEBUG"

scraping:
  headless: false
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- Use type hints
- Mantenha compatibilidade cross-platform
- Adicione docstrings
- Escreva testes para novas funcionalidades

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## ⚠️ Avisos Importantes

- **Uso Autorizado**: Este projeto é destinado apenas para uso interno da Itaipu Binacional
- **Termos de Serviço**: Respeite os termos de serviço do sistema SAM
- **Responsabilidade**: Use com responsabilidade para evitar sobrecarga do sistema
- **Dados Sensíveis**: Não commite dados sensíveis ou credenciais

## 📞 Suporte

Para suporte técnico, entre em contato com a equipe de desenvolvimento ou abra uma issue no repositório.
