"""
Configuration management for Seedance Video Generation skill.

Handles configuration loading from multiple sources with proper fallback order:
1. Environment variables (ARK_API_KEY)
2. ~/.config/seedance/config.json
3. ~/.seedance.json
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for Seedance API."""

    # Default configuration values
    DEFAULT_CONFIG = {
        "ark_api_key": "",
        "region": "cn-beijing",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "timeout": 300,
        "poll_interval": 5,
    }

    def __init__(self, environment: str = "default"):
        """
        Initialize configuration.

        Args:
            environment: Environment name (default, development, production)
        """
        self.environment = environment
        self._config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from files and environment variables."""
        # Try loading from ~/.config/seedance/config.json
        config_path = Path.home() / ".config" / "seedance" / "config.json"
        if config_path.exists():
            self._load_from_file(config_path)

        # Try loading from ~/.seedance.json (fallback)
        fallback_path = Path.home() / ".seedance.json"
        if fallback_path.exists() and not config_path.exists():
            self._load_from_file(fallback_path)

        # Override with environment variables
        self._load_from_env()

    def _load_from_file(self, path: Path) -> None:
        """Load configuration from a JSON file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                file_config = json.load(f)

            # Get environment-specific config if available
            if self.environment in file_config:
                env_config = file_config[self.environment]
                self._config.update(
                    {
                        k: v
                        for k, v in env_config.items()
                        if v is not None and v != ""
                    }
                )
            # Also check for "default" environment as fallback
            elif "default" in file_config:
                default_config = file_config["default"]
                self._config.update(
                    {
                        k: v
                        for k, v in default_config.items()
                        if v is not None and v != ""
                    }
                )
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load config from {path}: {e}")

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # Map environment variable names to config keys
        env_mappings = {
            "ARK_API_KEY": "ark_api_key",
            "SEEDANCE_REGION": "region",
            "SEEDANCE_BASE_URL": "base_url",
            "SEEDANCE_TIMEOUT": "timeout",
            "SEEDANCE_POLL_INTERVAL": "poll_interval",
        }

        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                # Convert numeric values
                if config_key in ("timeout", "poll_interval"):
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                self._config[config_key] = value

    @property
    def ark_api_key(self) -> str:
        """Get the ARK API key."""
        return self._config.get("ark_api_key", "")

    @property
    def region(self) -> str:
        """Get the region."""
        return self._config.get("region", "cn-beijing")

    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return self._config.get("base_url", "https://ark.cn-beijing.volces.com/api/v3")

    @property
    def timeout(self) -> int:
        """Get the timeout in seconds."""
        return self._config.get("timeout", 300)

    @property
    def poll_interval(self) -> int:
        """Get the poll interval in seconds."""
        return self._config.get("poll_interval", 5)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate that required configuration is present.

        Returns:
            (is_valid, error_message)
        """
        if not self.ark_api_key:
            return (
                False,
                "ARK_API_KEY not configured. Set it via environment variable or config file.",
            )
        return True, None


# Default config instance
_default_config: Optional[Config] = None


def get_config(environment: str = "default") -> Config:
    """Get or create the configuration instance."""
    global _default_config
    if _default_config is None:
        _default_config = Config(environment)
    return _default_config
