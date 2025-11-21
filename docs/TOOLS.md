# 🛠️ Security Tools Guide

Deep dive into each security tool integrated with 1Security.

---

## Overview

1Security integrates 4 best-in-class open-source security tools:

| Tool | Category | Purpose | Language | Install |
|------|----------|---------|----------|---------|
| **Checkov** | IaC | Infrastructure scanning | Python | `pip install checkov` |
| **Trivy** | SCA | Dependency vulnerabilities | Go | `brew install trivy` |
| **Semgrep** | SAST | Code security | OCaml/Python | `pip install semgrep` |
| **Gitleaks** | Secrets | Credential detection | Go | `brew install gitleaks` |

---

## 🏗️ Checkov - Infrastructure as Code Scanner

**by Bridgecrew (Palo Alto Networks)**

### What It Does

Scans infrastructure-as-code files for security misconfigurations and compliance violations.

### Supported Frameworks

- **Terraform** (.tf files)
- **CloudFormation** (.yaml, .json templates)
- **Kubernetes** (manifests, Helm charts)
- **Azure Resource Manager** (ARM templates)
- **Docker** (Dockerfiles)
- **Serverless Framework**
- **Ansible**
- **Bicep**

### Installation

```bash
# Python package
pip install checkov

# Verify
checkov --version
```

### Configuration

```yaml
tools:
  iac:
    enabled: true
    runner: checkov
    args: ["-d", ".", "--output", "json", "--quiet"]
```

### Common Arguments

```yaml
# Specific directory
args: ["-d", "./terraform", "--output", "json"]

# Specific framework
args: ["-d", ".", "--framework", "terraform", "--output", "json"]

# Skip specific checks
args: ["-d", ".", "--skip-check", "CKV_AWS_19,CKV_AWS_20", "--output", "json"]

# Only specific checks
args: ["-d", ".", "--check", "CKV_AWS_18,CKV_AWS_19", "--output", "json"]

# Quiet mode (no progress)
args: ["-d", ".", "--output", "json", "--quiet"]
```

### What It Finds

**AWS Issues:**
- Unencrypted S3 buckets
- Public S3 access
- Unencrypted EBS volumes
- Security groups allowing 0.0.0.0/0
- IAM policies with wildcards
- Unencrypted RDS instances

**Kubernetes Issues:**
- Privileged containers
- Missing resource limits
- hostNetwork enabled
- Default service accounts
- Missing pod security policies

**Docker Issues:**
- Running as root
- COPY instead of ADD
- Missing HEALTHCHECK
- Using latest tag

### Example Finding

```
Check: CKV_AWS_19: "Ensure all data stored in the S3 bucket is encrypted"
Resource: aws_s3_bucket.example
File: /terraform/main.tf:15-20
Severity: HIGH
Guide: https://docs.bridgecrew.io/docs/s3_14-data-encrypted-at-rest
```

### Checkov-Specific Files

**Skip checks:**
`.checkov.yaml`
```yaml
skip-check:
  - CKV_AWS_19
  - CKV_AWS_20
```

**External checks:**
```bash
checkov -d . --external-checks-dir ./custom-checks
```

### Resources

- **Website**: https://www.checkov.io/
- **Docs**: https://www.checkov.io/documentation.html
- **Rules**: https://www.checkov.io/5.Policy%20Index/all.html

---

## 📦 Trivy - Vulnerability Scanner

**by Aqua Security**

### What It Does

Comprehensive vulnerability scanner for dependencies, containers, and filesystems.

### Scan Types

1. **Filesystem** - Dependencies in your project
2. **Container Image** - Docker/OCI images
3. **Repository** - Git repositories
4. **SBOM** - Software Bill of Materials
5. **Config** - IaC misconfigurations

### Installation

#### macOS
```bash
brew install trivy
```

#### Linux (Homebrew)
```bash
brew install trivy
```

#### Linux (APT)
```bash
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

#### Binary Download
```bash
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
```

#### Verify
```bash
trivy --version
```

### Configuration

```yaml
tools:
  sca:
    enabled: true
    runner: trivy
    args: ["fs", ".", "--scanners", "vuln", "--format", "json", "--quiet"]
