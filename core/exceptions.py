"""
Custom exceptions for 1Security
"""


class SecurityError(Exception):
    """Base exception for 1Security errors."""
    pass


class ConfigurationError(SecurityError):
    """Raised when configuration is invalid or missing."""
    pass


class ToolNotFoundError(SecurityError):
    """Raised when a security tool is not installed."""
    
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        super().__init__(f"{tool_name} is not installed. Run: pip install {tool_name}")


class ToolExecutionError(SecurityError):
    """Raised when a security tool fails to execute."""
    
    def __init__(self, tool_name: str, message: str):
        self.tool_name = tool_name
        super().__init__(f"{tool_name} execution failed: {message}")


class ToolTimeoutError(SecurityError):
    """Raised when a security tool times out."""
    
    def __init__(self, tool_name: str, timeout: int):
        self.tool_name = tool_name
        self.timeout = timeout
        super().__init__(f"{tool_name} timed out after {timeout} seconds")


class ParserError(SecurityError):
    """Raised when parsing tool output fails."""
    
    def __init__(self, tool_name: str, message: str):
        self.tool_name = tool_name
        super().__init__(f"Failed to parse {tool_name} output: {message}")


class ReportGenerationError(SecurityError):
    """Raised when report generation fails."""
    pass


class ValidationError(ConfigurationError):
    """Raised when validation fails."""
    pass

