"""
Unified output schema for 1Security
"""
from dataclasses import dataclass, asdict
from typing import Optional, List
from enum import Enum


class Severity(Enum):
    """Standardized severity levels."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"
    UNKNOWN = "UNKNOWN"


class Category(Enum):
    """Security scanning categories."""
    SCA = "sca"
    SAST = "sast"
    DAST = "dast"
    IAC = "iac"
    SECRETS = "secrets"
    CONTAINER = "container"


@dataclass
class Finding:
    """Unified finding structure across all tools."""
    
    # Core fields
    tool: str
    category: str
    severity: str
    title: str
    description: str
    
    # Location
    file: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    resource: Optional[str] = None  # For IaC resources
    
    # Identification
    rule_id: Optional[str] = None
    check_id: Optional[str] = None
    cwe: Optional[str] = None
    cve: Optional[str] = None
    owasp: Optional[str] = None
    
    # Additional context
    recommendation: Optional[str] = None
    references: Optional[List[str]] = None
    code_snippet: Optional[str] = None
    
    # Metadata
    raw_output: Optional[dict] = None
    
    def to_dict(self) -> dict:
        """Convert finding to dictionary."""
        data = asdict(self)
        # Clean up None values
        return {k: v for k, v in data.items() if v is not None}
    
    def __str__(self) -> str:
        location = self.file or self.resource or "Unknown"
        if self.line:
            location += f":{self.line}"
        return f"[{self.severity}] {self.tool}: {self.title} @ {location}"


@dataclass
class ScanResult:
    """Result from a single tool scan."""
    
    tool: str
    category: str
    findings: List[Finding]
    execution_time: float
    success: bool
    error_message: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert scan result to dictionary."""
        return {
            "tool": self.tool,
            "category": self.category,
            "findings": [f.to_dict() for f in self.findings],
            "total_findings": len(self.findings),
            "severity_count": self._count_by_severity(),
            "execution_time": self.execution_time,
            "success": self.success,
            "error_message": self.error_message,
        }
    
    def _count_by_severity(self) -> dict:
        """Count findings by severity."""
        counts = {}
        for finding in self.findings:
            severity = finding.severity
            counts[severity] = counts.get(severity, 0) + 1
        return counts

