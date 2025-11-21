"""
Configuration loader for 1Security
"""
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Loads and validates YAML configuration."""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        
    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate required fields
        self._validate(config)
        
        return config
    
    def _validate(self, config: Dict[str, Any]) -> None:
        """Validate configuration structure."""
        if not config:
            raise ValueError("Configuration is empty")
        
        if "tools" not in config:
            raise ValueError("Configuration must contain 'tools' section")
        
        # Check at least one tool is enabled
        tools = config.get("tools", {})
        enabled_tools = [name for name, cfg in tools.items() if cfg.get("enabled", False)]
        
        if not enabled_tools:
            raise ValueError("At least one tool must be enabled")
        
        # Validate each enabled tool has a runner
        for tool_name, tool_cfg in tools.items():
            if tool_cfg.get("enabled", False):
                if "runner" not in tool_cfg:
                    raise ValueError(f"Tool '{tool_name}' is enabled but has no 'runner' specified")