```

### Common Arguments

```yaml
# Scan filesystem
args: ["fs", ".", "--scanners", "vuln", "--format", "json"]

# Filter by severity
args: ["fs", ".", "--severity", "CRITICAL,HIGH", "--format", "json"]

# Ignore unfixed vulnerabilities
args: ["fs", ".", "--ignore-unfixed", "--format", "json"]

# Skip directories
args: ["fs", ".", "--skip-dirs", "node_modules,vendor", "--format", "json"]

# Scan container image
args: ["image", "nginx:latest", "--format", "json"]

# Multiple scanners
args: ["fs", ".", "--scanners", "vuln,config,secret", "--format", "json"]
```

### Supported Languages & Package Managers

**Python:**
- requirements.txt
- Pipfile, Pipfile.lock
- poetry.lock
- setup.py

**JavaScript/Node.js:**
- package.json, package-lock.json
- yarn.lock
- pnpm-lock.yaml

**Java:**
- pom.xml (Maven)
- build.gradle, gradle.lockfile (Gradle)

**Go:**
- go.mod, go.sum

**Ruby:**
- Gemfile.lock

**PHP:**
- composer.lock

**Rust:**
- Cargo.lock

**.NET:**
- packages.lock.json
- *.deps.json

### What It Finds

**Vulnerabilities:**
- Known CVEs in dependencies
- OS package vulnerabilities
- Exploitable vulnerabilities
- Outdated libraries

**Example Finding:**
```
CVE-2022-23491: Certifi vulnerable to certificate validation bypass
Package: certifi
Installed Version: 2020.12.5
Fixed Version: 2022.12.7
Severity: CRITICAL
CVSS Score: 9.8
Published: 2022-12-07
References: 
  - https://nvd.nist.gov/vuln/detail/CVE-2022-23491
  - https://github.com/advisories/GHSA-43fp-rhv2-5gv8
```

### Trivy-Specific Files

**Ignore vulnerabilities:**
`.trivyignore`
```
# Ignore specific CVE
CVE-2022-1234

# Ignore by package
pkg:pypi/requests@2.25.1

# Ignore with expiry
CVE-2022-5678 exp:2025-12-31
```

### Performance Tuning

```yaml
# Skip large directories
args: ["fs", ".", "--skip-dirs", "node_modules,.git,vendor"]

# Only specific scanners
args: ["fs", ".", "--scanners", "vuln"]

# Timeout
args: ["fs", ".", "--timeout", "5m"]
```

### Resources

- **Website**: https://aquasecurity.github.io/trivy/
- **Docs**: https://aquasecurity.github.io/trivy/latest/
- **GitHub**: https://github.com/aquasecurity/trivy

---

## 🔍 Semgrep - Static Application Security Testing

**by Semgrep Inc. (formerly r2c)**

### What It Does

Fast, customizable static analysis for finding security vulnerabilities and code quality issues.

### Supported Languages

- Python, JavaScript, TypeScript, Java, Go
- Ruby, PHP, C, C++, C#, Kotlin, Scala
- Swift, Rust, Bash, Lua, OCaml, JSON, YAML

### Installation

```bash
# Python package
pip install semgrep

# Verify
semgrep --version
```

### Configuration

```yaml
tools:
  sast:
    enabled: true
    runner: semgrep
    args: ["--config", "p/security-audit", "--json", "--quiet", "."]
```

### Ruleset Options

```yaml
# Comprehensive security audit (recommended)
args: ["--config", "p/security-audit", "--json", "."]

# OWASP Top 10
args: ["--config", "p/owasp-top-ten", "--json", "."]

# CWE Top 25
args: ["--config", "p/cwe-top-25", "--json", "."]

# Auto-detect language rules
args: ["--config", "auto", "--json", "."]

# Multiple rulesets
args: ["--config", "p/security-audit", "--config", "p/owasp-top-ten", "--json", "."]

