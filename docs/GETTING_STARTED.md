# 🚀 Getting Started with 1Security

Complete guide to install, set up, and run your first security scan in under 10 minutes.

---

## 📋 Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- **macOS** or **Linux** (Windows WSL2 supported)

---

## ⚡ Quick Install (Recommended)

### Step 1: Install 1Security

```bash
cd "/path/to/1Security"

# Install 1Security
pip install -e .

# Verify installation
1security --version
# Output: 1security, version 0.2.0
```

### Step 2: Initialize Configuration

```bash
1security init
```

This creates `config.yaml` and offers to install security tools automatically.

### Step 3: Run Your First Scan

```bash
# Scan with default config
1security run

# View HTML report
open reports/1security-report.html
```

**That's it!** You're scanning for security issues. 🎉

---

## 🔧 Manual Setup (If Needed)

If automatic tool installation doesn't work, install tools manually:

### Install Security Tools

#### Checkov (IaC Scanner)
```bash
pip install checkov
checkov --version
```

#### Trivy (SCA Scanner)
```bash
# macOS
brew install trivy

# Linux (Homebrew)
brew install trivy

# Verify
trivy --version
```

#### Semgrep (SAST Scanner)
```bash
pip install semgrep
semgrep --version
```

#### Gitleaks (Secrets Detection)
```bash
# macOS
brew install gitleaks

# Linux (Homebrew)
brew install gitleaks

# Verify
gitleaks version
```

---

## 🎯 Automatic Tool Management

1Security can automatically check and install required tools!

### Check Tool Status

```bash
1security check
```

**Output:**
```
🔍 Checking required security tools...

┏━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Tool     ┃ Category      ┃ Status     ┃ Version  ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Checkov  │ IaC Scanner   │ ✅ Installed │ 3.2.1   │
│ Trivy    │ SCA Scanner   │ ❌ Missing   │ -       │
│ Semgrep  │ SAST Scanner  │ ✅ Installed │ 1.144.0 │
│ Gitleaks │ Secrets       │ ❌ Missing   │ -       │
└──────────┴───────────────┴────────────┴──────────┘
```

### Install Missing Tools

```bash
# Interactive installation
1security setup

# Or auto-install everything
1security setup --yes
```

The setup command will:
1. Check which tools are needed (based on your config)
2. Detect what's already installed
3. Install missing tools automatically
4. Verify installations

---

## 📝 Configuration Basics

### Default Configuration

When you run `1security init`, it creates:

```yaml
project: myapp
language: python

tools:
  iac:
    enabled: true
    runner: checkov
    args: ["-d", ".", "--output", "json", "--quiet"]
  
  sca:
    enabled: true
    runner: trivy
    args: ["fs", ".", "--scanners", "vuln", "--format", "json", "--quiet"]

output:
  format: html
  report_path: reports/
  fail_on: high
```

### Configuration Templates

1Security provides ready-to-use templates in `examples/`:

```bash
# IaC + SCA (default)
cp examples/config.example.yaml config.yaml

# SCA only (dependencies)
cp examples/config-sca.yaml config.yaml

# SAST only (code security)
cp examples/config-sast.yaml config.yaml

# Secrets only (credentials)
cp examples/config-secrets.yaml config.yaml

# Everything (comprehensive)
cp examples/config-phase2.yaml config.yaml
```

---

## 🎨 Scan Examples

### Example 1: Quick Security Check

```bash
# Use default config
1security run
```

### Example 2: Comprehensive Scan

```bash
# Run all security tools
1security run --config examples/config-phase2.yaml --format all

# Generates:
# - reports/1security-report.json
# - reports/1security-report.html  
# - reports/1security-report.sarif
```

### Example 3: Focus on Secrets

```bash
# Scan for hardcoded credentials
1security run --config examples/config-secrets.yaml
```

### Example 4: Custom Output

```bash
# Save reports in custom directory
1security run --output ./security-scans

# JSON format only
1security run --format json

# HTML format only
1security run --format html
```

---

## 📊 Understanding Reports

### Console Output

```
🔒 1Security v0.2.0 - ASPM Orchestrator

📋 Loading configuration from: config.yaml
Running checkov...
✓ checkov completed (12 findings)
Running trivy...
✓ trivy completed (102 findings)

📝 Generating reports...

📊 Scan Summary

┏━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━┓
┃ Category ┃ Tool    ┃ Critical ┃ High ┃ Medium ┃ Low ┃ Info ┃ Total ┃
┡━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━┩
│ IAC      │ checkov │ 2        │ 5    │ 3      │ 2   │ 0    │ 12    │
│ SCA      │ trivy   │ 15       │ 47   │ 32     │ 8   │ 0    │ 102   │
└──────────┴─────────┴──────────┴──────┴────────┴─────┴──────┴───────┘

Total Findings: 114

📄 Reports Generated:
  • reports/1security-report.json
  • reports/1security-report.html
```

