"""
Checkov parser for IaC scanning results
"""
import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any
from core.schema import Finding, ScanResult, Severity
from core.utils.file_utils import make_path_relative
from core.constants import TOOL_TIMEOUT_SECONDS
from core.logger import get_logger

logger = get_logger(__name__)


class CheckovParser:
    """Parser for Checkov IaC scanner."""
    
    SEVERITY_MAP = {
        "CRITICAL": Severity.CRITICAL.value,
        "HIGH": Severity.HIGH.value,
        "MEDIUM": Severity.MEDIUM.value,
        "LOW": Severity.LOW.value,
        "INFO": Severity.INFO.value,
    }
    
    def __init__(self, args: List[str] = None):
        """
        Initialize Checkov parser.
        
        Args:
            args: Additional arguments to pass to Checkov
        """
        self.args = args or []
        
    def run(self) -> ScanResult:
        """
        Execute Checkov and parse results.
        
        Returns:
            ScanResult containing parsed findings
        """
        start_time = time.time()
        
        try:
            # Build command
            cmd = ["checkov"] + self.args
            
            # Ensure JSON output
            if "--output" not in self.args and "-o" not in self.args:
                cmd.extend(["--output", "json"])
            
            # Run Checkov
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TOOL_TIMEOUT_SECONDS
            )
            
            # Checkov returns non-zero exit code when findings are present
            # So we don't check returncode
            
            # Parse output
            findings = self._parse_output(result.stdout)
            
            execution_time = time.time() - start_time
            
            return ScanResult(
                tool="checkov",
                category="iac",
                findings=findings,
                execution_time=execution_time,
                success=True,
            )
            
        except subprocess.TimeoutExpired:
            return ScanResult(
                tool="checkov",
                category="iac",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message="Checkov execution timed out after 5 minutes",
            )
        except FileNotFoundError:
            return ScanResult(
                tool="checkov",
                category="iac",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message="Checkov is not installed. Run: pip install checkov",
            )
        except Exception as e:
            return ScanResult(
                tool="checkov",
                category="iac",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message=f"Error running Checkov: {str(e)}",
            )
    
    def _parse_output(self, output: str) -> List[Finding]:
        """
        Parse Checkov JSON output into Finding objects.
        
        Args:
            output: JSON output from Checkov
            
        Returns:
            List of Finding objects
        """
        findings = []
        
        if not output or not output.strip():
            return findings
        
        try:
            data = json.loads(output)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Checkov output as JSON: {e}")
            return findings
        
        # Checkov can have multiple result sets
        results = data if isinstance(data, list) else [data]
        
        for result_set in results:
            # Parse failed checks
            failed_checks = result_set.get("results", {}).get("failed_checks", [])
            
            for check in failed_checks:
                finding = self._parse_check(check, passed=False)
                if finding:
                    findings.append(finding)
        
        return findings
    
    def _parse_check(self, check: Dict[str, Any], passed: bool = False) -> Finding:
        """
        Parse a single Checkov check into a Finding.
        
        Args:
            check: Checkov check dictionary
            passed: Whether the check passed
            
        Returns:
            Finding object
        """
        # Extract basic information
        check_id = check.get("check_id", "UNKNOWN")
        check_name = check.get("check_name", "Unknown Check")
        file_path = make_path_relative(check.get("file_path", ""))
        
        # Extract location
        file_line_range = check.get("file_line_range", [])
        start_line = file_line_range[0] if file_line_range else None
        
        # Extract resource information
        resource = check.get("resource", "")
        
        # Map severity (Checkov uses "severity" field)
        severity_raw = check.get("severity")
        if severity_raw:
            severity = self.SEVERITY_MAP.get(severity_raw.upper(), Severity.UNKNOWN.value)
        else:
            # Default severity if not provided
            severity = Severity.MEDIUM.value
        
        # Extract guideline/recommendation
        guideline = check.get("guideline", "")
        description = check.get("description", check_name)
        
        # Build references
        references = []
        if guideline:
            references.append(guideline)
        
        # Extract code snippet if available
        code_block = check.get("code_block", [])
        code_snippet = None
        if code_block:
            code_snippet = "\n".join([line[1] for line in code_block if len(line) > 1])
        
        # Create Finding
        finding = Finding(
            tool="checkov",
            category="iac",
            severity=severity,
            title=check_name,
            description=description,
            file=file_path if file_path else None,
            line=start_line,
            resource=resource if resource else None,
            rule_id=check_id,
            check_id=check_id,
            recommendation=guideline if guideline else None,
            references=references if references else None,
            code_snippet=code_snippet if code_snippet else None,
            raw_output=check,
        )
        
        return finding

