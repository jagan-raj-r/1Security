# 🛠️ Development Guide

Welcome to 1Security development! This guide covers architecture, setup, contributing, and best practices.

---

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Adding New Tools](#adding-new-tools)
- [Code Style](#code-style)
- [Testing](#testing)
- [Contributing](#contributing)
- [Release Process](#release-process)

---

## 🏗️ Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                           │
│                    (cli.py - Click)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Orchestrator Layer                        │
│              (core/orchestrator.py)                         │
│  - Tool execution                                           │
│  - Result compilation                                       │
│  - Report generation                                        │
└────────┬────────────────────────┬───────────────────────────┘
         │                        │
┌────────▼─────────┐    ┌────────▼──────────┐
│   Parser Layer   │    │  Reporter Layer   │
│  core/parsers/   │    │ core/reporters/   │
│  - Checkov       │    │  - JSON           │
│  - Trivy         │    │  - HTML           │
│  - Semgrep       │    │  - SARIF          │
│  - Gitleaks      │    └───────────────────┘
└──────────────────┘
```

### Core Components

#### 1. **CLI Layer** (`cli.py`)
- **Purpose**: User interface and command handling
- **Framework**: Click
- **Commands**: `init`, `run`, `check`, `setup`
- **Responsibilities**:
  - Parse command-line arguments
  - Load configuration
  - Call orchestrator
  - Display results

#### 2. **Orchestrator** (`core/orchestrator.py`)
- **Purpose**: Coordinate tool execution and result aggregation
- **Responsibilities**:
  - Execute security tools
  - Collect results from parsers
  - Compile unified findings
  - Generate reports
  - Apply fail thresholds

#### 3. **Parsers** (`core/parsers/`)
- **Purpose**: Execute tools and normalize their output
- **Pattern**: Each parser implements:
  ```python
  def parse(self, target_path: str) -> List[Finding]
  ```
- **Current Parsers**:
  - `checkov_parser.py` - IaC scanning
  - `trivy_parser.py` - SCA scanning
  - `semgrep_parser.py` - SAST scanning
  - `gitleaks_parser.py` - Secrets detection

#### 4. **Reporters** (`core/reporters/`)
- **Purpose**: Generate reports in various formats
- **Current Reporters**:
  - `json_reporter.py` - JSON output
  - `html_reporter.py` - Interactive HTML
  - `sarif_reporter.py` - SARIF format

#### 5. **Schema** (`core/schema.py`)
- **Purpose**: Unified data model
- **Key Classes**:
  - `Finding` - Individual security issue
  - `ScanResult` - Complete scan results
  - `Severity` - Severity enum

#### 6. **Utilities** (`core/utils/`)
- **Purpose**: Helper functions
- **Modules**:
  - `file_utils.py` - File operations
  - `severity_utils.py` - Severity comparison
  - `tool_installer.py` - Tool installation

---

## 💻 Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/jagan-raj-r/1Security.git
   cd 1Security
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e .
   ```

4. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"  # If dev extras defined
   # Or manually:
   pip install pytest black pylint mypy
   ```

5. **Install security tools**
   ```bash
   1security setup
   ```

6. **Verify installation**
   ```bash
   1security --version
   1security check
   ```

---

## 📁 Project Structure

```
1Security/
├── cli.py                          # CLI entry point
├── setup.py                        # Package configuration
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
│
├── core/                           # Core package
│   ├── __init__.py                # Package initialization
│   ├── constants.py               # Application constants
│   ├── exceptions.py              # Custom exceptions
│   ├── logger.py                  # Logging configuration
│   ├── schema.py                  # Data models
│   ├── config_loader.py           # Configuration loader
│   ├── orchestrator.py            # Main orchestrator
│   │
│   ├── parsers/                   # Tool parsers
│   │   ├── __init__.py
│   │   ├── checkov_parser.py     # Checkov integration
│   │   ├── trivy_parser.py       # Trivy integration
│   │   ├── semgrep_parser.py     # Semgrep integration
│   │   └── gitleaks_parser.py    # Gitleaks integration
│   │
│   ├── reporters/                 # Report generators
│   │   ├── __init__.py
│   │   ├── json_reporter.py      # JSON reports
│   │   ├── html_reporter.py      # HTML reports
│   │   └── sarif_reporter.py     # SARIF reports
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── file_utils.py          # File operations
│       ├── severity_utils.py      # Severity helpers
│       └── tool_installer.py      # Tool management
│
├── docs/                           # Documentation
│   ├── README.md                  # Documentation index
│   ├── GETTING_STARTED.md         # Quick start guide
│   ├── USER_GUIDE.md              # User documentation
│   ├── FEATURES.md                # Features overview
│   ├── TOOLS.md                   # Tool-specific docs
│   ├── DEVELOPMENT.md             # This file
│   └── CHANGELOG.md               # Version history
│
└── examples/                       # Example configurations
    ├── config.example.yaml        # Example config
    ├── terraform/                 # Example IaC files
    ├── python/                    # Example Python app
    └── nodejs/                    # Example Node.js app
```

---

## 🔧 Adding New Tools

### Step 1: Create a Parser

Create a new file in `core/parsers/`, e.g., `snyk_parser.py`:

```python
"""
Snyk parser for dependency scanning
"""
import json
import subprocess
from typing import List
from core.schema import Finding, ScanResult, Severity, Category
from core.utils.file_utils import make_path_relative
from core.constants import TOOL_TIMEOUT_SECONDS
from core.logger import get_logger

logger = get_logger(__name__)


class SnykParser:
    """Parser for Snyk security scanner"""
    
    def parse(self, target_path: str, args: List[str] = None) -> ScanResult:
        """
        Run Snyk and parse results
        
        Args:
            target_path: Path to scan
            args: Additional Snyk arguments
            
        Returns:
            ScanResult with findings
        """
        findings = []
        args = args or []
        
        # Build command
        cmd = ["snyk", "test", target_path] + args + ["--json"]
        
        logger.info(f"Running Snyk: {' '.join(cmd)}")
        
        try:
            # Execute Snyk
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TOOL_TIMEOUT_SECONDS
            )
            
            # Parse JSON output
            data = json.loads(result.stdout)
            
            # Extract vulnerabilities
            for vuln in data.get("vulnerabilities", []):
                finding = Finding(
                    tool="snyk",
                    category=Category.SCA,
                    severity=self._map_severity(vuln.get("severity")),
                    title=vuln.get("title", "Unknown vulnerability"),
                    description=vuln.get("description", ""),
                    file=make_path_relative(vuln.get("from", [None])[0] or ""),
                    line=0,
                    resource=vuln.get("packageName", ""),
                    rule_id=vuln.get("id", ""),
                    check_id=vuln.get("id", ""),
                    recommendation=vuln.get("remediation", "")
                )
                findings.append(finding)
        
        except subprocess.TimeoutExpired:
            logger.error(f"Snyk timed out after {TOOL_TIMEOUT_SECONDS}s")
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Snyk output: {e}")
        except Exception as e:
            logger.error(f"Snyk execution failed: {e}")
        
        return ScanResult(
            tool="snyk",
            findings=findings,
            summary=self._generate_summary(findings)
        )
    
    def _map_severity(self, severity: str) -> Severity:
        """Map Snyk severity to standard severity"""
        mapping = {
            "critical": Severity.CRITICAL,
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
        }
        return mapping.get(severity.lower(), Severity.INFO)
    
    def _generate_summary(self, findings: List[Finding]) -> dict:
        """Generate summary statistics"""
        summary = {
            "total": len(findings),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
        for finding in findings:
            severity = finding.severity.value.lower()
            if severity in summary:
                summary[severity] += 1
        
        return summary
```

### Step 2: Register the Parser

Add to `core/parsers/__init__.py`:

```python
from core.parsers.snyk_parser import SnykParser

__all__ = [
    # ... existing parsers ...
    "SnykParser",
]
```

### Step 3: Update Orchestrator

Add to `core/orchestrator.py` in the `_run_tool` method:

```python
tool_map = {
    "checkov": CheckovParser,
    "trivy": TrivyParser,
    "semgrep": SemgrepParser,
    "gitleaks": GitleaksParser,
    "snyk": SnykParser,  # Add new tool
}
```

### Step 4: Add Tool Installation

Add to `core/utils/tool_installer.py`:

```python
def install_snyk(self):
    """Install Snyk"""
    if platform.system() == "Darwin":  # macOS
        return self._run_command(["brew", "install", "snyk"])
    else:  # Linux/Others
        return self._run_command(["npm", "install", "-g", "snyk"])
```

### Step 5: Update Constants

Add to `core/constants.py`:

```python
VALID_TOOL_RUNNERS = ["checkov", "trivy", "semgrep", "gitleaks", "snyk"]
TOOL_NAME_SNYK = "Snyk"
```

### Step 6: Test

```bash
# Create test config
cat > test-snyk.yaml << EOF
project_name: "Test-Snyk"

tools:
  sca:
    enabled: true
    runner: "snyk"
    args: []

output:
  format: "json"
  report_path: "reports"
EOF

# Run scan
1security run --config test-snyk.yaml
```

---

## 🎨 Code Style

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Line length: 100 characters (not 79)
# Use 4 spaces for indentation
# Use double quotes for strings
# Use type hints

# Good example:
def process_findings(
    findings: List[Finding],
    severity_threshold: Severity = Severity.HIGH
) -> List[Finding]:
    """
    Filter findings by severity threshold.
    
    Args:
        findings: List of security findings
        severity_threshold: Minimum severity to include
        
    Returns:
        Filtered list of findings
    """
    return [f for f in findings if f.severity >= severity_threshold]
```

### Formatting Tools

```bash
# Format code with black
black .

# Check style with pylint
pylint core/ cli.py

# Type checking with mypy
mypy core/ cli.py
```

### Import Order

```python
# 1. Standard library
import json
import subprocess
from typing import List, Dict

# 2. Third-party packages
import click
from rich.console import Console

# 3. Local imports
from core.schema import Finding
from core.utils import ensure_dir
```

### Docstrings

Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Longer description if needed. Can be multiple paragraphs.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        
    Example:
        >>> my_function("test", 42)
        True
    """
    pass
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test file
pytest tests/test_parsers.py

# Run specific test
pytest tests/test_parsers.py::test_checkov_parser
```

### Writing Tests

Create test files in `tests/` directory:

```python
# tests/test_parsers.py
import pytest
from core.parsers.checkov_parser import CheckovParser
from core.schema import Severity, Category


def test_checkov_parser():
    """Test Checkov parser with sample output"""
    parser = CheckovParser()
    result = parser.parse("examples/terraform/")
    
    assert result.tool == "checkov"
    assert len(result.findings) > 0
    assert all(f.category == Category.IAC for f in result.findings)


def test_severity_mapping():
    """Test severity mapping"""
    parser = CheckovParser()
    
    assert parser._map_severity("CRITICAL") == Severity.CRITICAL
    assert parser._map_severity("HIGH") == Severity.HIGH
    assert parser._map_severity("MEDIUM") == Severity.MEDIUM
```

---

## 🤝 Contributing

### Contribution Workflow

1. **Fork the repository**
   ```bash
   # On GitHub, click "Fork"
   git clone https://github.com/YOUR_USERNAME/1Security.git
   cd 1Security
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   # or
   git checkout -b fix/bug-description
   ```

3. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

4. **Test your changes**
   ```bash
   pytest
   black .
   pylint core/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add Snyk integration"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```

7. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Describe your changes

### Commit Message Format

We follow **Conventional Commits**:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(parser): Add Snyk integration
fix(orchestrator): Fix fail_on threshold logic
docs(readme): Update installation instructions
refactor(utils): Simplify path handling
```

### Pull Request Guidelines

- ✅ **Clear title** - Describe what the PR does
- ✅ **Description** - Explain why the change is needed
- ✅ **Tests** - Include tests for new features
- ✅ **Documentation** - Update docs if needed
- ✅ **No breaking changes** - Unless discussed first
- ✅ **Single purpose** - One feature/fix per PR

---

## 📦 Release Process

### Version Numbering

We use **Semantic Versioning** (semver):

```
MAJOR.MINOR.PATCH

Example: 0.2.0
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes
```

### Release Steps

1. **Update version**
   ```python
   # core/__init__.py
   __version__ = "0.3.0"
   ```

2. **Update CHANGELOG**
   ```markdown
   # docs/CHANGELOG.md
   ## [0.3.0] - 2025-12-01
   
   ### Added
   - Snyk integration for dependency scanning
   
   ### Fixed
   - Bug in fail_on threshold logic
   ```

3. **Create git tag**
   ```bash
   git tag -a v0.3.0 -m "Release v0.3.0"
   git push origin v0.3.0
   ```

4. **Create GitHub release**
   - Go to GitHub → Releases → New Release
   - Tag: v0.3.0
   - Title: 1Security v0.3.0
   - Description: Copy from CHANGELOG

---

## 🐛 Debugging

### Enable Debug Logging

```bash
# Set verbose mode
1security run --verbose

# Or in code:
from core.logger import setup_logger
logger = setup_logger(verbose=True)
```

### Common Issues

#### Issue: Parser not finding tool

**Solution:**
```bash
# Check if tool is installed
which checkov
which trivy

# Install missing tools
1security setup
```

#### Issue: Import errors

**Solution:**
```bash
# Reinstall in development mode
pip uninstall 1security
pip install -e .
```

#### Issue: Test failures

**Solution:**
```bash
# Run tests with verbose output
pytest -v

# Run specific failing test
pytest tests/test_specific.py::test_name -v
```

---

## 📚 Resources

### Internal Documentation
- [Getting Started](GETTING_STARTED.md) - Installation & setup
- [User Guide](USER_GUIDE.md) - Using 1Security
- [Features](FEATURES.md) - Feature overview
- [Tools](TOOLS.md) - Tool-specific docs

### External Resources
- [Python Packaging Guide](https://packaging.python.org/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [PEP 8 Style Guide](https://pep8.org/)

### Tool Documentation
- [Checkov Docs](https://www.checkov.io/1.Welcome/What%20is%20Checkov.html)
- [Trivy Docs](https://aquasecurity.github.io/trivy/)
- [Semgrep Docs](https://semgrep.dev/docs/)
- [Gitleaks Docs](https://github.com/gitleaks/gitleaks)

---

## 🎯 Development Roadmap

### Short Term (Next Release)
- [ ] Add unit tests (pytest)
- [ ] Add integration tests
- [ ] Improve error handling
- [ ] Add more tool integrations

### Medium Term
- [ ] Web dashboard
- [ ] Result deduplication
- [ ] Policy engine
- [ ] Parallel tool execution

### Long Term
- [ ] Plugin system
- [ ] Cloud integrations
- [ ] Machine learning for false positives
- [ ] Custom rule engine

---

## 💬 Getting Help

- **Questions?** Open a [GitHub Discussion](https://github.com/jagan-raj-r/1Security/discussions)
- **Bug?** Open a [GitHub Issue](https://github.com/jagan-raj-r/1Security/issues)
- **Feature Request?** Open a [GitHub Issue](https://github.com/jagan-raj-r/1Security/issues) with label `enhancement`

---

## 🙏 Thank You!

Thank you for contributing to 1Security! Every contribution makes the tool better for everyone.

**Happy coding!** 🚀

---

*Last Updated: November 21, 2025*
