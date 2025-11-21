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
from core.utils.tool_installer import ToolInstaller

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
    type=click.Choice(["json", "html", "both", "sarif", "all"], case_sensitive=False),
    default="both",
    help="Output format (json, html, both, sarif, all)",
)
@click.option(
    "--skip-tool-check",
    is_flag=True,
    help="Skip automatic tool installation check",
)
def run(config, output, format, skip_tool_check):
    """
    Run security scans based on configuration.
    """
    console.print("\n[bold blue]🔒 1Security - ASPM Orchestrator[/bold blue]\n")
    
    try:
        # Load configuration
        console.print(f"[cyan]📋 Loading configuration from:[/cyan] {config}")
        config_loader = ConfigLoader(config)
        cfg = config_loader.load()
        
        # Check and install required tools
        if not skip_tool_check:
            installer = ToolInstaller()
            if not installer.ensure_tools_installed(cfg, auto_install=True):
                console.print("\n[yellow]⚠️  Some tools are missing. Scan may fail.[/yellow]")
                console.print("[cyan]Tip: Install missing tools or use --skip-tool-check to proceed anyway[/cyan]")
                # Continue anyway - individual parsers will handle missing tools gracefully
        
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
@click.option(
    "--config",
    "-c",
    default="config.yaml",
    help="Path to configuration file to check tools for",
    type=click.Path(exists=True),
)
def check(config):
    """
    Check if required security tools are installed.
    """
    console.print("\n[bold blue]🔍 1Security - Tool Check[/bold blue]\n")
    
    try:
        # Load configuration to see what tools are needed
        config_loader = ConfigLoader(config)
        cfg = config_loader.load()
        
        # Check tools
        installer = ToolInstaller()
        installer.ensure_tools_installed(cfg, auto_install=False)
        
    except FileNotFoundError as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        console.print("[cyan]Tip: Run '1security init' to create a configuration file[/cyan]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error:[/bold red] {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--config",
    "-c",
    default="config.yaml",
    help="Path to configuration file",
    type=click.Path(exists=True),
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Install all tools without prompting",
)
def setup(config, yes):
    """
    Install all required security scanning tools.
    """
    console.print("\n[bold blue]📦 1Security - Tool Setup[/bold blue]\n")
    
    try:
        # Load configuration
        config_loader = ConfigLoader(config)
        cfg = config_loader.load()
        
        # Install tools
        installer = ToolInstaller()
        
        # Get required tools
        required_tools = installer.get_required_tools(cfg)
        console.print(f"[cyan]Required tools based on configuration:[/cyan]")
        for tool in required_tools:
            if tool in installer.TOOLS:
                tool_info = installer.TOOLS[tool]
                console.print(f"  • {tool_info['name']} ({tool_info['category']})")
        
        # Check and install
        status = installer.check_all_tools(required_tools)
        installer.display_tool_status(status)
        
        if installer.install_missing_tools(status, auto_yes=yes):
            console.print("\n[green]✅ Setup complete! All tools are ready.[/green]")
            console.print("\n[cyan]Next steps:[/cyan]")
            console.print("1. Run: 1security run")
            console.print("2. View reports in the reports/ directory")
            sys.exit(0)
        else:
            console.print("\n[yellow]⚠️  Setup incomplete. Some tools may be missing.[/yellow]")
            sys.exit(1)
            
    except FileNotFoundError as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        console.print("[cyan]Tip: Run '1security init' to create a configuration file[/cyan]")
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
    
    # Ask if user wants to install tools
    console.print("\n[cyan]Would you like to check and install required security tools?[/cyan]")
    from rich.prompt import Confirm
    if Confirm.ask("Check tools now?", default=True):
        console.print("")
        try:
            from core.config_loader import ConfigLoader
            cfg = ConfigLoader(str(config_path)).load()
            installer = ToolInstaller()
            installer.ensure_tools_installed(cfg, auto_install=True)
        except Exception as e:
            console.print(f"[yellow]⚠️  Tool check failed: {e}[/yellow]")
    
    console.print("\n[cyan]Next steps:[/cyan]")
    console.print("1. Edit config.yaml to match your project")
    console.print("2. Run: 1security check (to verify tools)")
    console.print("3. Run: 1security setup (to install missing tools)")
    console.print("4. Run: 1security run (to start scanning)")


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

