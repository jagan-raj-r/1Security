# 🚀 Quick Start Guide

Get 1Security up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Step 1: Installation

```bash
# Navigate to the project directory
cd /path/to/1security

# Install dependencies
pip install -r requirements.txt

# Install 1Security CLI
pip install -e .
```

## Step 2: Verify Installation

```bash
# Check if CLI is installed
1security --version

# Should output: 1security, version 0.1.0
```

## Step 3: Initialize Configuration

```bash
# Create a default config.yaml
1security init
```

This creates a `config.yaml` file in your current directory.

## Step 4: Run Your First Scan

### Option A: Scan Example Terraform Files

```bash
# Use the example configuration
cp examples/config.example.yaml config.yaml

# Run scan
1security run

# View HTML report
open reports/1security-report.html
```

### Option B: Scan Your Own Infrastructure Code

```bash
# Edit config.yaml to point to your code
# For example, to scan a specific directory:
vim config.yaml

# Update the args to scan your directory:
# args: ["-d", "./your-terraform-dir", "--framework", "terraform", "--output", "json", "--quiet"]

# Run scan
1security run
```

## Step 5: Understand the Output

After running a scan, you'll get:

1. **Console Summary** - Quick overview in your terminal
2. **JSON Report** - Machine-readable format at `reports/1security-report.json`
3. **HTML Report** - Beautiful web report at `reports/1security-report.html`

### Example Console Output

```
🔒 1Security - ASPM Orchestrator

📋 Loading configuration from: config.yaml
Running checkov...
✓ checkov completed (12 findings)

📝 Generating reports...

📊 Scan Summary

┏━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━┓
┃ Category ┃ Tool    ┃ Critical ┃ High ┃ Medium ┃ Low ┃ Info ┃ Total ┃
┡━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━┩
│ IAC      │ checkov │ 2        │ 5    │ 3      │ 2   │ 0    │ 12    │
└──────────┴─────────┴──────────┴──────┴────────┴─────┴──────┴───────┘

Total Findings: 12

📄 Reports Generated:
  • reports/1security-report.json
  • reports/1security-report.html
```

## Common Commands

```bash
# Run with custom config
1security run --config my-config.yaml

# Change output directory
1security run --output ./security-reports

# Generate only JSON report
1security run --format json

# Generate only HTML report
1security run --format html
```

## CLI Options

```
1security run [OPTIONS]

Options:
  -c, --config PATH   Path to configuration file [default: config.yaml]
  -o, --output PATH   Output directory for reports [default: reports]
  -f, --format TEXT   Output format: json, html, or both [default: both]
  --help             Show this message and exit
```

## Configuration Options

### Basic Configuration

```yaml
project: myapp
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
```

### Scanning Specific Frameworks

```yaml
# Terraform only
args: ["-d", ".", "--framework", "terraform", "--output", "json", "--quiet"]

# Kubernetes only
args: ["-d", ".", "--framework", "kubernetes", "--output", "json", "--quiet"]

# CloudFormation only
args: ["-d", ".", "--framework", "cloudformation", "--output", "json", "--quiet"]

# All frameworks (default)
args: ["-d", ".", "--output", "json", "--quiet"]
```

### Skip Specific Checks

```yaml
# Skip a specific check
args: ["-d", ".", "--skip-check", "CKV_AWS_19", "--output", "json", "--quiet"]

# Skip multiple checks
args: ["-d", ".", "--skip-check", "CKV_AWS_19,CKV_AWS_20", "--output", "json", "--quiet"]
```

## Troubleshooting

### Command Not Found

```bash
# If '1security' command is not found, try:
python -m pip install -e .

# Or run directly with Python:
python cli.py run
```

### Checkov Not Found

```bash
# Install Checkov
pip install checkov

# Verify installation
checkov --version
```

### No Findings in Report

This could mean:
1. ✅ Your code has no security issues (great!)
2. ⚠️ Checkov didn't find files to scan
3. ⚠️ Wrong directory or framework specified

Check your configuration and ensure you're pointing to the right directory.

## What's Next?

1. **Integrate into CI/CD** - Add to your GitHub Actions or GitLab CI
2. **Customize Rules** - Use Checkov's policy features
3. **Set Fail Thresholds** - Configure `fail_on` to fail builds on critical issues
4. **Explore Checkov** - Learn more at https://www.checkov.io/

## Need Help?

- Check the main [README.md](README.md)
- Review [examples/config.example.yaml](examples/config.example.yaml)
- Open an issue on GitHub

---

Happy Scanning! 🔒

