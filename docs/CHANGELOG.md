# Changelog

All notable changes to 1Security will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2025-11-21 - Phase 2 Complete 🎉

### 🎯 Major Release - Multi-Tool Security Platform

Phase 2 transforms 1Security from a dual-tool scanner into a comprehensive security platform with **4 major scanning categories**.

### ✨ Added

#### New Security Scanners
- **Semgrep Parser** - Static Application Security Testing (SAST)
  - Full Semgrep integration for code-level vulnerability detection
  - Support for all Semgrep rulesets (security-audit, OWASP Top 10, etc.)
  - CWE and OWASP mapping
  - Code snippet extraction
  - Multi-language support (Python, JavaScript, Java, Go, Ruby, etc.)

- **Gitleaks Parser** - Secrets Detection
  - Comprehensive secrets scanning across 100+ secret types
  - API keys (AWS, GitHub, Stripe, OpenAI, etc.)
  - Database credentials and connection strings
  - Private keys and certificates
  - Smart secret redaction in reports
  - Git history scanning support

#### New Report Format
- **SARIF Reporter** - Industry-standard output format
  - Full SARIF 2.1.0 specification compliance
  - GitHub Advanced Security integration
  - Azure DevOps compatibility
  - VS Code extension support
  - Rich metadata (CWE, CVE, OWASP, severity scores)

#### Enhanced CLI
- New output format options: `sarif` and `all`
- `--format all` generates JSON, HTML, and SARIF reports simultaneously
- Better error messages for missing tools

#### Example Files
- `examples/vulnerable-app/app.py` - Intentionally vulnerable Python application
- `examples/vulnerable-app/server.js` - Vulnerable Node.js application
- `examples/vulnerable-app/config.py` - Hardcoded secrets for testing
- `examples/config-sast.yaml` - SAST-only scanning configuration
- `examples/config-secrets.yaml` - Secrets detection configuration
- `examples/config-phase2.yaml` - Comprehensive all-tools configuration

#### Documentation
- `PHASE2_COMPLETE.md` - Complete Phase 2 achievement guide
- Updated `INSTALLATION.md` with Semgrep and Gitleaks setup
- Enhanced `README.md` with Phase 2 features
- Updated configuration examples

### 🔄 Changed

- **Version**: Updated from 0.1.0 to 0.2.0
- **CLI**: Format option now accepts 5 values: json, html, both, sarif, all
- **Orchestrator**: Extended to support 4 security tools (was 2)
- **HTML Reports**: Updated version footer to 0.2.0
- **Configuration Examples**: Updated with Phase 2 tools

### 📈 Improved

- **Security Coverage**: 100% increase (from 2 to 4 tool categories)
- **Vulnerability Detection**: 1000+ new security patterns via Semgrep
- **Secret Detection**: 100+ credential types via Gitleaks
- **Report Formats**: 50% increase (from 2 to 3 formats)
- **CI/CD Integration**: SARIF support for better platform integration

### 🏗️ Architecture Changes

```
New Parsers:
  core/parsers/semgrep_parser.py    (215 lines)
  core/parsers/gitleaks_parser.py   (211 lines)

New Reporters:
  core/reporters/sarif_reporter.py  (268 lines)

Updated Files:
  core/orchestrator.py              (Added tool mappings)
  cli.py                           (Enhanced format options)
  core/parsers/__init__.py         (Export new parsers)
  core/reporters/__init__.py       (Export SARIF reporter)
```

### 📊 Statistics

- **New Code**: ~1,000 lines
- **New Files**: 3 parsers + 3 examples + 1 reporter
- **New Configurations**: 3 example configs
- **Documentation**: 4 updated files + 1 new comprehensive guide

---

## [0.1.0] - 2025-11-20 - Phase 1 Complete ✅

### 🎯 Initial Release - IaC & SCA Scanning

First production-ready release of 1Security with Infrastructure as Code (IaC) and Software Composition Analysis (SCA) capabilities.

### ✨ Added

#### Core Features
- **CLI Interface** - Command-line tool with `init` and `run` commands
- **YAML Configuration** - Flexible configuration system
- **Orchestrator** - Coordinates multiple security tools
- **Unified Schema** - Standardized Finding and ScanResult models

