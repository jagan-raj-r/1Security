# 📖 1Security User Guide

Complete reference for using 1Security - all commands, configurations, and workflows.

---

## 🎯 Quick Command Reference

```bash
# Core Commands
1security init              # Create config.yaml
1security run              # Run security scan
1security check            # Verify tool installation
1security setup            # Install security tools
1security --version        # Show version
1security --help           # Show help

# Run with Options
1security run --config my-config.yaml        # Custom config
1security run --output ./reports             # Custom output dir
1security run --format json                  # JSON only
1security run --format html                  # HTML only
1security run --format sarif                 # SARIF only
1security run --format all                   # All formats
1security run --skip-tool-check              # Skip tool verification
```

---

## 🛡️ Security Tools Overview

| Tool | Category | Purpose | Finds |
|------|----------|---------|-------|
| **Checkov** | IaC | Infrastructure misconfigurations | Unencrypted resources, public access, weak policies |
| **Trivy** | SCA | Vulnerable dependencies | CVEs in libraries, outdated packages, exploits |
| **Semgrep** | SAST | Code security issues | SQL injection, XSS, command injection, weak crypto |
| **Gitleaks** | Secrets | Hardcoded credentials | API keys, passwords, tokens, certificates |

---

## 📋 Configuration Guide

### Basic Configuration Structure

```yaml
project: myapp           # Project name
language: python         # Primary language (optional)

tools:
  iac:                   # Infrastructure scanning
    enabled: true
    runner: checkov
    args: [...]
  
  sca:                   # Dependency scanning
    enabled: true
    runner: trivy
    args: [...]
  
  sast:                  # Code scanning
    enabled: true
    runner: semgrep
    args: [...]
  
  secrets:               # Secret scanning
    enabled: true
    runner: gitleaks
    args: [...]

output:
  format: html          # json, html, both, sarif, all
  report_path: reports/ # Output directory
  fail_on: high         # critical, high, medium, low, info
```

### Configuration Templates

#### IaC Only (Infrastructure)
```yaml
project: myapp
tools:
  iac:
    enabled: true
    runner: checkov
    args: ["-d", ".", "--framework", "terraform", "--output", "json", "--quiet"]
output:
  format: html
  fail_on: high
```

#### SCA Only (Dependencies)
```yaml
project: myapp
tools:
  sca:
    enabled: true
    runner: trivy
    args: ["fs", ".", "--scanners", "vuln", "--format", "json", "--quiet"]
output:
  format: html
  fail_on: critical
```

#### SAST Only (Code Security)
```yaml
project: myapp
tools:
  sast:
    enabled: true
    runner: semgrep
    args: ["--config", "p/security-audit", "--json", "--quiet", "."]
output:
  format: html
  fail_on: high
```

#### Secrets Only (Credentials)
```yaml
project: myapp
tools:
  secrets:
    enabled: true
    runner: gitleaks
    args: ["detect", "--source", ".", "--report-format", "json", "--no-git"]
output:
  format: html
  fail_on: high
```

#### Comprehensive (All Tools)
```yaml
project: myapp
tools:
  iac:
    enabled: true
    runner: checkov
    args: ["-d", ".", "--output", "json", "--quiet"]
  sca:
    enabled: true
    runner: trivy
    args: ["fs", ".", "--scanners", "vuln", "--format", "json", "--quiet"]
  sast:
    enabled: true
    runner: semgrep
    args: ["--config", "p/security-audit", "--json", "--quiet", "."]
  secrets:
    enabled: true
    runner: gitleaks
    args: ["detect", "--source", ".", "--report-format", "json", "--no-git"]
output:
  format: all
  fail_on: high
```

---

## ⚙️ Tool-Specific Arguments

### Checkov (IaC)

```yaml
# Scan specific directory
args: ["-d", "./terraform", "--output", "json", "--quiet"]

# Specific framework
args: ["-d", ".", "--framework", "terraform", "--output", "json"]
args: ["-d", ".", "--framework", "kubernetes", "--output", "json"]

# Skip specific checks
args: ["-d", ".", "--skip-check", "CKV_AWS_19", "--output", "json"]

# Multiple frameworks
args: ["-d", ".", "--framework", "terraform,kubernetes", "--output", "json"]
```

### Trivy (SCA)

```yaml
# Scan filesystem
args: ["fs", ".", "--scanners", "vuln", "--format", "json", "--quiet"]

# Filter by severity
args: ["fs", ".", "--severity", "CRITICAL,HIGH", "--format", "json"]

# Ignore unfixed vulnerabilities
args: ["fs", ".", "--ignore-unfixed", "--format", "json"]

# Skip directories
args: ["fs", ".", "--skip-dirs", "node_modules,vendor", "--format", "json"]

# Scan container image
args: ["image", "myapp:latest", "--format", "json"]
```

