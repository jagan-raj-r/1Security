# 🛡️ Trivy Integration Guide

**Status:** ✅ **IMPLEMENTED** (v0.1.0)

---

## 🎯 Overview

Trivy is now integrated into 1Security for **Software Composition Analysis (SCA)** scanning! Trivy scans your dependencies, containers, and code for known vulnerabilities.

---

## 📦 What is Trivy?

**Trivy** is a comprehensive security scanner by Aqua Security that finds:
- 🔍 **Vulnerabilities** in OS packages and language dependencies
- 📦 **Container images** security issues
- 🔧 **IaC misconfigurations** (Terraform, CloudFormation, Kubernetes, etc.)
- 📋 **SBOM** (Software Bill of Materials) generation
- 🔐 **License** detection

---

## 🚀 Quick Start

### 1. Install Trivy

#### macOS
```bash
brew install trivy
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

#### Using Homebrew (Linux)
```bash
brew install trivy
```

#### Binary Download
```bash
# Download latest release
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
```

**Verify installation:**
```bash
trivy --version
```

---

### 2. Configure 1Security

Create or update your `config.yaml`:

```yaml
project: myapp
language: python

tools:
  # SCA scanning with Trivy
  sca:
    enabled: true
    runner: trivy
    args: ["fs", ".", "--scanners", "vuln", "--format", "json", "--quiet"]

output:
  format: both
  report_path: reports/
  fail_on: high
```

---

### 3. Run Scan

```bash
python3 1security run
```

---

## 📋 Scan Types

### 1. Filesystem Scan (Dependencies)

Scans your project dependencies for vulnerabilities:

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", ".", "--scanners", "vuln", "--format", "json", "--quiet"]
```

**Supports:**
- Python (requirements.txt, Pipfile, poetry.lock)
- Node.js (package.json, package-lock.json, yarn.lock)
- Java (pom.xml, build.gradle)
- Go (go.mod)
- Ruby (Gemfile.lock)
- PHP (composer.lock)
- .NET (packages.lock.json)
- Rust (Cargo.lock)

---

### 2. Container Image Scan

Scans Docker images:

```yaml
container:
  enabled: true
  runner: trivy
  args: ["image", "nginx:latest", "--format", "json", "--quiet"]
```

**Examples:**
```bash
# Scan public image
args: ["image", "nginx:1.19", "--format", "json", "--quiet"]

# Scan local image
args: ["image", "my-app:latest", "--format", "json", "--quiet"]

# Scan from tarball
args: ["image", "--input", "image.tar", "--format", "json", "--quiet"]
```

---

### 3. Specific Directory Scan

Scan a specific directory:

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", "backend/", "--scanners", "vuln", "--format", "json", "--quiet"]
```

---

### 4. SBOM Generation

Generate Software Bill of Materials:

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", ".", "--format", "cyclonedx", "--output", "sbom.json"]
```

---

## 🎨 Advanced Configuration

### Filter by Severity

Only show CRITICAL and HIGH:

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", ".", "--scanners", "vuln", "--severity", "CRITICAL,HIGH", "--format", "json", "--quiet"]
```

---

### Ignore Unfixed Vulnerabilities

Only report vulnerabilities with available fixes:

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", ".", "--scanners", "vuln", "--ignore-unfixed", "--format", "json", "--quiet"]
```

---

### Scan Specific File

Scan a specific requirements file:

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", "--security-checks", "vuln", "--scanners", "vuln", "requirements.txt", "--format", "json", "--quiet"]
```

---

### Skip Directories

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", ".", "--scanners", "vuln", "--skip-dirs", "node_modules,vendor", "--format", "json", "--quiet"]
```

---

### Offline Mode

Use cached database (no internet required):

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", ".", "--scanners", "vuln", "--offline-scan", "--format", "json", "--quiet"]
```

---

## 🧪 Testing with Example Vulnerabilities

We've included example files with **known vulnerabilities** for testing:

### Python Example

```bash
# Copy SCA config
cp examples/config-sca.yaml config.yaml

# Run scan
python3 1security run

# Expected: Multiple CRITICAL and HIGH vulnerabilities in Django, Flask, etc.
```

**Example findings:**
- Django 2.2.0: CVE-2019-14234 (CRITICAL)
- Flask 0.12.2: CVE-2018-1000656 (HIGH)
- PyYAML 5.1: CVE-2020-1747 (CRITICAL)

---

### Node.js Example

Update config to scan Node.js:

```yaml
sca:
  enabled: true
  runner: trivy
  args: ["fs", "examples/nodejs", "--scanners", "vuln", "--format", "json", "--quiet"]
```

**Example findings:**
- express 3.0.0: Multiple CVEs (HIGH)
- lodash 4.17.4: Prototype pollution (MEDIUM)
- minimist 0.0.8: CVE-2020-7598 (HIGH)

---

## 🔄 Multi-Tool Scanning

Run both Checkov (IaC) and Trivy (SCA) together:

```yaml
project: multi-scan
language: multi

tools:
  # IaC scanning
  iac:
    enabled: true
    runner: checkov
    args: ["-d", "examples/terraform", "--output", "json", "--quiet"]
  
  # SCA scanning
  sca:
    enabled: true
    runner: trivy
    args: ["fs", "examples/python", "--scanners", "vuln", "--format", "json", "--quiet"]

output:
  format: both
  fail_on: high
