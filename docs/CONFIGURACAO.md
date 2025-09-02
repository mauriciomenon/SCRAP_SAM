# Guia de Configuração - SCRAP_SAM

Este documento explica como configurar e personalizar o sistema SCRAP_SAM.

## 📁 Estrutura de Configuração

```
config/
├── settings.py      # Configurações Python (carrega YAML)
├── config.yaml      # Arquivo de configuração principal
└── error_report.json # Relatórios de erro (gerado automaticamente)
```

## ⚙️ Arquivo config.yaml

### Seções Principais

#### 1. Projeto
```yaml
project:
  name: "SCRAP_SAM"
  version: "1.0.0"
  description: "Sistema de scraping e análise de dados do SAM da Itaipu"
```

#### 2. Scraping
```yaml
scraping:
  timeout: 30          # Timeout em segundos para operações
  max_retries: 3       # Número máximo de tentativas
  headless: false      # Executar navegador em modo headless
  wait_time: 10        # Tempo de espera entre operações
  download_dir: "downloads"  # Diretório para downloads
```

#### 3. Drivers
```yaml
drivers:
  geckodriver:
    version: "latest"   # Versão do GeckoDriver
    auto_download: true # Baixar automaticamente se não encontrado
  firefox:
    use_system: true    # Usar Firefox do sistema
    profile: "default"  # Perfil do Firefox a usar
```

#### 4. Dashboard
```yaml
dashboard:
  host: "127.0.0.1"    # Host do servidor
  port: 8050           # Porta do servidor
  debug: true          # Modo debug
  theme: "bootstrap"   # Tema do dashboard
```

#### 5. URLs
```yaml
urls:
  sam_login: "https://apps.itaipu.gov.br/SAM_SMA_Reports/SSAsExecuted.aspx"
  sam_reports: "https://apps.itaipu.gov.br/SAM_SMA_Reports/"
```

#### 6. Logging
```yaml
logging:
  level: "INFO"        # Nível de log (DEBUG, INFO, WARNING, ERROR)
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/scrap_sam.log"
  max_size: 10485760   # Tamanho máximo do arquivo (10MB)
  backup_count: 5      # Número de backups a manter
```

#### 7. Dados
```yaml
data:
  input_format: "excel"    # Formato de entrada
  output_format: "excel"   # Formato de saída
  date_format: "%Y-%m-%d %H:%M:%S"  # Formato de data
  encoding: "utf-8"        # Codificação de caracteres
```

#### 8. Segurança
```yaml
security:
  max_file_size: 100000000  # Tamanho máximo de arquivo (100MB)
  allowed_extensions:       # Extensões permitidas
    - ".xlsx"
    - ".xls"
    - ".csv"
    - ".json"
  timeout_hard: 300         # Timeout absoluto (5 minutos)
```

#### 9. Ambiente
```yaml
environment:
  development: true    # Modo desenvolvimento
  test_mode: false     # Modo teste
  mock_data: false     # Usar dados mock
```

## 🔧 Como Usar as Configurações

### Importando Configurações

```python
from config.settings import config

# Acessar configurações
timeout = config.SCRAPING_TIMEOUT
port = config.DASHBOARD_PORT
url = config.ITAIPU_SAM_URL
```

### Configurações Hierárquicas

```python
# Acessar configurações aninhadas
log_level = config._get_config('logging.level', 'INFO')
max_retries = config._get_config('scraping.max_retries', 3)
```

### Caminhos Dinâmicos

```python
# Caminhos base
project_root = config.PROJECT_ROOT
downloads_dir = config.DOWNLOADS_DIR
logs_dir = config.LOGS_DIR

# Caminhos de drivers
gecko_path = config.get_driver_path('geckodriver')
firefox_path = config.get_firefox_path()
```

## 🌍 Configurações por Ambiente

### Desenvolvimento
```yaml
environment:
  development: true

logging:
  level: "DEBUG"

scraping:
  headless: false
```

### Produção
```yaml
environment:
  development: false

logging:
  level: "WARNING"

scraping:
  headless: true
```

## 🔐 Variáveis de Ambiente

Você pode sobrescrever configurações usando variáveis de ambiente:

```bash
# Linux/Mac
export SCRAP_SAM_SCRAPING_TIMEOUT=60
export SCRAP_SAM_DASHBOARD_PORT=8080
export SCRAP_SAM_DOWNLOAD_DIR="/custom/path"

# Windows
set SCRAP_SAM_SCRAPING_TIMEOUT=60
set SCRAP_SAM_DASHBOARD_PORT=8080
set SCRAP_SAM_DOWNLOAD_DIR=C:\custom\path
```

### Mapeamento de Variáveis

| Variável de Ambiente | Configuração YAML |
|---------------------|-------------------|
| `SCRAP_SAM_SCRAPING_TIMEOUT` | `scraping.timeout` |
| `SCRAP_SAM_MAX_RETRIES` | `scraping.max_retries` |
| `SCRAP_SAM_DASHBOARD_PORT` | `dashboard.port` |
| `SCRAP_SAM_DOWNLOAD_DIR` | `scraping.download_dir` |
| `SCRAP_SAM_LOG_LEVEL` | `logging.level` |

## 📝 Exemplos de Configuração

### Configuração Mínima
```yaml
scraping:
  timeout: 30
  headless: false

dashboard:
  port: 8050

logging:
  level: "INFO"
```

### Configuração Completa para Produção
```yaml
project:
  name: "SCRAP_SAM"
  version: "1.0.0"

scraping:
  timeout: 60
  max_retries: 5
  headless: true
  download_dir: "/data/downloads"

drivers:
  geckodriver:
    auto_download: true

dashboard:
  host: "0.0.0.0"
  port: 80
  debug: false

logging:
  level: "WARNING"
  file: "/var/log/scrap_sam.log"
  max_size: 52428800  # 50MB

security:
  max_file_size: 50000000  # 50MB
  timeout_hard: 600  # 10 minutos

environment:
  development: false
```

## 🔄 Atualização Dinâmica

As configurações podem ser atualizadas em tempo de execução:

```python
from config.settings import config

# Modificar configuração
config._config['scraping']['timeout'] = 60

# Salvar alterações
config.save_config()
```

## 🚨 Validação de Configuração

O sistema valida automaticamente as configurações na inicialização:

- Verifica existência de diretórios necessários
- Valida formatos de URL
- Verifica compatibilidade de versões
- Alerta sobre configurações potencialmente problemáticas

## 📊 Monitoramento

### Logs de Configuração

O sistema gera logs detalhados sobre:
- Carregamento de configurações
- Valores padrão utilizados
- Erros de validação
- Alterações dinâmicas

### Métricas

```python
# Verificar status da configuração
print(f"Configuração carregada: {config._config is not None}")
print(f"Timeout atual: {config.SCRAPING_TIMEOUT}")
print(f"Porta do dashboard: {config.DASHBOARD_PORT}")
```

## 🛠️ Troubleshooting

### Problema: Configuração não carrega
```
Verifique se o arquivo config/config.yaml existe
Verifique permissões de leitura
Verifique sintaxe YAML
```

### Problema: Configurações não aplicam
```
Reinicie a aplicação após alterar config.yaml
Verifique se há variáveis de ambiente sobrescrevendo
Confirme que o caminho do arquivo está correto
```

### Problema: Erro de validação
```
Verifique os valores permitidos para cada configuração
Confirme que os caminhos existem
Valide formatos de URL e números
```
