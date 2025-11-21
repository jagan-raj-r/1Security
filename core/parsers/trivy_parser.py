"""
Trivy parser for SCA (Software Composition Analysis) scanning results
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


class TrivyParser:
    """Parser for Trivy vulnerability scanner."""
    
    SEVERITY_MAP = {
        "CRITICAL": Severity.CRITICAL.value,
        "HIGH": Severity.HIGH.value,
        "MEDIUM": Severity.MEDIUM.value,
        "LOW": Severity.LOW.value,
        "UNKNOWN": Severity.UNKNOWN.value,
    }
    
    def __init__(self, args: List[str] = None):
        """
        Initialize Trivy parser.
        
        Args:
            args: Additional arguments to pass to Trivy
        """
        self.args = args or []
        
    def run(self) -> ScanResult:
        """
        Execute Trivy and parse results.
        
        Returns:
            ScanResult containing parsed findings
        """
        start_time = time.time()
        
        try:
            # Build command
            cmd = ["trivy"] + self.args
            
            # Ensure JSON output
            if "--format" not in self.args and "-f" not in self.args:
                cmd.extend(["--format", "json"])
            
            # Suppress Trivy's download progress messages
            if "--quiet" not in self.args and "-q" not in self.args:
                cmd.append("--quiet")
            
            # Run Trivy
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TOOL_TIMEOUT_SECONDS
            )
            
            # Trivy returns non-zero exit code when vulnerabilities are found
            # So we don't check returncode
            
            # Parse output
            findings = self._parse_output(result.stdout)
            
            execution_time = time.time() - start_time
            
            return ScanResult(
                tool="trivy",
                category="sca",
                findings=findings,
                execution_time=execution_time,
                success=True,
            )
            
        except subprocess.TimeoutExpired:
            return ScanResult(
                tool="trivy",
                category="sca",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message="Trivy execution timed out after 5 minutes",
            )
        except FileNotFoundError:
            return ScanResult(
                tool="trivy",
                category="sca",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message="Trivy is not installed. Run: brew install trivy (macOS) or see https://aquasecurity.github.io/trivy/",
            )
        except Exception as e:
            return ScanResult(
                tool="trivy",
                category="sca",
                findings=[],
                execution_time=time.time() - start_time,
                success=False,
                error_message=f"Error running Trivy: {str(e)}",
            )
    
    def _parse_output(self, output: str) -> List[Finding]:
        """
        Parse Trivy JSON output into Finding objects.
        
        Args:
            output: JSON output from Trivy
            
        Returns:
            List of Finding objects
        """
        findings = []
        
        if not output or not output.strip():
            return findings
        
        try:
            data = json.loads(output)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Trivy output as JSON: {e}")
            return findings
        
        # Trivy output structure: Results array containing vulnerability info
        results = data.get("Results", [])
        
        for result in results:
            target = result.get("Target", "")
            result_type = result.get("Type", "")
            
            # Parse vulnerabilities
            vulnerabilities = result.get("Vulnerabilities", [])
            if vulnerabilities:
                for vuln in vulnerabilities:
                    finding = self._parse_vulnerability(vuln, target, result_type)
                    if finding:
                        findings.append(finding)
            
            # Parse misconfigurations (if any)
            misconfigs = result.get("Misconfigurations", [])
            if misconfigs:
                for misconfig in misconfigs:
                    finding = self._parse_misconfiguration(misconfig, target)
                    if finding:
                        findings.append(finding)
        
        return findings
    
    def _parse_vulnerability(self, vuln: Dict[str, Any], target: str, result_type: str) -> Optional[Finding]:
        """
        Parse a single Trivy vulnerability into a Finding.
        
        Args:
            vuln: Vulnerability dictionary from Trivy
            target: Target file/image being scanned
            result_type: Type of result (e.g., 'pip', 'npm', 'alpine')
            
        Returns:
            Finding object or None
        """
        # Extract vulnerability information
        vuln_id = vuln.get("VulnerabilityID", "UNKNOWN")
        pkg_name = vuln.get("PkgName", "")
        installed_version = vuln.get("InstalledVersion", "")
        fixed_version = vuln.get("FixedVersion", "")
        severity_raw = vuln.get("Severity", "UNKNOWN")
        title = vuln.get("Title", "")
        description = vuln.get("Description", "")
        
        # Map severity
        severity = self.SEVERITY_MAP.get(severity_raw.upper(), Severity.UNKNOWN.value)
        
        # Build title
        if not title:
            title = f"{pkg_name}: {vuln_id}"
        
        # Build description
        if not description and title:
            description = title
        elif not description:
            description = f"Vulnerability found in {pkg_name}"
        
        # Build recommendation
        recommendation = None
        if fixed_version:
            recommendation = f"Upgrade {pkg_name} from {installed_version} to {fixed_version}"
        else:
            recommendation = f"No fix available yet for {pkg_name} {installed_version}"
        
        # Extract references
        references = vuln.get("References", [])
        
        # Extract CWE IDs
        cwes = vuln.get("CweIDs", [])
        cwe = cwes[0] if cwes else None
        
        # Primary URL (if available)
        primary_url = vuln.get("PrimaryURL", "")
        if primary_url and primary_url not in references:
            references.insert(0, primary_url)
        
        # CVSS information
        cvss_info = []
        if "CVSS" in vuln:
            for vendor, cvss_data in vuln["CVSS"].items():
                v3_score = cvss_data.get("V3Score")
                if v3_score:
                    cvss_info.append(f"{vendor}: {v3_score}")
        
        # Build full description with version info
        full_description = description
        if installed_version:
            full_description = f"{description}\n\nInstalled Version: {installed_version}"
        if fixed_version:
            full_description += f"\nFixed Version: {fixed_version}"
        if cvss_info:
            full_description += f"\nCVSS: {', '.join(cvss_info)}"
        
        # Create Finding
        finding = Finding(
            tool="trivy",
            category="sca",
            severity=severity,
            title=title,
            description=full_description.strip(),
            file=target if target else None,
            resource=f"{pkg_name}@{installed_version}" if pkg_name else None,
            rule_id=vuln_id,
            cve=vuln_id if vuln_id.startswith("CVE-") else None,
            cwe=cwe,
            recommendation=recommendation,
            references=references if references else None,
            raw_output=vuln,
        )
        
        return finding
    
    def _parse_misconfiguration(self, misconfig: Dict[str, Any], target: str) -> Optional[Finding]:
        """
        Parse a Trivy misconfiguration into a Finding.
        
        Args:
            misconfig: Misconfiguration dictionary from Trivy
            target: Target being scanned
            
        Returns:
            Finding object or None
        """
        # Extract misconfiguration information
        check_id = misconfig.get("ID", "UNKNOWN")
        title = misconfig.get("Title", "")
        description = misconfig.get("Description", "")
        severity_raw = misconfig.get("Severity", "UNKNOWN")
        
        # Map severity
        severity = self.SEVERITY_MAP.get(severity_raw.upper(), Severity.UNKNOWN.value)
        
        # Extract location information
        cause_metadata = misconfig.get("CauseMetadata", {})
        start_line = cause_metadata.get("StartLine")
        
        # Build recommendation
        recommendation = misconfig.get("Resolution", "")
        
        # Extract references
        references = misconfig.get("References", [])
        
        # Create Finding
        finding = Finding(
            tool="trivy",
            category="iac",  # Misconfigurations are typically IaC related
            severity=severity,
            title=title if title else check_id,
            description=description if description else title,
            file=target if target else None,
            line=start_line,
            rule_id=check_id,
            check_id=check_id,
            recommendation=recommendation if recommendation else None,
            references=references if references else None,
            raw_output=misconfig,
        )
        
        return finding