# Custom rules
args: ["--config", "./custom-rules.yaml", "--json", "."]
```

### Common Arguments

```yaml
# Exclude directories
args: ["--config", "p/security-audit", "--exclude", "tests,docs", "--json", "."]

# Timeout per rule
args: ["--config", "p/security-audit", "--timeout", "30", "--json", "."]

# Severity filter
args: ["--config", "p/security-audit", "--severity", "ERROR", "--json", "."]

# Verbose
args: ["--config", "p/security-audit", "--verbose", "--json", "."]
```

### What It Finds

**Injection Vulnerabilities:**
- SQL injection
- Command injection
- LDAP injection
- XPath injection

**Authentication & Authorization:**
- Broken authentication
- Weak password requirements
- Insecure session management
- Missing authorization checks

**Cryptography:**
- Weak encryption algorithms (MD5, SHA1)
- Hardcoded keys (also found by Gitleaks)
- Insecure random number generation
- Missing encryption

**Code Quality:**
- Use of dangerous functions (eval, exec)
- Insecure deserialization
- Path traversal
- Server-side request forgery (SSRF)
- XML external entity (XXE)

### Example Finding

```
python.flask.security.audit.direct-use-of-jinja2
Direct use of Jinja2 templates can lead to XSS
File: app.py:45
Severity: WARNING
Confidence: HIGH
CWE: CWE-79
OWASP: A03:2021 - Injection
Fix: Use Flask's render_template() instead
```

### Semgrep-Specific Files

**Exclude paths:**
`.semgrepignore`
```
tests/
node_modules/
vendor/
*.test.js
*.spec.py
```

**Custom rules:**
```yaml
rules:
  - id: custom-sql-injection
    pattern: execute($SQL)
    message: Potential SQL injection
    languages: [python]
    severity: ERROR
