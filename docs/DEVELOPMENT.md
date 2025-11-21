# 🔧 Development Guide

Guide for contributors and developers working on 1Security.

---

## 🏗️ Project Structure

```
1Security/
├── 1security                 # CLI executable
├── cli.py                   # CLI implementation (Click)
├── setup.py                 # Package configuration
├── requirements.txt         # Python dependencies
│
├── core/                    # Core application logic
│   ├── __init__.py         # Package exports
│   ├── orchestrator.py     # Main coordinator
│   ├── config_loader.py    # YAML config parser
│   ├── schema.py           # Data models (Finding, ScanResult)
│   ├── constants.py        # Application constants
│   ├── exceptions.py       # Custom exceptions
│   │
│   ├── parsers/            # Tool output parsers
│   │   ├── checkov_parser.py
│   │   ├── trivy_parser.py
│   │   ├── semgrep_parser.py
│   │   └── gitleaks_parser.py
│   │
│   ├── reporters/          # Report generators
│   │   ├── json_reporter.py
│   │   ├── html_reporter.py
│   │   └── sarif_reporter.py
│   │
│   └── utils/             # Utility modules
│       ├── file_utils.py
│       ├── severity_utils.py
│       └── tool_installer.py
│
├── examples/              # Example configurations
│   ├── config.example.yaml
│   ├── config-phase2.yaml
│   └── vulnerable-app/    # Test files
│
└── docs/                  # Documentation
    ├── GETTING_STARTED.md
    ├── USER_GUIDE.md
    ├── FEATURES.md
    ├── TOOLS.md
    └── CHANGELOG.md
```

---

## 🎯 Architecture Overview

### Design Principles

1. **Plugin Architecture** - Easy to add new tools
2. **Unified Schema** - Consistent output across tools
3. **Separation of Concerns** - Clear module boundaries
4. **Configuration-Driven** - YAML-based flexibility
5. **Extensibility** - Open for extension, closed for modification

### Data Flow

```
CLI (cli.py)
  ↓
ConfigLoader (config_loader.py)
  ↓
Orchestrator (orchestrator.py)
  ↓
Parsers (checkov_parser.py, trivy_parser.py, etc.)
  ↓
Unified Schema (schema.py) → Finding objects
  ↓
Reporters (json_reporter.py, html_reporter.py, sarif_reporter.py)
  ↓
Output Files (reports/)
```

### Key Components

#### 1. CLI Layer (`cli.py`)

- Built with **Click** framework
- Commands: `init`, `run`, `check`, `setup`
- Handles user input and validation
- Displays Rich console output

#### 2. Configuration (`config_loader.py`)

- Loads and validates YAML config
- Schema validation
- Error handling for malformed configs

#### 3. Orchestrator (`orchestrator.py`)

- Coordinates tool execution
- Manages tool lifecycle
- Collects and normalizes results
- Generates reports

#### 4. Parsers (`core/parsers/`)

Each parser:
- Executes the security tool
- Parses tool-specific output format
- Converts to unified `Finding` schema
- Handles errors gracefully

#### 5. Schema (`schema.py`)

Defines core data models:
```python
@dataclass
class Finding:
    tool: str
    category: Category
    severity: Severity
    title: str
    description: str
    file_path: str
    line_number: int
    check_id: str
    references: List[str]
    remediation: str
    code_snippet: str

@dataclass
class ScanResult:
    metadata: dict
    findings: List[Finding]
    summary: dict
```

#### 6. Reporters (`core/reporters/`)

- **JSONReporter**: Structured JSON output
- **HTMLReporter**: Interactive web report (Jinja2)
- **SARIFReporter**: SARIF 2.1.0 compliant output

---

## 🔌 Adding a New Security Tool

### Step 1: Create Parser

Create `core/parsers/newtool_parser.py`:

```python
import subprocess
import json
from typing import List
from ..schema import Finding, Category, Severity

class NewToolParser:
    """Parser for NewTool security scanner."""
    
    def __init__(self):
        self.tool_name = "newtool"
        self.category = Category.SAST  # or SCA, IAC, SECRETS
    
    def run(self, args: List[str], cwd: str) -> List[Finding]:
        """Execute NewTool and parse results."""
        try:
            # Run the tool
            result = subprocess.run(
                [self.tool_name] + args,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False
            )
            
            # Parse output
            if result.returncode != 0 and not result.stdout:
                raise Exception(f"NewTool failed: {result.stderr}")
            
            # Convert to JSON
            data = json.loads(result.stdout)
            
            # Parse findings
            findings = []
            for item in data.get('issues', []):
                finding = Finding(
                    tool=self.tool_name,
                    category=self.category,
                    severity=self._map_severity(item['severity']),
                    title=item['title'],
                    description=item['description'],
                    file_path=item['file'],
                    line_number=item.get('line', 0),
                    check_id=item['rule_id'],
                    references=item.get('references', []),
                    remediation=item.get('fix', ''),
                    code_snippet=item.get('code', '')
                )
                findings.append(finding)
            
            return findings
            
        except Exception as e:
            raise Exception(f"NewTool parser error: {str(e)}")
    
    def _map_severity(self, tool_severity: str) -> Severity:
        """Map tool severity to unified severity."""
        mapping = {
            'critical': Severity.CRITICAL,
            'high': Severity.HIGH,
            'medium': Severity.MEDIUM,
            'low': Severity.LOW,
            'info': Severity.INFO
        }
        return mapping.get(tool_severity.lower(), Severity.MEDIUM)
```

