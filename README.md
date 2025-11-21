# 1Security — Open Source ASPM Orchestrator

![Version](https://img.shields.io/badge/version-0.1.0-blue)
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
brew install trivy           # For SCA scanning (macOS)
# See INSTALLATION.md for other platforms

# Install 1Security in development mode
pip install -e .
```

### Usage

```bash
# Initialize a new configuration
1security init

# Run security scans
1security run --config config.yaml

# View reports
open reports/1security-report.html
```

## 📋 Phase 1 MVP - IaC & SCA Scanning

The Phase 1 MVP includes **Infrastructure as Code (IaC)** scanning with **Checkov** and **Software Composition Analysis (SCA)** with **Trivy**.

### Features

✅ Command-line interface (`1security run`)  
✅ YAML-based configuration  
✅ **Checkov** integration for IaC scanning  
✅ **Trivy** integration for SCA/vulnerability scanning ⭐ NEW  
✅ Unified JSON output schema  
✅ HTML and JSON report generation  
✅ Severity-based filtering  
✅ Beautiful, modern HTML reports  
✅ Multi-tool scanning support  

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

### Phase 1 — IaC & SCA Scanning (✅ Current)
- [x] CLI with config loader
- [x] Checkov integration (IaC)
- [x] Trivy integration (SCA) ⭐ NEW
- [x] Unified output schema
- [x] JSON and HTML reports
- [x] Multi-tool support

### Phase 2 — Additional Tools (Coming Soon)
- [ ] Semgrep (SAST)
- [ ] Gitleaks (Secrets)
- [ ] Trivy container scanning
- [ ] SARIF export format
- [ ] GitHub Actions enhancement

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

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**R Jagan Raj**  
GitHub: [@jaganraj](https://github.com/jaganraj)

## 🙏 Acknowledgments

- [Checkov](https://www.checkov.io/) by Bridgecrew
- All open-source security tool maintainers

---

**Note**: This is a Phase 1 MVP focusing on IaC scanning with Checkov. More tools and features are coming soon!

