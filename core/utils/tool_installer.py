"""
Automatic tool detection and installation for 1Security
"""
import subprocess
import sys
import shutil
from typing import Dict, List, Tuple, Optional
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

console = Console()


class ToolInstaller:
    """Manages detection and installation of security scanning tools."""
    
    # Tool configurations
    TOOLS = {
        "checkov": {
            "name": "Checkov",
            "category": "IaC Scanner",
            "install_method": "pip",
            "install_cmd": ["pip", "install", "checkov"],
            "check_cmd": ["checkov", "--version"],
            "required_for": ["iac"],
        },
        "trivy": {
            "name": "Trivy",
            "category": "SCA Scanner",
            "install_method": "brew",
            "install_cmd": ["brew", "install", "trivy"],
            "check_cmd": ["trivy", "--version"],
            "required_for": ["sca"],
            "alternatives": {
                "linux": "See https://aquasecurity.github.io/trivy/latest/getting-started/installation/",
                "windows": "See https://aquasecurity.github.io/trivy/latest/getting-started/installation/",
            }
        },
        "semgrep": {
            "name": "Semgrep",
            "category": "SAST Scanner",
            "install_method": "pip",
            "install_cmd": ["pip", "install", "semgrep"],
            "check_cmd": ["semgrep", "--version"],
            "required_for": ["sast"],
        },
        "gitleaks": {
            "name": "Gitleaks",
            "category": "Secrets Detection",
            "install_method": "brew",
            "install_cmd": ["brew", "install", "gitleaks"],
            "check_cmd": ["gitleaks", "version"],
            "required_for": ["secrets"],
            "alternatives": {
                "linux": "brew install gitleaks OR download from https://github.com/gitleaks/gitleaks/releases",
                "windows": "Download from https://github.com/gitleaks/gitleaks/releases",
            }
        },
    }
    
    def __init__(self):
        """Initialize tool installer."""
        self.platform = self._detect_platform()
        
    def _detect_platform(self) -> str:
        """Detect the operating system."""
        if sys.platform.startswith('darwin'):
            return 'macos'
        elif sys.platform.startswith('linux'):
            return 'linux'
        elif sys.platform.startswith('win'):
            return 'windows'
        return 'unknown'
    
    def check_tool_installed(self, tool_name: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a tool is installed.
        
        Args:
            tool_name: Name of the tool to check
            
        Returns:
            Tuple of (is_installed, version)
        """
        if tool_name not in self.TOOLS:
            return False, None
        
        tool = self.TOOLS[tool_name]
        
        try:
            # Check if command exists
            if not shutil.which(tool["check_cmd"][0]):
                return False, None
            
            # Try to get version
            result = subprocess.run(
                tool["check_cmd"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Some tools return version on stderr, some on stdout
            output = result.stdout or result.stderr
            
            # Extract version (first line usually)
            version = output.strip().split('\n')[0] if output else "installed"
            
            return True, version
            
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            return False, None
    
    def get_required_tools(self, config: Dict) -> List[str]:
        """
        Get list of tools required based on configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            List of required tool names
        """
        required = []
        tools_config = config.get("tools", {})
        
        for tool_category, tool_config in tools_config.items():
            if tool_config.get("enabled", False):
                runner = tool_config.get("runner")
                if runner and runner in self.TOOLS:
                    required.append(runner)
        
        return required
    
    def check_all_tools(self, required_tools: List[str]) -> Dict[str, Tuple[bool, Optional[str]]]:
        """
        Check status of all required tools.
        
        Args:
            required_tools: List of tool names to check
            
        Returns:
            Dictionary mapping tool names to (is_installed, version)
        """
        status = {}
        for tool in required_tools:
            status[tool] = self.check_tool_installed(tool)
        return status
    
    def display_tool_status(self, status: Dict[str, Tuple[bool, Optional[str]]]) -> None:
        """
        Display tool installation status in a nice table.
        
        Args:
            status: Dictionary of tool statuses
        """
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Tool", style="cyan")
        table.add_column("Category", style="blue")
        table.add_column("Status", style="green")
        table.add_column("Version/Info", style="dim")
        
        for tool_name, (installed, version) in status.items():
            if tool_name not in self.TOOLS:
                continue
                
            tool = self.TOOLS[tool_name]
            status_text = "✅ Installed" if installed else "❌ Missing"
            status_style = "green" if installed else "red"
            version_text = version or "Not installed"
            
            table.add_row(
                tool["name"],
                tool["category"],
                f"[{status_style}]{status_text}[/{status_style}]",
                version_text
            )
        
        console.print("\n")
        console.print(table)
        console.print("\n")
    
    def install_tool(self, tool_name: str, auto_yes: bool = False) -> bool:
        """
        Install a specific tool.
        
        Args:
            tool_name: Name of the tool to install
            auto_yes: Skip confirmation prompt
            
        Returns:
            True if installation successful, False otherwise
        """
        if tool_name not in self.TOOLS:
            console.print(f"[red]Unknown tool: {tool_name}[/red]")
            return False
        
        tool = self.TOOLS[tool_name]
        
        # Check if already installed
        installed, version = self.check_tool_installed(tool_name)
        if installed:
            console.print(f"[green]✓ {tool['name']} is already installed ({version})[/green]")
            return True
        
        # Show installation info
        console.print(f"\n[yellow]📦 {tool['name']} ({tool['category']}) is not installed[/yellow]")
        console.print(f"[cyan]Installation method: {tool['install_method']}[/cyan]")
        console.print(f"[cyan]Command: {' '.join(tool['install_cmd'])}[/cyan]")
        
        # Check for platform-specific alternatives
        if tool['install_method'] == 'brew' and self.platform != 'macos':
            alternatives = tool.get('alternatives', {})
            alt_instruction = alternatives.get(self.platform)
            if alt_instruction:
                console.print(f"\n[yellow]Note for {self.platform}:[/yellow]")
                console.print(f"[cyan]{alt_instruction}[/cyan]")
                return False
        
        # Confirm installation
        if not auto_yes:
            proceed = Confirm.ask(f"\nInstall {tool['name']} now?", default=True)
            if not proceed:
                console.print(f"[yellow]⚠️  Skipping {tool['name']} installation[/yellow]")
                return False
        
        # Install the tool
        console.print(f"\n[cyan]Installing {tool['name']}...[/cyan]")
        
        try:
            result = subprocess.run(
                tool['install_cmd'],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes for installation
            )
            
            if result.returncode == 0:
                console.print(f"[green]✓ {tool['name']} installed successfully![/green]")
                
                # Verify installation
                installed, version = self.check_tool_installed(tool_name)
                if installed:
                    console.print(f"[green]✓ Verified: {tool['name']} {version}[/green]")
                    return True
                else:
                    console.print(f"[yellow]⚠️  Installation completed but tool not found in PATH[/yellow]")
                    console.print(f"[yellow]You may need to restart your terminal or add to PATH[/yellow]")
                    return False
            else:
                console.print(f"[red]✗ Installation failed:[/red]")
                console.print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            console.print(f"[red]✗ Installation timed out after 5 minutes[/red]")
            return False
        except Exception as e:
            console.print(f"[red]✗ Installation error: {str(e)}[/red]")
            return False
    
    def install_missing_tools(self, status: Dict[str, Tuple[bool, Optional[str]]], auto_yes: bool = False) -> bool:
        """
        Install all missing tools.
        
        Args:
            status: Dictionary of tool statuses
            auto_yes: Skip confirmation prompts
            
        Returns:
            True if all installations successful, False otherwise
        """
        missing_tools = [tool for tool, (installed, _) in status.items() if not installed]
        
        if not missing_tools:
            console.print("[green]✓ All required tools are already installed![/green]")
            return True
        
        console.print(f"\n[yellow]📦 Found {len(missing_tools)} missing tool(s)[/yellow]")
        
        if not auto_yes:
            proceed = Confirm.ask(f"\nInstall all missing tools now?", default=True)
            if not proceed:
                console.print("[yellow]⚠️  Skipping automatic installation[/yellow]")
                console.print("\nTo install manually:")
                for tool in missing_tools:
                    if tool in self.TOOLS:
                        console.print(f"  • {self.TOOLS[tool]['name']}: {' '.join(self.TOOLS[tool]['install_cmd'])}")
                return False
        
        # Install each missing tool
        success_count = 0
        for tool in missing_tools:
            if self.install_tool(tool, auto_yes=True):
                success_count += 1
        
        if success_count == len(missing_tools):
            console.print(f"\n[green]✓ All {len(missing_tools)} tool(s) installed successfully![/green]")
            return True
        else:
            failed = len(missing_tools) - success_count
            console.print(f"\n[yellow]⚠️  {success_count}/{len(missing_tools)} tools installed ({failed} failed)[/yellow]")
            return False
    
    def ensure_tools_installed(self, config: Dict, auto_install: bool = True) -> bool:
        """
        Main method to check and install required tools.
        
        Args:
            config: Configuration dictionary
            auto_install: Whether to automatically install missing tools
            
        Returns:
            True if all required tools are installed, False otherwise
        """
        console.print("\n[bold blue]🔍 Checking required security tools...[/bold blue]")
        
        # Get required tools from config
        required_tools = self.get_required_tools(config)
        
        if not required_tools:
            console.print("[yellow]⚠️  No tools enabled in configuration[/yellow]")
            return True
        
        # Check tool status
        status = self.check_all_tools(required_tools)
        
        # Display status
        self.display_tool_status(status)
        
        # Check if any tools are missing
        missing_tools = [tool for tool, (installed, _) in status.items() if not installed]
        
        if not missing_tools:
            console.print("[green]✓ All required tools are installed![/green]")
            return True
        
        # Install missing tools if requested
        if auto_install:
            return self.install_missing_tools(status, auto_yes=False)
        else:
            console.print(f"[yellow]⚠️  {len(missing_tools)} tool(s) missing. Run with --install to install automatically[/yellow]")
            return False

