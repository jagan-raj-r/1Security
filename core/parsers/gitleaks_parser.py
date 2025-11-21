"""
Gitleaks parser for secrets detection in code repositories
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


class GitleaksParser:
    """Parser for Gitleaks secrets scanner."""
    
    # All secrets are treated as HIGH or CRITICAL
    SEVERITY_MAP = {
        "high": Severity.HIGH.value,
        "medium": Severity.MEDIUM.value,
        "low": Severity.LOW.value,
    }
    
    def __init__(self, args: List[str] = None):
        """
        Initialize Gitleaks parser.
        
        Args:
            args: Additional arguments to pass to Gitleaks
        """
        self.args = args or []
        
    def run(self) -> ScanResult:
        """
        Execute Gitleaks and parse results.
        
        Returns:
            ScanResult containing parsed findings
        """
        start_time = time.time()
        
        try:
            # Build command
            cmd = ["gitleaks"] + self.args
            
            # Ensure report format is JSON
            if "--report-format" not in self.args and "-f" not in self.args:
                cmd.extend(["--report-format", "json"])
            
            # Add detect command if not specified
            if "detect" not in self.args and "protect" not in self.args:
                cmd.insert(1, "detect")
            
            # Run Gitleaks
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TOOL_TIMEOUT_SECONDS
            )
            
            # Gitleaks returns exit code 1 when secrets are found
            # Exit code 0 = no leaks, 1 = leaks found, other = error
            
            # Parse output
            findings = self._parse_output(result.stdout)
            
            execution_time = time.time() - start_time
            
            return ScanResult(
                tool="gitleaks",
                category="secrets",
                findings=findings,
                execution_time=execution_time,
                success=True,
            )
            
        except subprocess.TimeoutExpired:
            return ScanResult(
                tool="gitleaks",
                category="secrets",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message="Gitleaks execution timed out after 5 minutes",
            )
        except FileNotFoundError:
            return ScanResult(
                tool="gitleaks",
                category="secrets",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message="Gitleaks is not installed. Run: brew install gitleaks (macOS) or see https://github.com/gitleaks/gitleaks",
            )
        except Exception as e:
            return ScanResult(
                tool="gitleaks",
                category="secrets",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message=f"Error running Gitleaks: {str(e)}",
            )
    
    def _parse_output(self, output: str) -> List[Finding]:
        """
        Parse Gitleaks JSON output into Finding objects.
        
        Args:
            output: JSON output from Gitleaks
            
        Returns:
            List of Finding objects
        """
        findings = []
        
        if not output or not output.strip():
            return findings
        
        try:
            # Gitleaks output is an array of findings
            data = json.loads(output)
            
            # Handle both array and object formats
            if isinstance(data, dict):
                data = [data]
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Gitleaks output as JSON: {e}")
            return findings
        
        for leak in data:
            finding = self._parse_leak(leak)
            if finding:
                findings.append(finding)
        
        return findings
    
    def _parse_leak(self, leak: Dict[str, Any]) -> Optional[Finding]:
        """
        Parse a single Gitleaks leak into a Finding.
        
        Args:
            leak: Leak dictionary from Gitleaks
            
        Returns:
            Finding object or None
        """
        # Extract basic information
        rule_id = leak.get("RuleID", "UNKNOWN")
        description = leak.get("Description", "")
        file_path = make_path_relative(leak.get("File", ""))
        
        # Extract location
        start_line = leak.get("StartLine")
        end_line = leak.get("EndLine")
        start_column = leak.get("StartColumn")
        
        # Extract secret information
        secret = leak.get("Secret", "")
        match = leak.get("Match", "")
        
        # Build title
        title = f"Secret detected: {rule_id}"
        if description:
            title = description
        
        # Build detailed description (without exposing the actual secret)
        full_description = f"{description}\n\n"
        full_description += f"Rule: {rule_id}\n"
        
        # Add redacted match info
        if match and len(match) > 10:
            # Redact middle portion of the secret
            redacted = match[:5] + "***" + match[-5:]
            full_description += f"Match (redacted): {redacted}\n"
        
        # Add commit info if available
        commit = leak.get("Commit", "")
        if commit:
            full_description += f"Commit: {commit}\n"
        
        author = leak.get("Author", "")
        if author:
            full_description += f"Author: {author}\n"
        
        email = leak.get("Email", "")
        if email:
            full_description += f"Email: {email}\n"
        
        date = leak.get("Date", "")
        if date:
            full_description += f"Date: {date}\n"
        
        # Extract tags for categorization
        tags = leak.get("Tags", [])
        if tags:
            full_description += f"Tags: {', '.join(tags)}"
        
        # All secrets are HIGH severity by default
        severity = Severity.HIGH.value
        
        # Build recommendation
        recommendation = f"Remove the exposed secret from {file_path}"
        recommendation += "\n1. Rotate/revoke the compromised credential immediately"
        recommendation += "\n2. Remove the secret from the code"
        recommendation += "\n3. Use environment variables or secret management tools"
        recommendation += "\n4. Consider using git-filter-repo to remove from history"
        
        # Fingerprint for deduplication
        fingerprint = leak.get("Fingerprint", "")
        
        # Create Finding
        finding = Finding(
            tool="gitleaks",
            category="secrets",
            severity=severity,
            title=title,
            description=full_description.strip(),
            file=file_path if file_path else None,
            line=start_line,
            column=start_column,
            rule_id=rule_id,
            check_id=rule_id,
            recommendation=recommendation,
            code_snippet=match[:50] + "..." if match and len(match) > 50 else None,  # Limit exposure
            raw_output=leak,
        )
        
        return finding