```

Run scan:
```bash
python3 1security run
```

**Result:** Combined report with both IaC and SCA findings!

---

## 📊 Output Examples

### Console Output

```
🔒 1Security - ASPM Orchestrator

📋 Loading configuration from: config.yaml
✓ trivy completed (25 findings)

📝 Generating reports...

📊 Scan Summary

┏━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━┓
┃ Category ┃ Tool    ┃ Critical ┃ High ┃ Medium ┃ Low ┃ Info ┃ Total ┃
┡━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━┩
│ SCA      │ trivy   │ 3        │ 12   │ 8      │ 2   │ 0    │ 25    │
└──────────┴─────────┴──────────┴──────┴────────┴─────┴──────┴───────┘

Total Findings: 25

📄 Reports Generated:
  • reports/1security-report.json
  • reports/1security-report.html

❌ Scan failed: Issues exceed 'high' threshold
```

---

### JSON Output

```json
{
  "tool": "trivy",
  "category": "sca",
  "severity": "CRITICAL",
  "title": "django: SQL Injection",
  "description": "Django 2.2.0 contains a SQL injection vulnerability...",
  "file": "requirements.txt",
  "resource": "django@2.2.0",
  "cve": "CVE-2019-14234",
  "recommendation": "Upgrade django from 2.2.0 to 2.2.4"
}
```

---

### HTML Report

Beautiful web report showing:
- ✅ Summary dashboard with severity breakdown
- ✅ Detailed table with all vulnerabilities
- ✅ Package names and versions
- ✅ CVE IDs with links
- ✅ Fix recommendations
- ✅ CVSS scores

---

## 🎯 Use Cases

### 1. Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running 1Security SCA scan..."
python3 1security run --config config-sca.yaml

if [ $? -ne 0 ]; then
  echo "❌ Security vulnerabilities found! Fix them before committing."
  exit 1
fi
```

---

### 2. CI/CD Pipeline

See `.github/workflows/1security-scan.yml` for GitHub Actions integration.

**GitLab CI:**
```yaml
security_scan:
  stage: test
  script:
    - pip install -r requirements.txt
    - python3 1security run
  artifacts:
    paths:
      - reports/
```

---

### 3. Regular Audits

```bash
# Daily cron job
0 2 * * * cd /path/to/project && python3 1security run --config config-sca.yaml && mail -s "Security Report" team@company.com < reports/1security-report.html
```

---

## 🔧 Troubleshooting

### Trivy Database Download Slow

```bash
# Pre-download database
trivy image --download-db-only

# Then run scans
python3 1security run
```

---

### False Positives

Create `.trivyignore` file:

```
# Ignore specific CVE
CVE-2019-1234

# Ignore by package
pkg:npm/example@1.0.0
```

---

### Rate Limiting

```yaml
# Use offline mode after initial download
args: ["fs", ".", "--offline-scan", "--format", "json", "--quiet"]
```

---

### Permission Errors

```bash
# Run with elevated permissions if needed
sudo python3 1security run
```

---

## 📈 Performance Tips

1. **Cache Database**: Trivy downloads vulnerability database (~500MB). Cache it in CI/CD:
   ```bash
   trivy image --download-db-only
   ```

2. **Skip Unnecessary Scans**: Use `--skip-dirs` to exclude vendor directories

3. **Parallel Scans**: 1Security runs tools sequentially (Phase 2 will add parallelization)

4. **Offline Mode**: After initial database download, use `--offline-scan`

---

## 🎓 Best Practices

✅ **Run regularly** - Weekly or on every PR  
✅ **Fix by priority** - Critical > High > Medium  
✅ **Update dependencies** - Keep packages current  
✅ **Use version pinning** - Avoid wildcards  
✅ **Monitor trends** - Track vulnerabilities over time  
✅ **Educate team** - Share reports and findings  

---

## 🔗 Resources

- **Trivy Docs**: https://aquasecurity.github.io/trivy/
- **Trivy GitHub**: https://github.com/aquasecurity/trivy
- **CVE Database**: https://cve.mitre.org/
- **NVD Database**: https://nvd.nist.gov/

---

## 🆘 Support

**Issue: Trivy not found**
```bash
# Install Trivy first
brew install trivy  # macOS
# or see INSTALLATION.md for other platforms
```

**Issue: No vulnerabilities found**
- Check if dependencies file exists (requirements.txt, package.json)
- Verify Trivy can access the internet (for database updates)
- Try with example vulnerable dependencies: `cp examples/config-sca.yaml config.yaml`

**Issue: Too many findings**
- Filter by severity: `--severity CRITICAL,HIGH`
- Ignore unfixed: `--ignore-unfixed`
- Use .trivyignore file for known false positives

---

## 🚀 What's Next?

### Phase 2 Enhancements:
- [ ] Parallel scanning (run multiple tools simultaneously)
- [ ] Vulnerability trending (track fixes over time)
- [ ] Custom ignore rules in config
- [ ] SARIF export format
- [ ] Integration with issue trackers (Jira, GitHub Issues)

---

## ✅ Summary

Trivy integration is **production-ready** and provides:
- ✅ Comprehensive vulnerability scanning
- ✅ Multi-language support
- ✅ Fast and accurate results
- ✅ Beautiful reports (JSON + HTML)
- ✅ CI/CD ready
- ✅ Easy configuration

**Start scanning today!** 🎯

```bash
python3 1security run --config examples/config-sca.yaml
```

---

**End of Guide**