#### Security Scanners
- **Checkov Parser** - Infrastructure as Code scanning
  - Terraform, CloudFormation, Kubernetes, ARM templates
  - 1000+ built-in policies
  - Severity mapping (CRITICAL to INFO)
  - Resource-level findings
  
- **Trivy Parser** - Software Composition Analysis
  - Dependency vulnerability scanning
  - Container image scanning
  - OS package vulnerabilities
  - Multi-language support (Python, Node.js, Java, Go, etc.)

#### Reporting
- **JSON Reporter** - Machine-readable structured output
- **HTML Reporter** - Beautiful web-based security reports
  - Modern UI with gradient design
  - Severity-based color coding
  - Sortable findings table
  - Summary dashboard

#### Configuration
- `config.yaml` - Main configuration file
- `examples/config.example.yaml` - Comprehensive example
- `examples/config-sca.yaml` - SCA-focused configuration
- `examples/config-multi.yaml` - Multi-tool scanning

#### Examples
- `examples/terraform/main.tf` - Vulnerable Terraform code
- `examples/python/requirements.txt` - Vulnerable dependencies
- `examples/python/app.py` - Vulnerable Flask application
- `examples/nodejs/package.json` - Vulnerable Node.js dependencies

#### Documentation
- `README.md` - Complete project documentation
- `QUICKSTART.md` - 5-minute getting started guide
- `MVP_COMPLETE.md` - Phase 1 completion summary
- `TRIVY_INTEGRATION.md` - Trivy setup and usage guide
- `INSTALLATION.md` - Installation instructions
- `LICENSE` - MIT License

### 🏗️ Project Structure

```
1security/
├── 1security                    # CLI executable
├── cli.py                       # CLI implementation
├── setup.py                     # Package setup
├── requirements.txt             # Dependencies
├── core/
│   ├── __init__.py
│   ├── orchestrator.py          # Main coordinator
│   ├── config_loader.py         # YAML config loader
│   ├── schema.py                # Data models
│   ├── constants.py             # Constants
│   ├── exceptions.py            # Custom exceptions
│   ├── parsers/
│   │   ├── checkov_parser.py
│   │   └── trivy_parser.py
│   ├── reporters/
│   │   ├── json_reporter.py
│   │   └── html_reporter.py
│   └── utils/
│       ├── file_utils.py
│       └── severity_utils.py
└── examples/
    ├── terraform/
    ├── python/
    └── nodejs/
```

### 📦 Dependencies

- `pyyaml>=6.0` - YAML configuration parsing
- `click>=8.1.0` - CLI framework
- `jinja2>=3.1.0` - HTML template rendering
- `rich>=13.0.0` - Beautiful terminal output
- `checkov>=3.0.0` - IaC scanning

### 🎯 Features Delivered

✅ Multi-tool orchestration  
✅ Unified output schema  
✅ Beautiful reports (HTML + JSON)  
✅ Severity-based filtering  
✅ Exit codes based on findings  
✅ Progress indicators  
✅ Comprehensive documentation  
✅ Example vulnerable code  
✅ CI/CD ready  

---

## Release Strategy

### Version Numbering

- **Major** (X.0.0): Breaking changes, major features
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, minor improvements

### Release Phases

- **Phase 1 (v0.1.0)**: IaC + SCA scanning ✅
- **Phase 2 (v0.2.0)**: SAST + Secrets + SARIF ✅
- **Phase 3 (v0.3.0)**: Web dashboard, policy engine (planned)
- **v1.0.0**: Production stable with all Phase 3 features

---

## Upcoming (Phase 3)

### Planned Features

- [ ] Web Dashboard (FastAPI + React)
- [ ] Historical Trending
- [ ] Finding Deduplication
- [ ] Custom Policy Engine
- [ ] Multi-Repo Scanning
- [ ] Notification Integrations (Slack, Jira, email)
- [ ] Risk Scoring System
- [ ] Compliance Reporting (SOC2, PCI-DSS)
- [ ] User Authentication & Authorization
- [ ] API Endpoints
- [ ] Database Backend
- [ ] Scheduled Scans

---

## Links

- **Homepage**: https://github.com/jaganraj/1security
- **Issues**: https://github.com/jaganraj/1security/issues
- **Releases**: https://github.com/jaganraj/1security/releases

---

## Contributors

- **R Jagan Raj** - Creator and maintainer

---

## License

MIT License - See LICENSE file for details