### HTML Report Features

The HTML report includes:
- **Summary Dashboard** - Severity breakdown and statistics
- **Interactive Filters** - Filter by tool, severity, category
- **Search Function** - Find specific findings
- **Detailed Findings** - Full description, remediation, references
- **Color-Coded Badges** - Visual severity indicators

### JSON Report Structure

```json
{
  "metadata": {
    "tool": "1security",
    "version": "0.2.0",
    "scan_time": "2025-11-21T12:00:00Z"
  },
  "summary": {
    "total": 114,
    "by_severity": {
      "critical": 17,
      "high": 52,
      "medium": 35,
      "low": 10
    }
  },
  "findings": [...]
}
```

### SARIF Report

SARIF format is ideal for:
- GitHub Advanced Security
- Azure DevOps
- VS Code SARIF Viewer
- CI/CD integrations

---

## 🔧 Common Commands

```bash
# Initialize configuration
1security init

# Check tool installation
1security check

# Install missing tools
1security setup

# Run scan (default config)
1security run

# Run with custom config
1security run --config my-config.yaml

# Custom output directory
1security run --output ./scans

# Specific output format
1security run --format json          # JSON only
1security run --format html          # HTML only
1security run --format sarif         # SARIF only
1security run --format all           # All formats

# Skip tool check (faster)
1security run --skip-tool-check

# Get version
1security --version

# Get help
1security --help
1security run --help
```

---

## 🐛 Troubleshooting

### Command not found: 1security

**Solution:**
```bash
# Use Python directly
python3 1security run

# Or reinstall
pip install -e .
```

### Tool not found errors

**Solution:**
```bash
# Check what's missing
1security check

# Install missing tools
1security setup

# Or install manually (see Manual Setup section above)
```

### No findings in report

**Possible reasons:**
1. ✅ Your code is secure (great!)
2. ⚠️  Wrong directory scanned
3. ⚠️  Tool not finding relevant files

**Check:**
```bash
# Verify you're in the right directory
pwd

# Check config points to correct paths
cat config.yaml

# Verify tools work independently
checkov --version
trivy --version
```

### Permission errors

**Solution:**
```bash
# Install for user only
pip install --user -e .

# Make script executable
chmod +x 1security
```

### Slow scans

**Optimization:**
```yaml
# Exclude large directories
sca:
  enabled: true
  runner: trivy
  args: ["fs", ".", "--skip-dirs", "node_modules,vendor"]

# Use specific severity filters
args: ["--severity", "CRITICAL,HIGH"]
```

---

## ✅ Verification Checklist

Before your first scan, verify:

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] 1Security installed (`1security --version`)
- [ ] At least one security tool installed (`1security check`)
- [ ] Config file exists (`ls config.yaml`)
- [ ] In the right directory to scan
- [ ] Reports directory accessible

---

## 🎯 Next Steps

Now that you're set up:

1. **Read [USER_GUIDE.md](USER_GUIDE.md)** - Learn all commands and features
2. **Check [TOOLS.md](TOOLS.md)** - Deep dive into each security tool
3. **Review [FEATURES.md](FEATURES.md)** - Explore advanced capabilities
4. **See example configs** in `examples/` directory
5. **Integrate into CI/CD** for automated scanning

---

## 💡 Pro Tips

1. **Start Simple**: Begin with one tool, add more gradually
2. **Use Templates**: Copy from `examples/` instead of writing from scratch
3. **Automatic Setup**: Let `1security init` handle everything
4. **Regular Scans**: Run daily or on every commit
5. **Read Reports**: HTML reports are designed for human review
6. **Tune Gradually**: Adjust severity thresholds as your team adapts

---

## 📞 Need Help?

- **Quick Reference**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Tool Details**: See [TOOLS.md](TOOLS.md)
- **Features**: See [FEATURES.md](FEATURES.md)
- **Changelog**: See [CHANGELOG.md](CHANGELOG.md)
- **Issues**: Open an issue on GitHub

---

**You're all set!** Start scanning and making your applications more secure. 🔒

---

**1Security v0.2.0** | MIT License | R Jagan Raj

