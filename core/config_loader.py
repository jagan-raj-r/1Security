"""
Configuration loader for 1Security
"""
import yaml
from pathlib import Path
from typing import Dict, Any, List
from core.logger import get_logger

logger = get_logger(__name__)


class ConfigLoader:
    """Loads and validates YAML configuration."""
    
    # Valid configuration values
    VALID_FORMATS = ["json", "html", "both", "sarif", "all"]
    VALID_SEVERITIES = ["critical", "high", "medium", "low", "info"]
    VALID_TOOLS = ["checkov", "trivy", "semgrep", "gitleaks"]
    VALID_CATEGORIES = ["iac", "sca", "sast", "secrets"]
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        logger.debug(f"Initializing ConfigLoader with path: {config_path}")
        
    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            logger.error(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        logger.info(f"Loading configuration from: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in configuration file: {e}")
            raise ValueError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            logger.error(f"Error reading configuration file: {e}")
            raise
        
        # Validate configuration
        self._validate(config)
        logger.debug("Configuration loaded and validated successfully")
        
        return config
    
    def _validate(self, config: Dict[str, Any]) -> None:
        """Validate configuration structure and values."""
        if not config:
            raise ValueError("Configuration is empty")
        
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")
        
        # Validate tools section
        if "tools" not in config:
            raise ValueError("Configuration must contain 'tools' section")
        
        tools = config.get("tools", {})
        if not isinstance(tools, dict):
            raise ValueError("'tools' section must be a dictionary")
        
        # Check at least one tool is enabled
        enabled_tools = [name for name, cfg in tools.items() 
                        if isinstance(cfg, dict) and cfg.get("enabled", False)]
        
        if not enabled_tools:
            raise ValueError("At least one tool must be enabled")
        
        logger.debug(f"Enabled tools: {enabled_tools}")
        
        # Validate each enabled tool
        for tool_name, tool_cfg in tools.items():
            if not isinstance(tool_cfg, dict):
                logger.warning(f"Tool '{tool_name}' config is not a dictionary, skipping")
                continue
                
            if tool_cfg.get("enabled", False):
                # Validate tool category
                if tool_name not in self.VALID_CATEGORIES:
                    logger.warning(f"Unknown tool category: {tool_name}")
                
                # Validate runner is specified
                if "runner" not in tool_cfg:
                    raise ValueError(f"Tool '{tool_name}' is enabled but has no 'runner' specified")
                
                runner = tool_cfg["runner"]
                if runner not in self.VALID_TOOLS:
                    logger.warning(f"Unknown runner: {runner}")
                
                # Validate args is a list if present
                if "args" in tool_cfg and not isinstance(tool_cfg["args"], list):
                    raise ValueError(f"Tool '{tool_name}' args must be a list")
        
        # Validate output section
        if "output" in config:
            self._validate_output(config["output"])
    
    def _validate_output(self, output: Dict[str, Any]) -> None:
        """Validate output configuration section."""
        if not isinstance(output, dict):
            raise ValueError("'output' section must be a dictionary")
        
        # Validate format
        if "format" in output:
            format_value = output["format"].lower()
            if format_value not in self.VALID_FORMATS:
                raise ValueError(
                    f"Invalid output format: '{format_value}'. "
                    f"Valid values: {', '.join(self.VALID_FORMATS)}"
                )
        
        # Validate fail_on
        if "fail_on" in output:
            fail_on = output["fail_on"].lower()
            if fail_on not in self.VALID_SEVERITIES:
                raise ValueError(
                    f"Invalid fail_on value: '{fail_on}'. "
                    f"Valid values: {', '.join(self.VALID_SEVERITIES)}"
                )
        
        # Validate report_path
        if "report_path" in output:
            if not isinstance(output["report_path"], str):
                raise ValueError("'report_path' must be a string")

