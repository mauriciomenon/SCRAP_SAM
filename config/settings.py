import os
from pathlib import Path
import yaml
from typing import Dict, Any, Optional

# Configurações principais do projeto
class Config:
    """Configuração centralizada do projeto SCRAP_SAM."""

    def __init__(self):
        # Caminhos base
        self.PROJECT_ROOT = Path(__file__).parent.parent
        self.SRC_DIR = self.PROJECT_ROOT / "src"
        self.CONFIG_DIR = self.PROJECT_ROOT / "config"
        self.DOWNLOADS_DIR = self.PROJECT_ROOT / "downloads"
        self.DRIVERS_DIR = self.PROJECT_ROOT / "drivers"
        self.LOGS_DIR = self.PROJECT_ROOT / "logs"

        # Criar diretórios necessários
        self.DOWNLOADS_DIR.mkdir(exist_ok=True)
        self.DRIVERS_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)

        # Carregar configurações do YAML
        self._config = self._load_config()

        # Configurações com fallbacks
        self.SCRAPING_TIMEOUT = self._get_config('scraping.timeout', 30)
        self.MAX_RETRIES = self._get_config('scraping.max_retries', 3)
        self.HEADLESS_MODE = self._get_config('scraping.headless', False)
        self.DASHBOARD_PORT = self._get_config('dashboard.port', 8050)
        self.DASHBOARD_HOST = self._get_config('dashboard.host', '127.0.0.1')
        self.LOG_LEVEL = self._get_config('logging.level', 'INFO')

        # URLs
        self.ITAIPU_SAM_URL = self._get_config('urls.sam_login',
            "https://apps.itaipu.gov.br/SAM_SMA_Reports/SSAsExecuted.aspx")

    def _load_config(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo YAML."""
        config_file = self.CONFIG_DIR / "config.yaml"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
                return {}
        return {}

    def _get_config(self, key: str, default: Any = None) -> Any:
        """Obtém valor de configuração com suporte a chaves aninhadas."""
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_driver_path(self, driver_name: str = "geckodriver") -> Path:
        """Retorna o caminho para o driver especificado."""
        import platform
        system = platform.system().lower()

        if system == "windows":
            driver_file = f"{driver_name}.exe"
        else:
            driver_file = driver_name

        return self.DRIVERS_DIR / driver_file

    def get_firefox_path(self) -> Optional[str]:
        """Retorna o caminho para o Firefox."""
        import platform
        system = platform.system().lower()

        if system == "darwin":  # macOS
            return "/Applications/Firefox.app/Contents/MacOS/firefox"
        elif system == "linux":
            return "/usr/bin/firefox"
        else:  # Windows
            firefox_path = self.DRIVERS_DIR / "firefox" / "firefox.exe"
            return str(firefox_path) if firefox_path.exists() else None

    def save_config(self):
        """Salva as configurações atuais no arquivo YAML."""
        config_file = self.CONFIG_DIR / "config.yaml"
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")

# Instância global de configuração
config = Config()
