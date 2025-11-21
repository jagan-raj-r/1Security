# 1Security — Open Source ASPM Orchestrator

![Version](https://img.shields.io/badge/version-0.2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)

**1Security** is a lightweight, open-source **Application Security Posture Management (ASPM)** tool that unifies the best security scanners into a single, developer-friendly platform.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/jaganraj/1security.git
cd 1security

# Install dependencies
pip install -r requirements.txt

# Install security scanners
pip install checkov          # For IaC scanning
pip install semgrep          # For SAST scanning (NEW)
brew install trivy           # For SCA scanning (macOS)
brew install gitleaks        # For secrets detection (NEW)
# See INSTALLATION.md for other platforms

# Install 1Security in development mode
pip install -e .
```

### Usage

```bash
# Initialize a new configuration (with automatic tool setup!)
1security init

# Check which tools are installed
1security check

# Install missing tools automatically
1security setup

# Run security scans (auto-checks tools before scanning)
1security run --config config.yaml

# View reports
open reports/1security-report.html
```

### ⭐ **NEW: Automatic Tool Management**

1Security now **automatically detects and installs** required security tools!

```bash
# One command to set up everything
1security setup --yes

# Or let init guide you through setup
1security init
```

No more manual tool installation! See [docs/TOOL_MANAGEMENT.md](docs/TOOL_MANAGEMENT.md) for details.

### ⭐ **NEW: Interactive Report Filtering**

HTML reports now include powerful **client-side filtering**!

**Filter by:**
- 🔧 Tool (Checkov, Trivy, Semgrep, Gitleaks)
- ⚠️ Severity (Critical, High, Medium, Low, Info)
- 📋 Category (IaC, SCA, SAST, Secrets)
- 🔍 Search (keywords, files, check IDs)

**Features:**
- ✅ Instant filtering (no page reload)
- ✅ Combine multiple filters
- ✅ Keyboard shortcuts (Ctrl+K for search)
- ✅ Live stats counter
- ✅ Beautiful, responsive UI

See [docs/REPORT_FILTERING.md](docs/REPORT_FILTERING.md) for details and examples.

## 📋 Phase 2 - Multi-Tool Security Platform ⭐ NEW

**Phase 2 is now COMPLETE!** 1Security now includes comprehensive security scanning across multiple categories.

### Features

✅ Command-line interface (`1security run`)  
✅ YAML-based configuration  
✅ **Checkov** integration for IaC scanning  
✅ **Trivy** integration for SCA/vulnerability scanning  
✅ **Semgrep** integration for SAST (Static Analysis) ⭐ NEW  
✅ **Gitleaks** integration for secrets detection ⭐ NEW  
✅ **SARIF** export format ⭐ NEW  
✅ **Automatic tool detection & installation** ⭐ NEW  
✅ **Interactive filtering in HTML reports** ⭐ NEW  
✅ Unified JSON output schema  
✅ HTML, JSON, and SARIF report generation  
✅ Severity-based filtering  
✅ Beautiful, modern HTML reports  
✅ Multi-tool scanning support (4+ tools)  

### Example Configuration

```yaml
project: myapp
language: python

tools:
  # IaC scanning with Checkov
  iac:
    enabled: true
    runner: checkov
    args: ["-d", ".", "--framework", "terraform", "--output", "json", "--quiet"]
  
  # SCA scanning with Trivy
  sca:
    enabled: true
    runner: trivy
    args: ["fs", ".", "--scanners", "vuln", "--format", "json", "--quiet"]

output:
  format: both  # json, html, or both
  report_path: reports/
  fail_on: critical
```

### Running a Scan

```bash
# Scan current directory
1security run

# Specify custom config
1security run --config my-config.yaml

# Change output directory
1security run --output ./security-reports

# Generate only JSON report
1security run --format json
```

## 🧩 Project Structure

```
1security/
├── cli.py                      # Command-line interface
├── setup.py                    # Package setup
├── requirements.txt            # Python dependencies
├── core/
│   ├── orchestrator.py        # Main orchestration logic
│   ├── config_loader.py       # YAML config loader
│   ├── schema.py              # Unified output schema
│   ├── parsers/
│   │   └── checkov_parser.py  # Checkov output parser
│   └── reporters/
│       ├── json_reporter.py   # JSON report generator
│       └── html_reporter.py   # HTML report generator
└── examples/
    ├── config.example.yaml    # Example configuration
    └── terraform/             # Example Terraform files
        └── main.tf
```

## 📊 Output Schema

All findings are normalized to a unified schema:

```json
{
  "tool": "checkov",
  "category": "iac",
  "severity": "HIGH",
  "title": "Ensure S3 bucket has encryption enabled",
  "description": "S3 bucket does not have encryption enabled",
  "file": "terraform/main.tf",
  "line": 15,
  "resource": "aws_s3_bucket.example",
  "rule_id": "CKV_AWS_19",
  "check_id": "CKV_AWS_19",
  "recommendation": "Enable S3 bucket encryption"
}
```

## 🎯 Roadmap

### Phase 1 — IaC & SCA Scanning (✅ Complete)
- [x] CLI with config loader
- [x] Checkov integration (IaC)
- [x] Trivy integration (SCA)
- [x] Unified output schema
- [x] JSON and HTML reports
- [x] Multi-tool support

### Phase 2 — Additional Security Tools (✅ Complete)
- [x] Semgrep (SAST) ⭐ NEW
- [x] Gitleaks (Secrets) ⭐ NEW
- [x] SARIF export format ⭐ NEW
- [x] Enhanced configuration
- [x] Comprehensive examples

### Phase 3 — Advanced Features
- [ ] Web dashboard (FastAPI + React)
- [ ] Policy engine
- [ ] Deduplication and correlation
- [ ] CI/CD integrations (GitLab, Jenkins)
- [ ] Slack/Jira notifications
- [ ] Plugin system

## 🧪 Testing

Try it out with the example Terraform files:

```bash
# Copy example config
cp examples/config.example.yaml config.yaml

# Run scan on example Terraform files
1security run

# View the report
open reports/1security-report.html
```

The example Terraform files intentionally contain security issues to demonstrate Checkov's capabilities.

## 🔧 Requirements

**Python Dependencies:**
- Python 3.8+
- Checkov 3.0+
- PyYAML
- Click
- Jinja2
- Rich

**Security Scanners:**
- Checkov (IaC) - `pip install checkov`
- Trivy (SCA) - `brew install trivy` or see [INSTALLATION.md](INSTALLATION.md)
- Semgrep (SAST) - `pip install semgrep`
- Gitleaks (Secrets) - `brew install gitleaks`

## 📝 Configuration Options

### Checkov Arguments

Common Checkov arguments you can use:

- `-d <directory>` - Directory to scan
- `--framework <name>` - Specific framework (terraform, cloudformation, kubernetes, etc.)
- `--output json` - Output format (required)
- `--quiet` - Suppress progress output
- `--check <check_id>` - Run specific checks
- `--skip-check <check_id>` - Skip specific checks
- `--soft-fail` - Don't exit with error code

### Output Configuration

- `format`: `json`, `html`, or `both`
- `report_path`: Directory for reports
- `fail_on`: Severity threshold (`critical`, `high`, `medium`, `low`, `info`)

## 🤝 Contributing

Contributions are welcome! This is Phase 1 MVP, and we'd love help adding:

- Additional tool integrations
- Enhanced reporting
- Policy engine
- CI/CD templates
- Documentation

## 📚 Documentation

**Complete, organized documentation** in the [`docs/`](docs/) directory:

| Document | Description | For |
|----------|-------------|-----|
| [**Getting Started**](docs/GETTING_STARTED.md) | Install, setup, first scan | New users (10 min) |
| [**User Guide**](docs/USER_GUIDE.md) | Commands, configs, workflows | Daily usage (20 min) |
| [**Features**](docs/FEATURES.md) | All capabilities explained | Understanding 1Security (15 min) |
| [**Tools**](docs/TOOLS.md) | Deep dive: Checkov, Trivy, Semgrep, Gitleaks | Tool-specific questions (30 min) |
| [**Development**](docs/DEVELOPMENT.md) | Architecture, contributing | Contributors (20 min) |
| [**Changelog**](docs/CHANGELOG.md) | Version history | Tracking updates |

### Quick Links

- **New to 1Security?** → [Getting Started](docs/GETTING_STARTED.md)
- **Need a command?** → [User Guide](docs/USER_GUIDE.md#quick-command-reference)
- **What can it do?** → [Features](docs/FEATURES.md)
- **Tool questions?** → [Tools Guide](docs/TOOLS.md)

👉 **[Documentation Index](docs/README.md)** - Complete navigation guide

---

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**R Jagan Raj**  
GitHub: [@jaganraj](https://github.com/jaganraj)

## 🙏 Acknowledgments

Thanks to the amazing open-source security tools:
- [**Checkov**](https://www.checkov.io/) by Bridgecrew
- [**Trivy**](https://aquasecurity.github.io/trivy/) by Aqua Security
- [**Semgrep**](https://semgrep.dev/) by Semgrep Inc.
- [**Gitleaks**](https://github.com/gitleaks/gitleaks) by Zachary Rice

---

**Phase 2 Complete!** - v0.2.0 includes IaC, SCA, SAST, and Secrets detection all in one platform. 🚀

