"""
Semgrep parser for SAST (Static Application Security Testing) scanning results
"""
import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from core.schema import Finding, ScanResult, Severity
from core.utils.file_utils import make_path_relative
from core.constants import TOOL_TIMEOUT_SECONDS
from core.logger import get_logger

logger = get_logger(__name__)


class SemgrepParser:
    """Parser for Semgrep SAST scanner."""
    
    SEVERITY_MAP = {
        "ERROR": Severity.HIGH.value,
        "WARNING": Severity.MEDIUM.value,
        "INFO": Severity.LOW.value,
    }
    
    def __init__(self, args: List[str] = None):
        """
        Initialize Semgrep parser.
        
        Args:
            args: Additional arguments to pass to Semgrep
        """
        self.args = args or []
        
    def run(self) -> ScanResult:
        """
        Execute Semgrep and parse results.
        
        Returns:
            ScanResult containing parsed findings
        """
        start_time = time.time()
        
        try:
            # Build command
            cmd = ["semgrep"] + self.args
            
            # Ensure JSON output
            if "--json" not in self.args:
                cmd.append("--json")
            
            # Add default config if none specified
            if "--config" not in self.args and "-c" not in self.args:
                cmd.extend(["--config", "auto"])
            
            # Run Semgrep
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TOOL_TIMEOUT_SECONDS
            )
            
            # Semgrep returns non-zero exit code when findings are present
            # So we don't check returncode
            
            # Parse output
            findings = self._parse_output(result.stdout)
            
            execution_time = time.time() - start_time
            
            return ScanResult(
                tool="semgrep",
                category="sast",
                findings=findings,
                execution_time=execution_time,
                success=True,
            )
            
        except subprocess.TimeoutExpired:
            return ScanResult(
                tool="semgrep",
                category="sast",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message="Semgrep execution timed out after 5 minutes",
            )
        except FileNotFoundError:
            return ScanResult(
                tool="semgrep",
                category="sast",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message="Semgrep is not installed. Run: pip install semgrep or brew install semgrep",
            )
        except Exception as e:
            return ScanResult(
                tool="semgrep",
                category="sast",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message=f"Error running Semgrep: {str(e)}",
            )
    
    def _parse_output(self, output: str) -> List[Finding]:
        """
        Parse Semgrep JSON output into Finding objects.
        
        Args:
            output: JSON output from Semgrep
            
        Returns:
            List of Finding objects
        """
        findings = []
        
        if not output or not output.strip():
            return findings
        
        try:
            data = json.loads(output)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Semgrep output as JSON: {e}")
            return findings
        
        # Semgrep output structure: results array containing findings
        results = data.get("results", [])
        
        for result in results:
            finding = self._parse_result(result)
            if finding:
                findings.append(finding)
        
        return findings
    
    def _parse_result(self, result: Dict[str, Any]) -> Optional[Finding]:
        """
        Parse a single Semgrep result into a Finding.
        
        Args:
            result: Result dictionary from Semgrep
            
        Returns:
            Finding object or None
        """
        # Extract basic information
        check_id = result.get("check_id", "UNKNOWN")
        path = make_path_relative(result.get("path", ""))
        
        # Extract location
        start = result.get("start", {})
        end = result.get("end", {})
        line = start.get("line")
        column = start.get("col")
        
        # Extract metadata
        extra = result.get("extra", {})
        message = extra.get("message", "")
        severity_raw = extra.get("severity", "WARNING")
        
        # Map severity
        severity = self.SEVERITY_MAP.get(severity_raw.upper(), Severity.MEDIUM.value)
        
        # Extract metadata
        metadata = extra.get("metadata", {})
        
        # Extract CWE
        cwe_list = metadata.get("cwe", [])
        cwe = cwe_list[0] if cwe_list else None
        if cwe and not cwe.startswith("CWE-"):
            cwe = f"CWE-{cwe}"
        
        # Extract OWASP
        owasp_list = metadata.get("owasp", [])
        owasp = ", ".join(owasp_list) if owasp_list else None
        
        # Extract references
        references = metadata.get("references", [])
        
        # Get vulnerability class or category
        category = metadata.get("category", "")
        vulnerability_class = metadata.get("vulnerability_class", [])
        
        # Build title
        title = message.split('\n')[0] if message else check_id
        
        # Build description
        description = message if message else f"Semgrep finding: {check_id}"
        if category:
            description += f"\n\nCategory: {category}"
        if vulnerability_class:
            description += f"\nVulnerability Class: {', '.join(vulnerability_class)}"
        
        # Build recommendation
        recommendation = metadata.get("fix", None)
        if not recommendation and metadata.get("fix_regex"):
            recommendation = f"Apply fix regex: {metadata.get('fix_regex')}"
        
        # Extract code snippet
        code_snippet = None
        lines = result.get("extra", {}).get("lines")
        if lines:
            code_snippet = lines.strip()
        
        # Create Finding
        finding = Finding(
            tool="semgrep",
            category="sast",
            severity=severity,
            title=title,
            description=description.strip(),
            file=path if path else None,
            line=line,
            column=column,
            rule_id=check_id,
            check_id=check_id,
            cwe=cwe,
            owasp=owasp,
            recommendation=recommendation,
            references=references if references else None,
            code_snippet=code_snippet,
            raw_output=result,
        )
        
        return finding
