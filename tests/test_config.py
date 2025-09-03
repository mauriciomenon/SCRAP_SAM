# tests/test_config.py
"""Tests for configuration system."""

import pytest
import yaml
from pathlib import Path
from unittest.mock import patch, mock_open
from config.settings import Config


class TestConfig:
    """Test cases for Config class."""

    def test_config_initialization(self, temp_dir):
        """Test basic configuration initialization."""
        config = Config()
        assert hasattr(config, 'PROJECT_ROOT')
        assert hasattr(config, 'DOWNLOADS_DIR')
        assert hasattr(config, 'LOGS_DIR')

    def test_config_yaml_loading(self, temp_dir):
        """Test loading configuration from YAML file."""
        # Create a test YAML file
        yaml_content = {
            'scraping': {
                'timeout': 60,
                'max_retries': 5
            },
            'dashboard': {
                'port': 8080
            }
        }

        yaml_file = temp_dir / "config.yaml"
        with open(yaml_file, 'w') as f:
            yaml.dump(yaml_content, f)

        # Test loading
        config = Config()
        config.CONFIG_DIR = temp_dir

        # Mock the file path
        with patch.object(config, 'CONFIG_DIR', temp_dir):
            loaded_config = config._load_config()
            assert loaded_config['scraping']['timeout'] == 60
            assert loaded_config['dashboard']['port'] == 8080

    def test_config_get_method(self, temp_dir):
        """Test _get_config method with nested keys."""
        config = Config()
        config._config = {
            'scraping': {
                'timeout': 45,
                'max_retries': 3
            },
            'dashboard': {
                'host': 'localhost'
            }
        }

        assert config._get_config('scraping.timeout') == 45
        assert config._get_config('dashboard.host') == 'localhost'
        assert config._get_config('nonexistent.key', 'default') == 'default'

    def test_config_fallbacks(self):
        """Test configuration fallbacks."""
        config = Config()
        config._config = {}  # Empty config

        # Test default values
        assert config.SCRAPING_TIMEOUT == 30  # Default from code
        assert config.MAX_RETRIES == 3
        assert config.HEADLESS_MODE is False

    def test_driver_path_detection(self):
        """Test driver path detection for different OS."""
        config = Config()

        with patch('platform.system', return_value='Windows'):
            path = config.get_driver_path('geckodriver')
            assert 'geckodriver.exe' in str(path)

        with patch('platform.system', return_value='Darwin'):
            path = config.get_driver_path('geckodriver')
            assert 'geckodriver' in str(path)
            assert 'geckodriver.exe' not in str(path)

    def test_firefox_path_detection(self):
        """Test Firefox path detection for different OS."""
        config = Config()

        with patch('platform.system', return_value='Darwin'):
            path = config.get_firefox_path()
            assert path is not None
            assert 'Firefox.app' in path

        with patch('platform.system', return_value='Linux'):
            path = config.get_firefox_path()
            assert path is not None
            assert '/usr/bin/firefox' in path

    def test_save_config(self, temp_dir):
        """Test saving configuration to YAML."""
        config = Config()
        config.CONFIG_DIR = temp_dir
        config._config = {
            'test': {
                'value': 123
            }
        }

        config.save_config()

        yaml_file = temp_dir / "config.yaml"
        assert yaml_file.exists()

        with open(yaml_file, 'r') as f:
            saved_config = yaml.safe_load(f)
            assert saved_config['test']['value'] == 123