### Semgrep (SAST)

```yaml
# Security audit ruleset (comprehensive)
args: ["--config", "p/security-audit", "--json", "--quiet", "."]

# OWASP Top 10 only
args: ["--config", "p/owasp-top-ten", "--json", "--quiet", "."]

# CWE Top 25
args: ["--config", "p/cwe-top-25", "--json", "--quiet", "."]

# Auto-detect language-specific rules
args: ["--config", "auto", "--json", "--quiet", "."]

# Exclude directories
args: ["--config", "p/security-audit", "--exclude", "tests,vendor", "--json", "."]

# Custom timeout
args: ["--config", "p/security-audit", "--timeout", "30", "--json", "."]
```

### Gitleaks (Secrets)

```yaml
# Standard scan
args: ["detect", "--source", ".", "--report-format", "json", "--no-git"]

# With git history
args: ["detect", "--source", ".", "--report-format", "json"]

# Verbose output
args: ["detect", "--source", ".", "--report-format", "json", "--verbose"]

# Custom config
args: ["detect", "--source", ".", "--config", ".gitleaks.toml", "--report-format", "json"]
```

---

## 📊 Output Formats

### JSON Format
```bash
1security run --format json
```

**Use for:**
- CI/CD automation
- API integration
- Programmatic processing
- Historical tracking

**Output:** `reports/1security-report.json`

### HTML Format
```bash
1security run --format html
```

**Use for:**
- Human review
- Team meetings
- Security reports
- Executive summaries

**Features:**
- Interactive filtering (by tool, severity, category)
- Search functionality
- Color-coded severity badges
- Summary dashboard

**Output:** `reports/1security-report.html`

### SARIF Format
```bash
1security run --format sarif
```

**Use for:**
- GitHub Advanced Security
- Azure DevOps
- VS Code SARIF Viewer
- IDE integrations

**Output:** `reports/1security-report.sarif`

### All Formats
```bash
1security run --format all
```

Generates all three formats simultaneously.

---

## 🎯 Common Workflows

### Workflow 1: Daily Development

```bash
# Morning: Quick secrets check
1security run --config config-secrets.yaml

# Before commit: Code scan
1security run --config config-sast.yaml
```

### Workflow 2: Pull Request Review

```bash
# Comprehensive scan
1security run --config config-phase2.yaml --format html

# Review HTML report
open reports/1security-report.html
```

### Workflow 3: Release Preparation

```bash
# Full security audit
1security run --config config-phase2.yaml --format all

# Review all findings
open reports/1security-report.html

# Upload SARIF to GitHub
gh api repos/$REPO/code-scanning/sarifs \
  -F sarif=@reports/1security-report.sarif
```

### Workflow 4: CI/CD Integration

```bash
# In CI pipeline
1security setup --yes                    # Install tools
1security run --format sarif             # Generate SARIF
# Upload to code scanning platform
```

### Workflow 5: Incremental Scanning

```bash
# Day 1: Infrastructure
1security run --config config-iac.yaml

# Day 2: Dependencies  
1security run --config config-sca.yaml

# Day 3: Code security
1security run --config config-sast.yaml

# Day 4: Secrets
1security run --config config-secrets.yaml

# Day 5: Everything
1security run --config config-phase2.yaml
```

---

## 🔐 Severity Levels

| Severity | Description | Typical Issues | Fix Timeline |
|----------|-------------|----------------|--------------|
| **CRITICAL** | Severe security risk | Hardcoded secrets, RCE vulnerabilities | Immediately |
| **HIGH** | Significant risk | SQL injection, auth bypass | Within 24 hours |
| **MEDIUM** | Moderate risk | XSS, weak encryption | Within 1 week |
| **LOW** | Minor risk | Info disclosure, deprecated APIs | Within 1 month |
| **INFO** | Informational | Best practices, recommendations | Optional |

### Fail Thresholds

```yaml
output:
  fail_on: critical    # Fail only on CRITICAL
  fail_on: high        # Fail on HIGH and above
  fail_on: medium      # Fail on MEDIUM and above
  fail_on: low         # Fail on LOW and above
  fail_on: info        # Fail on any finding
```

---

## 📈 HTML Report Features

### Interactive Filtering

**Filter by Tool:**
```
Buttons: All Tools | Checkov | Trivy | Semgrep | Gitleaks
```

**Filter by Severity:**
```
Buttons: All | Critical | High | Medium | Low | Info
```

