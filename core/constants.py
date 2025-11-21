"""
Constants and configuration values for 1Security
"""

# Application metadata
APP_NAME = "1Security"
APP_DESCRIPTION = "Open Source ASPM Orchestrator"

# Default configuration values
DEFAULT_OUTPUT_DIR = "reports"
DEFAULT_OUTPUT_FORMAT = "both"
DEFAULT_FAIL_ON = "critical"
DEFAULT_CONFIG_FILE = "config.yaml"

# Tool configuration
TOOL_TIMEOUT_SECONDS = 300  # 5 minutes

# Severity levels (ordered by priority)
SEVERITY_ORDER = {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
    "INFO": 4,
    "UNKNOWN": 5
}

# Tool categories
CATEGORY_IAC = "iac"
CATEGORY_SAST = "sast"
CATEGORY_SCA = "sca"
CATEGORY_DAST = "dast"
CATEGORY_SECRETS = "secrets"
CATEGORY_CONTAINER = "container"

# Report filenames
JSON_REPORT_NAME = "1security-report.json"
HTML_REPORT_NAME = "1security-report.html"
SARIF_REPORT_NAME = "1security-report.sarif"

# Error messages
ERROR_CONFIG_NOT_FOUND = "Configuration file not found: {path}"
ERROR_CONFIG_EMPTY = "Configuration is empty"
ERROR_NO_TOOLS_SECTION = "Configuration must contain 'tools' section"
ERROR_NO_TOOLS_ENABLED = "At least one tool must be enabled"
ERROR_NO_RUNNER_SPECIFIED = "Tool '{tool}' is enabled but has no 'runner' specified"
ERROR_TOOL_NOT_INSTALLED = "{tool} is not installed. Run: pip install {tool}"
ERROR_TOOL_TIMEOUT = "{tool} execution timed out after {timeout} seconds"
ERROR_TOOL_NOT_IMPLEMENTED = "Tool '{tool}' is not yet implemented"

# Success messages
SUCCESS_CONFIG_CREATED = "✅ Created {file}"
SUCCESS_SCAN_COMPLETE = "✅ Scan completed successfully"
SUCCESS_TOOL_COMPLETE = "✓ {tool} completed ({count} findings)"

# Warning messages
WARNING_CONFIG_EXISTS = "⚠️  config.yaml already exists"
WARNING_NO_FINDINGS = "No findings to report"

# UI Elements
EMOJI_LOCK = "🔒"
EMOJI_FOLDER = "📋"
EMOJI_REPORT = "📄"
EMOJI_CHECK = "✅"
EMOJI_CROSS = "❌"
EMOJI_WARNING = "⚠️"
EMOJI_CHART = "📊"
EMOJI_ROCKET = "🚀"

