import os
from pathlib import Path

# Configurações principais do projeto
class Config:
    """Configuração centralizada do projeto SCRAP_SAM."""

    # Caminhos base
    PROJECT_ROOT = Path(__file__).parent.parent
    SRC_DIR = PROJECT_ROOT / "src"
    CONFIG_DIR = PROJECT_ROOT / "config"
    DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
    DRIVERS_DIR = PROJECT_ROOT / "drivers"
    LOGS_DIR = PROJECT_ROOT / "logs"

    # Criar diretórios necessários
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    DRIVERS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)

    # Configurações de scraping
    SCRAPING_TIMEOUT = 30
    MAX_RETRIES = 3
    HEADLESS_MODE = False

    # Configurações do dashboard
    DASHBOARD_PORT = 8050
    DASHBOARD_HOST = "127.0.0.1"

    # URLs
    ITAIPU_SAM_URL = "https://apps.itaipu.gov.br/SAM_SMA_Reports/SSAsExecuted.aspx"

    @classmethod
    def get_driver_path(cls, driver_name="geckodriver"):
        """Retorna o caminho para o driver especificado."""
        import platform
        system = platform.system().lower()

        if system == "windows":
            driver_file = f"{driver_name}.exe"
        else:
            driver_file = driver_name

        return cls.DRIVERS_DIR / driver_file

    @classmethod
    def get_firefox_path(cls):
        """Retorna o caminho para o Firefox."""
        import platform
        system = platform.system().lower()

        if system == "darwin":  # macOS
            return "/Applications/Firefox.app/Contents/MacOS/firefox"
        elif system == "linux":
            return "/usr/bin/firefox"
        else:  # Windows
            return cls.DRIVERS_DIR / "firefox" / "firefox.exe"

# Instância global de configuração
config = Config()