**Filter by Category:**
```
Buttons: All | IaC | SCA | SAST | Secrets
```

**Search:**
```
Search box: Find by keyword in title, file, or description
```

**Combine Filters:**
- Click "Semgrep" + "Critical" = Only critical Semgrep findings
- Search "SQL" + "High" severity = High-severity SQL issues

### Keyboard Shortcuts

- **Ctrl/Cmd + F**: Focus search box
- **Esc**: Clear all filters
- **Click badge**: Quick filter by severity

---

## 🔧 Tool Management Commands

### Check Installation Status

```bash
1security check
```

Shows:
- Which tools are installed
- Tool versions
- What's missing

### Install Missing Tools

```bash
# Interactive (prompts for each tool)
1security setup

# Automatic (install all)
1security setup --yes

# For specific config
1security setup --config my-config.yaml
```

### Skip Tool Check (Performance)

```bash
# When you know tools are installed
1security run --skip-tool-check
```

---

## 🎨 Advanced Configuration

### Multiple Directories

```yaml
iac:
  enabled: true
  runner: checkov
  args: ["-d", "./terraform,./kubernetes", "--output", "json"]
```

### Custom Output Directory

```bash
1security run --output ./security-reports
```

### Environment-Specific Configs

```bash
# Development
1security run --config config-dev.yaml

# Staging
1security run --config config-staging.yaml

# Production
1security run --config config-prod.yaml
```

### Exclude Patterns

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", ".", "--skip-dirs", "test,vendor,node_modules"]

sast:
  enabled: true
  runner: semgrep
  args: ["--config", "p/security-audit", "--exclude", "tests,docs", "--json", "."]
```

---

## 📊 CI/CD Integration Examples

### GitHub Actions

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install 1Security
        run: |
          pip install -e .
          1security setup --yes
      
      - name: Run Security Scan
        run: 1security run --format sarif
      
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: reports/1security-report.sarif
```

### GitLab CI

```yaml
security_scan:
  image: python:3.9
  script:
    - pip install -e .
    - 1security setup --yes
    - 1security run --format all
  artifacts:
    paths:
      - reports/
    reports:
      sast: reports/1security-report.sarif
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔒 Running security scans..."
1security run --config config-secrets.yaml

if [ $? -ne 0 ]; then
    echo "❌ Security issues found! Fix before committing."
    exit 1
fi

echo "✅ Security checks passed!"
```

---

## 🐛 Troubleshooting Guide

### No Findings

**Possible causes:**
1. Code is secure (good!)
2. Wrong directory
3. Tool not recognizing files

**Solutions:**
```bash
# Check current directory
pwd

# Verify config paths
cat config.yaml

# Test tools individually
checkov -d .
trivy fs .
semgrep --config auto .
gitleaks detect --source .
```

### Too Many Findings

**Solutions:**
```yaml
# Filter by severity
output:
  fail_on: critical

# Exclude directories
sca:
  args: ["fs", ".", "--skip-dirs", "node_modules"]

# Use focused rulesets
sast:
  args: ["--config", "p/owasp-top-ten", "--json", "."]
```

### Slow Scans

**Optimizations:**
```yaml
# Exclude large directories
--skip-dirs node_modules,vendor,.git

# Limit scope
-d ./src  # Only scan src directory

# Use severity filters
--severity CRITICAL,HIGH

# Timeout controls
--timeout 30
```

### Tool Not Found

```bash
# Check installation
1security check

# Install missing tools
1security setup

# Or install manually
pip install checkov semgrep
brew install trivy gitleaks
```

---

## 💡 Best Practices

### 1. Start Small, Scale Up

```
Week 1: Secrets detection
Week 2: Add SAST
Week 3: Add SCA
Week 4: Full comprehensive scan
```

### 2. Tune for Your Team

```yaml
# Don't overwhelm - start with high severity
output:
  fail_on: high

# Gradually lower threshold
output:
  fail_on: medium  # After team adapts
```

### 3. Regular Scanning

```
Pre-commit: Secrets (fast)
Pre-push: SAST (medium)
PR: All tools (comprehensive)
Nightly: Full audit with all findings
```

### 4. Use Templates

```bash
# Don't write configs from scratch
cp examples/config-phase2.yaml config.yaml

# Modify as needed
```

### 5. Review Reports Together

- Weekly security review meetings
- Use HTML reports for team discussions
- Track trends over time

---

## 📞 Get Help

- **Getting Started**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Tool Details**: [TOOLS.md](TOOLS.md)
- **Features**: [FEATURES.md](FEATURES.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Examples**: `examples/` directory

---

**1Security v0.2.0** | MIT License | R Jagan Raj

