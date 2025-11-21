"""
1Security Core Module
"""
__version__ = "0.2.0"
__author__ = "R Jagan Raj"
__license__ = "MIT"

# Import main classes for easier access
from core.orchestrator import Orchestrator
from core.config_loader import ConfigLoader
from core.schema import Finding, ScanResult, Severity, Category

__all__ = [
    "Orchestrator",
    "ConfigLoader",
    "Finding",
    "ScanResult",
    "Severity",
    "Category",
    "__version__",
]

