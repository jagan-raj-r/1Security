"""
JSON reporter for 1Security scan results
"""
import json
from pathlib import Path
from typing import List
from datetime import datetime
from core.schema import ScanResult
from core.constants import JSON_REPORT_NAME
from core import __version__


class JSONReporter:
    """Generate JSON reports from scan results."""
    
    def __init__(self, output_path: Path):
        """
        Initialize JSON reporter.
        
        Args:
            output_path: Directory to write reports to
        """
        self.output_path = Path(output_path)
        
    def generate(self, scan_results: List[ScanResult]) -> Path:
        """
        Generate JSON report.
        
        Args:
            scan_results: List of ScanResult objects
            
        Returns:
            Path to generated JSON file
        """
        # Create output directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Build report structure
        report = {
            "metadata": {
                "tool": "1security",
                "version": __version__,
                "generated_at": datetime.now().isoformat(),
            },
            "summary": self._generate_summary(scan_results),
            "scans": [sr.to_dict() for sr in scan_results],
            "findings": self._collect_all_findings(scan_results),
        }
        
        # Write to file
        output_file = self.output_path / JSON_REPORT_NAME
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def _generate_summary(self, scan_results: List[ScanResult]) -> dict:
        """Generate summary statistics."""
        total_findings = sum(len(sr.findings) for sr in scan_results)
        
        severity_count = {}
        category_count = {}
        
        for scan_result in scan_results:
            # Count by category
            category = scan_result.category
            category_count[category] = category_count.get(category, 0) + len(scan_result.findings)
            
            # Count by severity
            for finding in scan_result.findings:
                severity = finding.severity
                severity_count[severity] = severity_count.get(severity, 0) + 1
        
        return {
            "total_findings": total_findings,
            "severity_breakdown": severity_count,
            "category_breakdown": category_count,
            "tools_executed": [sr.tool for sr in scan_results],
        }
    
    def _collect_all_findings(self, scan_results: List[ScanResult]) -> List[dict]:
        """Collect all findings from all scans."""
        all_findings = []
        
        for scan_result in scan_results:
            for finding in scan_result.findings:
                all_findings.append(finding.to_dict())
        
        # Sort by severity (Critical first)
        from core.utils.severity_utils import get_severity_order
        all_findings.sort(key=lambda f: get_severity_order(f.get("severity", "UNKNOWN")))
        
        return all_findings