### Step 2: Register Parser

Update `core/parsers/__init__.py`:
```python
from .newtool_parser import NewToolParser

__all__ = [
    'CheckovParser',
    'TrivyParser',
    'SemgrepParser',
    'GitleaksParser',
    'NewToolParser',  # Add this
]
```

### Step 3: Add to Orchestrator

Update `core/orchestrator.py`:
```python
from .parsers import NewToolParser

def _run_tool(self, tool_config):
    tool_map = {
        'checkov': CheckovParser,
        'trivy': TrivyParser,
        'semgrep': SemgrepParser,
        'gitleaks': GitleaksParser,
        'newtool': NewToolParser,  # Add this
    }
    # ...
```

### Step 4: Add Tool Installer

Update `core/utils/tool_installer.py`:
```python
def install_newtool(self) -> bool:
    """Install NewTool."""
    try:
        if self.platform == "darwin" or self.platform == "linux":
            subprocess.run(["brew", "install", "newtool"], check=True)
        return True
    except:
        return False
```

### Step 5: Update Configuration Schema

Add to example configs:
```yaml
tools:
  newtool:
    enabled: true
    runner: newtool
    args: ["--scan", "."]
```

---

## 🧪 Testing

### Manual Testing

```bash
# Test with example vulnerable code
python3 1security run --config examples/config-phase2.yaml

# Test individual tools
python3 1security run --config examples/config-sast.yaml

# Test tool installation
python3 1security check
python3 1security setup
```

### Test Vulnerable Code

Use `examples/vulnerable-app/` for testing:
- `app.py` - Python vulnerabilities (SQL injection, etc.)
- `server.js` - Node.js vulnerabilities
- `config.py` - Hardcoded secrets

### Validation Checklist

- [ ] Tool executes successfully
- [ ] Findings parsed correctly
- [ ] Severity mapping works
- [ ] JSON report valid
- [ ] HTML report renders
- [ ] SARIF report valid
- [ ] Error handling works
- [ ] Tool check/setup works

---

## 📝 Code Style

### Python Style Guide

- **PEP 8** compliance
- **Type hints** where appropriate
- **Docstrings** for all classes and methods
- **Comments** for complex logic

### Example:

```python
def parse_findings(self, data: dict) -> List[Finding]:
    """
    Parse tool output into Finding objects.
    
    Args:
        data: Raw tool output as dictionary
        
    Returns:
        List of Finding objects
        
    Raises:
        ParseError: If data format is invalid
    """
    findings = []
    # Implementation...
    return findings
```

---

## 🔍 Debugging

### Enable Verbose Output

```bash
# Add debug prints
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use rich inspect
from rich import inspect
inspect(finding, methods=True)
```

### Common Issues

**Tool not found:**
```python
# Check PATH
import shutil
print(shutil.which('checkov'))
```

**Parse errors:**
```python
# Print raw output
print(f"Tool output: {result.stdout}")
print(f"Tool errors: {result.stderr}")
```

**Severity mapping:**
```python
# Debug severity conversion
print(f"Original: {tool_severity}")
print(f"Mapped: {self._map_severity(tool_severity)}")
```

---

## 📊 Performance Considerations

### Optimization Tips

1. **Parallel Execution** - Tools run sequentially (could be parallelized)
2. **Caching** - Tool databases could be cached
3. **Incremental Scans** - Only scan changed files
4. **Result Caching** - Cache findings for unchanged files

### Current Bottlenecks

- Trivy database download (first run)
- Semgrep rule loading
- Large codebases

---

## 🚀 Release Process

### Version Numbering

Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Checklist

1. [ ] Update version in `core/__init__.py`
2. [ ] Update CHANGELOG.md
3. [ ] Test all features
4. [ ] Update documentation
5. [ ] Create git tag
6. [ ] Push to GitHub
7. [ ] Create GitHub release

### Version Update

```python
# core/__init__.py
__version__ = "0.3.0"
```

---

## 🎯 Roadmap

### Phase 3 (v0.3.0)

**Features:**
- Web dashboard (FastAPI + React)
- Finding deduplication
- Historical trending
- Custom policy engine
- Multi-repo scanning

**Technical:**
- Add SQLite/PostgreSQL storage
- REST API endpoints
- WebSocket for real-time updates
- Authentication system

---

## 📚 Resources

### Dependencies

- **Click**: CLI framework
- **Rich**: Terminal formatting
- **Jinja2**: HTML templating
- **PyYAML**: YAML parsing

### External Tools

- Checkov: https://www.checkov.io/
- Trivy: https://aquasecurity.github.io/trivy/
- Semgrep: https://semgrep.dev/
- Gitleaks: https://github.com/gitleaks/gitleaks

### Standards

- **SARIF**: https://sarifweb.azurewebsites.net/
- **CWE**: https://cwe.mitre.org/
- **CVE**: https://cve.mitre.org/
- **OWASP**: https://owasp.org/

---

## 🤝 Contributing

### Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes
4. Test thoroughly
5. Update documentation
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open Pull Request

### Commit Messages

```
feat: Add support for NewTool scanner
fix: Correct severity mapping for Trivy
docs: Update installation guide
refactor: Simplify parser architecture
test: Add tests for Semgrep parser
```

---

## 📞 Get Help

- **User Docs**: Other markdown files in `docs/`
- **Issues**: https://github.com/jaganraj/1security/issues
- **Discussions**: GitHub Discussions

---

**1Security v0.2.0** | MIT License | R Jagan Raj