```

### Performance

Semgrep is **fast**:
- 20,000+ lines of code in seconds
- Incremental scanning support
- Parallel execution

### Resources

- **Website**: https://semgrep.dev/
- **Playground**: https://semgrep.dev/playground
- **Rules**: https://semgrep.dev/explore
- **Docs**: https://semgrep.dev/docs/

---

## 🔐 Gitleaks - Secrets Detection

**by Zachary Rice**

### What It Does

Scans code and git history for hardcoded secrets, API keys, passwords, and credentials.

### Detects 100+ Secret Types

**Cloud Providers:**
- AWS (Access Key, Secret Key, Session Token)
- Google Cloud (API keys, Service Account)
- Azure (Storage keys, Service Principal)
- Digital Ocean tokens

**Services:**
- GitHub tokens
- GitLab tokens
- Slack tokens
- Stripe API keys
- OpenAI API keys
- Twilio credentials
- SendGrid API keys

**Databases:**
- PostgreSQL URLs
- MySQL URLs
- MongoDB URLs
- Redis passwords

**Generic:**
- Private keys (RSA, SSH, PGP)
- JWT secrets
- OAuth credentials
- Generic passwords
- Generic API keys

### Installation

#### macOS
```bash
brew install gitleaks
```

#### Linux (Homebrew)
```bash
brew install gitleaks
```

#### Linux (Binary)
```bash
# Download latest
VERSION=$(curl --silent "https://api.github.com/repos/gitleaks/gitleaks/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
wget https://github.com/gitleaks/gitleaks/releases/download/v${VERSION}/gitleaks_${VERSION}_linux_x64.tar.gz

# Extract
tar zxvf gitleaks_${VERSION}_linux_x64.tar.gz

# Move to PATH
sudo mv gitleaks /usr/local/bin/
sudo chmod +x /usr/local/bin/gitleaks
```

#### Verify
```bash
gitleaks version
```

### Configuration

```yaml
tools:
  secrets:
    enabled: true
    runner: gitleaks
    args: ["detect", "--source", ".", "--report-format", "json", "--no-git"]
```

### Common Arguments

```yaml
# Standard scan (no git)
args: ["detect", "--source", ".", "--report-format", "json", "--no-git"]

# Scan git history
args: ["detect", "--source", ".", "--report-format", "json"]

# Verbose output
args: ["detect", "--source", ".", "--report-format", "json", "--verbose"]

# Custom config
args: ["detect", "--source", ".", "--config", ".gitleaks.toml", "--report-format", "json"]

# Baseline (ignore known secrets)
args: ["detect", "--source", ".", "--baseline-path", "baseline.json", "--report-format", "json"]
```

### Example Finding

```
Rule: aws-access-key-id
Secret: AKIA****************WXYZ (redacted)
File: config.py:12
Line: AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
Commit: a1b2c3d (if scanning git history)
Severity: CRITICAL
```

### Gitleaks-Specific Files

**Ignore patterns:**
`.gitleaksignore`
```
# Ignore specific file
config/test-secrets.py

# Ignore pattern
**/*.example
**/test_*.py

# Ignore by fingerprint
abcdef1234567890
```

**Custom configuration:**
`.gitleaks.toml`
```toml
[extend]
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''api[_-]?key[_-]?[=:]\s*['"]?([a-zA-Z0-9]{32})['"]?'''
```

### Smart Redaction

Gitleaks findings in 1Security reports are **redacted**:
```
Original: AKIAIOSFODNN7EXAMPLE
Reported: AKIA****************WXYZ
```

**Why:** Safe to share reports without exposing actual secrets.

### Best Practices

1. **Pre-commit Hook**: Scan before committing
2. **CI/CD**: Block commits with secrets
3. **Regular Scans**: Find historical leaks
4. **Rotate Immediately**: If secrets found, rotate them
5. **Use .gitleaksignore**: For test files with fake secrets

### Resources

- **GitHub**: https://github.com/gitleaks/gitleaks
- **Docs**: https://github.com/gitleaks/gitleaks/wiki
- **Rules**: https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml

---

## 🔄 Tool Comparison

| Feature | Checkov | Trivy | Semgrep | Gitleaks |
|---------|---------|-------|---------|----------|
| **Speed** | Fast | Very Fast | Fast | Very Fast |
| **Accuracy** | High | High | Very High | High |
| **False Positives** | Low | Low | Medium | Low |
| **Language Support** | IaC only | Multi | 20+ | All |
| **Customization** | High | Medium | Very High | High |
| **Learning Curve** | Low | Low | Medium | Low |

---

## 🎯 When to Use Each Tool

### Use Checkov When:
- Scanning infrastructure-as-code
- Working with Terraform/K8s/CloudFormation
- Need compliance checks
- Want infrastructure security

### Use Trivy When:
- Checking dependencies for CVEs
- Scanning container images
- Need OS package vulnerabilities
- Want comprehensive SCA

### Use Semgrep When:
- Looking for code-level security bugs
- Need custom security patterns
- Want OWASP/CWE coverage
- Scanning source code

### Use Gitleaks When:
- Finding hardcoded credentials
- Checking for exposed API keys
- Scanning git history
- Pre-commit secret detection

---

## 🔧 Tool-Specific Tips

### Checkov Tips

```bash
# Update checks database
checkov --download-external-modules

# List available checks
checkov --list

# Soft-fail mode (exit 0 even with findings)
checkov -d . --soft-fail
```

### Trivy Tips

```bash
# Update vulnerability database
trivy image --download-db-only

# Clear cache
trivy clean --all

# Generate SBOM
trivy fs . --format cyclonedx --output sbom.json
```

### Semgrep Tips

```bash
# List available rulesets
semgrep --show-supported-languages

# Test specific rule
semgrep --config rule.yaml file.py

# Generate baseline
semgrep --config auto --baseline-commit main
```

### Gitleaks Tips

```bash
# Generate baseline (ignore current secrets)
gitleaks detect --source . --report-path baseline.json

# Scan specific commit range
gitleaks detect --log-opts="HEAD~10..HEAD"

# Protect mode (for pre-commit)
gitleaks protect --staged
```

---

## 📞 Get Help

- **Getting Started**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **Features**: [FEATURES.md](FEATURES.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

**1Security v0.2.0** | MIT License | R Jagan Raj

