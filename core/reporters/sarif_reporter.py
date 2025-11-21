"""
SARIF reporter for 1Security scan results
SARIF (Static Analysis Results Interchange Format) is a standard format for static analysis tools
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from core.schema import ScanResult, Finding
from core.constants import SARIF_REPORT_NAME
from core import __version__


class SARIFReporter:
    """Generate SARIF reports from scan results."""
    
    SARIF_VERSION = "2.1.0"
    SARIF_SCHEMA = "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"
    
    # Map our severity to SARIF levels
    SEVERITY_MAP = {
        "CRITICAL": "error",
        "HIGH": "error",
        "MEDIUM": "warning",
        "LOW": "note",
        "INFO": "note",
        "UNKNOWN": "none",
    }
    
    def __init__(self, output_path: Path):
        """
        Initialize SARIF reporter.
        
        Args:
            output_path: Directory to write reports to
        """
        self.output_path = Path(output_path)
        
    def generate(self, scan_results: List[ScanResult]) -> Path:
        """
        Generate SARIF report.
        
        Args:
            scan_results: List of ScanResult objects
            
        Returns:
            Path to generated SARIF file
        """
        # Create output directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Build SARIF structure
        sarif = {
            "version": self.SARIF_VERSION,
            "$schema": self.SARIF_SCHEMA,
            "runs": self._create_runs(scan_results),
        }
        
        # Write to file
        output_file = self.output_path / SARIF_REPORT_NAME
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sarif, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def _create_runs(self, scan_results: List[ScanResult]) -> List[Dict[str, Any]]:
        """
        Create SARIF runs from scan results.
        Each tool gets its own run.
        
        Args:
            scan_results: List of ScanResult objects
            
        Returns:
            List of SARIF run objects
        """
        runs = []
        
        for scan_result in scan_results:
            run = {
                "tool": self._create_tool_info(scan_result),
                "results": self._create_results(scan_result.findings),
                "invocations": [self._create_invocation(scan_result)],
            }
            
            # Add rules/taxonomies
            rules = self._create_rules(scan_result.findings)
            if rules:
                run["tool"]["driver"]["rules"] = rules
            
            runs.append(run)
        
        return runs
    
    def _create_tool_info(self, scan_result: ScanResult) -> Dict[str, Any]:
        """Create SARIF tool information."""
        return {
            "driver": {
                "name": scan_result.tool,
                "version": __version__,
                "informationUri": "https://github.com/jaganraj/1security",
                "semanticVersion": __version__,
                "organization": "1Security",
                "properties": {
                    "category": scan_result.category,
                }
            }
        }
    
    def _create_invocation(self, scan_result: ScanResult) -> Dict[str, Any]:
        """Create SARIF invocation information."""
        return {
            "executionSuccessful": scan_result.success,
            "endTimeUtc": datetime.now().isoformat() + "Z",
            "properties": {
                "executionTime": scan_result.execution_time,
                "errorMessage": scan_result.error_message,
            }
        }
    
    def _create_rules(self, findings: List[Finding]) -> List[Dict[str, Any]]:
        """
        Create SARIF rules from findings.
        
        Args:
            findings: List of Finding objects
            
        Returns:
            List of SARIF rule objects
        """
        # Extract unique rules
        rules_dict = {}
        
        for finding in findings:
            rule_id = finding.rule_id or finding.check_id or "UNKNOWN"
            
            if rule_id not in rules_dict:
                rules_dict[rule_id] = {
                    "id": rule_id,
                    "name": finding.title,
                    "shortDescription": {
                        "text": finding.title
                    },
                    "fullDescription": {
                        "text": finding.description
                    },
                    "defaultConfiguration": {
                        "level": self.SEVERITY_MAP.get(finding.severity, "warning")
                    },
                    "help": {
                        "text": finding.recommendation if finding.recommendation else finding.description
                    },
                    "properties": {
                        "tags": [finding.category, finding.severity.lower()],
                    }
                }
                
                # Add security metadata
                if finding.cwe or finding.cve or finding.owasp:
                    rules_dict[rule_id]["properties"]["security-severity"] = self._get_security_score(finding.severity)
                
                if finding.cwe:
                    rules_dict[rule_id]["properties"]["cwe"] = finding.cwe
                
                if finding.cve:
                    rules_dict[rule_id]["properties"]["cve"] = finding.cve
                
                if finding.owasp:
                    rules_dict[rule_id]["properties"]["owasp"] = finding.owasp
                
                if finding.references:
                    rules_dict[rule_id]["helpUri"] = finding.references[0] if finding.references else None
        
        return list(rules_dict.values())
    
    def _create_results(self, findings: List[Finding]) -> List[Dict[str, Any]]:
        """
        Create SARIF results from findings.
        
        Args:
            findings: List of Finding objects
            
        Returns:
            List of SARIF result objects
        """
        results = []
        
        for finding in findings:
            result = {
                "ruleId": finding.rule_id or finding.check_id or "UNKNOWN",
                "level": self.SEVERITY_MAP.get(finding.severity, "warning"),
                "message": {
                    "text": finding.description
                },
                "locations": self._create_locations(finding),
            }
            
            # Add fixes if available
            if finding.recommendation:
                result["message"]["markdown"] = f"{finding.description}\n\n**Recommendation:** {finding.recommendation}"
            
            # Add code flow if available
            if finding.code_snippet:
                result["codeFlows"] = [{
                    "threadFlows": [{
                        "locations": [{
                            "location": self._create_locations(finding)[0] if self._create_locations(finding) else {}
                        }]
                    }]
                }]
            
            # Add properties
            result["properties"] = {
                "severity": finding.severity,
                "category": finding.category,
                "tool": finding.tool,
            }
            
            if finding.cwe:
                result["properties"]["cwe"] = finding.cwe
            
            if finding.cve:
                result["properties"]["cve"] = finding.cve
            
            if finding.owasp:
                result["properties"]["owasp"] = finding.owasp
            
            results.append(result)
        
        return results
    
    def _create_locations(self, finding: Finding) -> List[Dict[str, Any]]:
        """Create SARIF location from finding."""
        locations = []
        
        if finding.file:
            location = {
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": finding.file,
                    }
                }
            }
            
            # Add region if line number is available
            if finding.line:
                location["physicalLocation"]["region"] = {
                    "startLine": finding.line,
                }
                
                if finding.column:
                    location["physicalLocation"]["region"]["startColumn"] = finding.column
                
                # Add code snippet if available
                if finding.code_snippet:
                    location["physicalLocation"]["region"]["snippet"] = {
                        "text": finding.code_snippet
                    }
            
            locations.append(location)
        
        # If no file but has resource (for IaC)
        elif finding.resource:
            locations.append({
                "logicalLocations": [{
                    "name": finding.resource,
                    "kind": "resource"
                }]
            })
        
        return locations
    
    def _get_security_score(self, severity: str) -> str:
        """
        Convert severity to SARIF security score (0.0 to 10.0).
        
        Args:
            severity: Severity level
            
        Returns:
            Security score as string
        """
        scores = {
            "CRITICAL": "9.0",
            "HIGH": "7.0",
            "MEDIUM": "5.0",
            "LOW": "3.0",
            "INFO": "1.0",
            "UNKNOWN": "0.0",
        }
        return scores.get(severity, "5.0")
