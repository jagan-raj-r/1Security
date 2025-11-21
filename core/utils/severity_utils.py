"""
Severity-related utility functions
"""
from core.constants import SEVERITY_ORDER


def get_severity_order(severity: str) -> int:
    """
    Get numeric order for severity level.
    
    Args:
        severity: Severity level string
        
    Returns:
        Numeric priority (lower = more severe)
    """
    return SEVERITY_ORDER.get(severity.upper(), 99)


def compare_severity(sev1: str, sev2: str) -> int:
    """
    Compare two severity levels.
    
    Args:
        sev1: First severity level
        sev2: Second severity level
        
    Returns:
        -1 if sev1 > sev2, 0 if equal, 1 if sev1 < sev2
    """
    order1 = get_severity_order(sev1)
    order2 = get_severity_order(sev2)
    
    if order1 < order2:
        return -1
    elif order1 > order2:
        return 1
    else:
        return 0


def meets_threshold(severity: str, threshold: str) -> bool:
    """
    Check if severity meets or exceeds threshold.
    
    Args:
        severity: Severity to check
        threshold: Threshold severity
        
    Returns:
        True if severity meets or exceeds threshold
    """
    return get_severity_order(severity) <= get_severity_order(threshold)

