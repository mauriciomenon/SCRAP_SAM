# tests/conftest.py
"""Pytest configuration and fixtures."""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_config():
    """Mock configuration for tests."""
    config = Mock()
    config.PROJECT_ROOT = Path("/tmp/test_project")
    config.DOWNLOADS_DIR = Path("/tmp/test_project/downloads")
    config.LOGS_DIR = Path("/tmp/test_project/logs")
    config.SCRAPING_TIMEOUT = 30
    config.MAX_RETRIES = 3
    config.HEADLESS_MODE = True
    return config

@pytest.fixture
def sample_excel_data():
    """Sample Excel data for testing."""
    return {
        "numero_ssa": ["SSA001", "SSA002", "SSA003"],
        "situacao": ["Aberta", "Fechada", "Em Andamento"],
        "setor_executor": ["Manutenção", "Produção", "Qualidade"],
        "prioridade": ["Alta", "Média", "Baixa"]
    }

@pytest.fixture
def mock_webdriver():
    """Mock webdriver for testing."""
    mock_driver = Mock()
    mock_driver.get = Mock()
    mock_driver.find_element = Mock()
    mock_driver.quit = Mock()
    return mock_driver
