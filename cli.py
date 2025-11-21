#!/usr/bin/env python3
"""
1Security CLI - Open Source ASPM Orchestrator
"""
import click
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from core import __version__
from core.orchestrator import Orchestrator
from core.config_loader import ConfigLoader

console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    1Security - Open Source ASPM Orchestrator
    
    Unify security scanning tools into one platform.
    """
    pass


@cli.command()
@click.option(
    "--config",
    "-c",
    default="config.yaml",
    help="Path to configuration file",
    type=click.Path(exists=True),
)
@click.option(
    "--output",
    "-o",
    default="reports",
    help="Output directory for reports",
    type=click.Path(),
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "html", "both"], case_sensitive=False),
    default="both",
    help="Output format",
)
def run(config, output, format):
    """
    Run security scans based on configuration.
    """
    console.print("\n[bold blue]🔒 1Security - ASPM Orchestrator[/bold blue]\n")
    
    try:
        # Load configuration
        console.print(f"[cyan]📋 Loading configuration from:[/cyan] {config}")
        config_loader = ConfigLoader(config)
        cfg = config_loader.load()
        
        # Create output directory
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Run orchestrator
        orchestrator = Orchestrator(cfg, output_path, format)
        results = orchestrator.run()
        
        # Display summary
        display_summary(results)
        
        # Exit with appropriate code based on fail_on threshold
        if results.get("should_fail", False):
            fail_on = cfg.get("output", {}).get("fail_on", "critical")
            console.print(f"\n[bold red]❌ Scan failed: Issues exceed '{fail_on}' threshold[/bold red]")
            sys.exit(1)
        else:
            console.print("\n[bold green]✅ Scan completed successfully[/bold green]")
            sys.exit(0)
            
    except FileNotFoundError as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error:[/bold red] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command()
def init():
    """
    Initialize a new 1Security configuration.
    """
    config_path = Path("config.yaml")
    
    if config_path.exists():
        console.print("[yellow]⚠️  config.yaml already exists[/yellow]")
        if not click.confirm("Overwrite?"):
            return
    
    template = """project: myapp
language: python

tools:
  iac:
    enabled: true
    runner: checkov
    args: ["-d", ".", "--framework", "terraform", "--output", "json", "--quiet"]

output:
  format: both
  report_path: reports/
  fail_on: critical
"""
    
    config_path.write_text(template)
    console.print(f"[green]✅ Created {config_path}[/green]")
    console.print("\n[cyan]Next steps:[/cyan]")
    console.print("1. Edit config.yaml to match your project")
    console.print("2. Run: 1security run")


def display_summary(results):
    """Display a summary table of scan results."""
    console.print("\n[bold]📊 Scan Summary[/bold]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Tool", style="blue")
    table.add_column("Critical", style="red")
    table.add_column("High", style="yellow")
    table.add_column("Medium", style="cyan")
    table.add_column("Low", style="green")
    table.add_column("Info", style="dim")
    table.add_column("Total", style="bold")
    
    for scan in results.get("scans", []):
        severity_count = scan.get("severity_count", {})
        table.add_row(
            scan.get("category", "").upper(),
            scan.get("tool", ""),
            str(severity_count.get("CRITICAL", 0)),
            str(severity_count.get("HIGH", 0)),
            str(severity_count.get("MEDIUM", 0)),
            str(severity_count.get("LOW", 0)),
            str(severity_count.get("INFO", 0)),
            str(scan.get("total_findings", 0)),
        )
    
    console.print(table)
    
    # Overall stats
    total = results.get("total_findings", 0)
    console.print(f"\n[bold]Total Findings:[/bold] {total}")
    
    if results.get("reports"):
        console.print("\n[bold]📄 Reports Generated:[/bold]")
        for report in results["reports"]:
            console.print(f"  • {report}")


if __name__ == "__main__":
    cli()

