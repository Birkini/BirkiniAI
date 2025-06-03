import os
import json
import yaml
from typing import Any, Optional, Dict


class ConfigManager:
    """
    Central configuration management class for Birkini.
    Loads config from JSON/YAML files and overrides with environment variables.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_data: Dict[str, Any] = {}
        self.load_from_file(config_path)
        self.override_with_env_vars()

    def load_from_file(self, config_path: Optional[str]) -> None:
        """
        Loads configuration from a JSON or YAML file if provided.
        """
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as file:
                    if config_path.endswith('.json'):
                        self.config_data = json.load(file)
                    elif config_path.endswith(('.yaml', '.yml')):
                        self.config_data = yaml.safe_load(file)
            except Exception as e:
                raise RuntimeError(f"Failed to load configuration file: {e}")

    def override_with_env_vars(self) -> None:
        """
        Overrides config values with environment variables if they exist.
        Keys are expected to be in uppercase with underscores (e.g., DATABASE_URL).
        """
        for key in self.config_data:
            env_value = os.getenv(key.upper())
            if env_value is not None:
                self.config_data[key] = env_value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value.
        """
        return self.config_data.get(key, default)

    def all(self) -> Dict[str, Any]:
        """
        Returns the entire configuration dictionary.
        """
        return self.config_data

    def print_config(self) -> None:
        """
        Debug method to print current config values.
        """
        print("Current Configuration:")
        for key, value in self.config_data.items():
            print(f"{key}: {value}")


# Example usage
if __name__ == "__main__":
    config_path = os.getenv("BIRKINI_CONFIG_PATH", "config.yaml")
    config = ConfigManager(config_path=config_path)

    # Print all config
    config.print_config()

    # Access individual value
    db_url = config.get("database_url")
    print(f"Database URL: {db_url}")
