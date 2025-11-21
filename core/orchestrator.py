"""
Orchestrator for coordinating security tool execution
"""
from pathlib import Path
from typing import Dict, Any, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.parsers.checkov_parser import CheckovParser
from core.parsers.trivy_parser import TrivyParser
from core.reporters.json_reporter import JSONReporter
from core.reporters.html_reporter import HTMLReporter


console = Console()


class Orchestrator:
    """Coordinates execution of security tools and report generation."""
    
    def __init__(self, config: Dict[str, Any], output_path: Path, output_format: str = "both"):
        """
        Initialize orchestrator.
        
        Args:
            config: Configuration dictionary
            output_path: Path to output directory
            output_format: Output format (json, html, or both)
        """
        self.config = config
        self.output_path = Path(output_path)
        self.output_format = output_format.lower()
        self.scan_results = []
        
    def run(self) -> Dict[str, Any]:
        """
        Execute all enabled security tools.
        
        Returns:
            Dictionary containing scan results and metadata
        """
        tools = self.config.get("tools", {})
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Process each tool
            for tool_name, tool_config in tools.items():
                if not tool_config.get("enabled", False):
                    continue
                
                runner = tool_config.get("runner")
                args = tool_config.get("args", [])
                
                task = progress.add_task(
                    f"[cyan]Running {runner}...",
                    total=None
                )
                
                # Execute tool
                scan_result = self._run_tool(tool_name, runner, args)
                self.scan_results.append(scan_result)
                
                progress.update(
                    task,
                    description=f"[green]✓ {runner} completed ({len(scan_result.findings)} findings)"
                )
                progress.stop_task(task)
        
        # Generate reports
        console.print("\n[cyan]📝 Generating reports...[/cyan]")
        reports = self._generate_reports()
        
        # Compile results
        results = self._compile_results(reports)
        
        return results
    
    def _run_tool(self, tool_name: str, runner: str, args: List[str]):
        """
        Run a specific security tool.
        
        Args:
            tool_name: Category name (e.g., 'iac', 'sast', 'sca')
            runner: Tool runner name (e.g., 'checkov', 'trivy', 'semgrep')
            args: Arguments to pass to the tool
            
        Returns:
            ScanResult object
        """
        # Map runners to their parsers
        tool_map = {
            "checkov": CheckovParser,
            "trivy": TrivyParser,
        }
        
        parser_class = tool_map.get(runner)
        
        if parser_class:
            parser = parser_class(args)
            return parser.run()
        else:
            # Tool not yet implemented
            from core.schema import ScanResult
            return ScanResult(
                tool=runner,
                category=tool_name,
                findings=[],
                execution_time=0.0,
                success=False,
                error_message=f"Tool '{runner}' is not yet implemented"
            )
    
    def _generate_reports(self) -> List[str]:
        """
        Generate output reports.
        
        Returns:
            List of generated report file paths
        """
        reports = []
        
        # Generate JSON report
        if self.output_format in ["json", "both"]:
            json_reporter = JSONReporter(self.output_path)
            json_path = json_reporter.generate(self.scan_results)
            reports.append(str(json_path))
        
        # Generate HTML report
        if self.output_format in ["html", "both"]:
            html_reporter = HTMLReporter(self.output_path)
            html_path = html_reporter.generate(self.scan_results, self.config)
            reports.append(str(html_path))
        
        return reports
    
    def _compile_results(self, reports: List[str]) -> Dict[str, Any]:
        """
        Compile final results dictionary.
        
        Args:
            reports: List of generated report paths
            
        Returns:
            Results dictionary
        """
        total_findings = sum(len(sr.findings) for sr in self.scan_results)
        
        # Count by severity across all scans
        severity_totals = {}
        for scan_result in self.scan_results:
            for finding in scan_result.findings:
                severity = finding.severity
                severity_totals[severity] = severity_totals.get(severity, 0) + 1
        
        # Check for critical issues
        has_critical = severity_totals.get("CRITICAL", 0) > 0
        fail_on = self.config.get("output", {}).get("fail_on", "").upper()
        
        should_fail = False
        if fail_on == "CRITICAL" and severity_totals.get("CRITICAL", 0) > 0:
            should_fail = True
        elif fail_on == "HIGH" and (severity_totals.get("CRITICAL", 0) > 0 or severity_totals.get("HIGH", 0) > 0):
            should_fail = True
        
        return {
            "project": self.config.get("project", "unknown"),
            "scans": [sr.to_dict() for sr in self.scan_results],
            "total_findings": total_findings,
            "severity_totals": severity_totals,
            "has_critical": has_critical,
            "should_fail": should_fail,
            "reports": reports,
        }

