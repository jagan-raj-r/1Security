# ✨ 1Security Features

Complete guide to all 1Security features and capabilities.

---

## 🎯 Overview

1Security v0.2.0 is a comprehensive Application Security Posture Management (ASPM) platform with:

- **4 Security Categories** (IaC, SCA, SAST, Secrets)
- **4 Best-in-class Tools** (Checkov, Trivy, Semgrep, Gitleaks)
- **3 Report Formats** (JSON, HTML, SARIF)
- **Automatic Tool Management**
- **Interactive Filtering**
- **CI/CD Ready**

---

## 🛡️ Security Scanning Categories

### 1. Infrastructure as Code (IaC) - Checkov

**Scans:** Terraform, Kubernetes, CloudFormation, ARM, Helm, Docker

**Finds:**
- ❌ Unencrypted resources (S3, EBS, RDS)
- ❌ Public access enabled
- ❌ Missing security groups
- ❌ Weak IAM policies
- ❌ Missing encryption
- ❌ Compliance violations

**Example Finding:**
```
CKV_AWS_19: Ensure all data stored in S3 is encrypted
Resource: aws_s3_bucket.example
File: terraform/main.tf:15-20
Severity: HIGH
```

**Configuration:**
```yaml
tools:
  iac:
    enabled: true
    runner: checkov
    args: ["-d", ".", "--output", "json", "--quiet"]
```

---

### 2. Software Composition Analysis (SCA) - Trivy

**Scans:** Dependencies, containers, OS packages

**Finds:**
- ❌ Known CVEs in dependencies
- ❌ Outdated libraries
- ❌ Exploitable vulnerabilities
- ❌ Container image issues
- ❌ OS package vulnerabilities

**Example Finding:**
```
CVE-2022-23491: Certifi vulnerable to certificate validation bypass
Package: certifi 2020.12.5
Fixed: 2022.12.7
Severity: CRITICAL
CVSS: 9.8
```

**Configuration:**
```yaml
tools:
  sca:
    enabled: true
    runner: trivy
    args: ["fs", ".", "--scanners", "vuln", "--format", "json", "--quiet"]
```

**Supported Languages:**
- Python (requirements.txt, Pipfile, poetry.lock)
- JavaScript/Node.js (package.json, yarn.lock)
- Java (pom.xml, build.gradle)
- Go (go.mod, go.sum)
- Ruby (Gemfile.lock)
- PHP (composer.lock)
- Rust (Cargo.lock)
- .NET (packages.lock.json)

---

### 3. Static Application Security Testing (SAST) - Semgrep

**Scans:** Source code across 20+ languages

**Finds:**
- ❌ SQL injection
- ❌ Command injection
- ❌ Cross-site scripting (XSS)
- ❌ Path traversal
- ❌ Insecure deserialization
- ❌ Weak cryptography
- ❌ Authentication bypasses
- ❌ Server-side request forgery (SSRF)
- ❌ XML external entity (XXE)
- ❌ And 1000+ more patterns

**Example Finding:**
```
python.lang.security.audit.sql-injection
SQL injection vulnerability using string formatting
File: app.py:45
Severity: HIGH
CWE: CWE-89
OWASP: A03:2021 - Injection
```

**Configuration:**
```yaml
tools:
  sast:
    enabled: true
    runner: semgrep
    args: ["--config", "p/security-audit", "--json", "--quiet", "."]
```

**Semgrep Rulesets:**
- `p/security-audit` - Comprehensive security (recommended)
- `p/owasp-top-ten` - OWASP Top 10 coverage
- `p/cwe-top-25` - CWE Top 25 coverage
- `auto` - Auto-detect language-specific rules

**Supported Languages:**
- Python, JavaScript/TypeScript, Java, Go
- Ruby, PHP, C/C++, C#, Kotlin, Scala
- Swift, Rust, Bash, and more

---

### 4. Secrets Detection - Gitleaks

**Scans:** Code, config files, git history

**Finds:**
- ❌ API keys (AWS, GitHub, Stripe, OpenAI, etc.)
- ❌ Database credentials
- ❌ Private keys (RSA, SSH)
- ❌ OAuth secrets
- ❌ JWT secrets
- ❌ Slack tokens
- ❌ Generic passwords
- ❌ And 100+ credential types

**Example Finding:**
```
AWS Access Key detected
Secret: AKIA****************WXYZ (redacted)
File: config.py:12
Severity: CRITICAL
Rule: aws-access-key
```

**Configuration:**
```yaml
tools:
  secrets:
    enabled: true
    runner: gitleaks
    args: ["detect", "--source", ".", "--report-format", "json", "--no-git"]
```

**Smart Redaction:**
- Secrets are partially hidden in reports
- Full detection without full exposure
- Safe for sharing reports

---

## 📊 Report Formats

### JSON Reports

**Purpose:** Machine-readable, automation-friendly

**Structure:**
```json
{
  "metadata": {
    "tool": "1security",
    "version": "0.2.0",
    "scan_time": "2025-11-21T12:00:00Z",
    "scan_duration": "45.2s"
  },
  "summary": {
    "total": 136,
    "by_severity": {
      "critical": 18,
      "high": 54,
      "medium": 48,
      "low": 14,
      "info": 2
    },
    "by_category": {
      "iac": 12,
      "sca": 102,
      "sast": 14,
      "secrets": 8
    }
  },
  "findings": [
    {
      "id": "uuid",
      "tool": "semgrep",
      "category": "sast",
      "severity": "high",
      "title": "SQL Injection",
      "description": "...",
      "file_path": "app.py",
      "line_number": 45,
      "check_id": "python.lang.security.sql-injection",
      "references": ["CWE-89", "OWASP A03:2021"]
    }
  ]
}
```

**Use Cases:**
- CI/CD pipelines
- Trend analysis
- Metrics dashboards
- API integrations
- Historical tracking

---

### HTML Reports

**Purpose:** Human-friendly, interactive reviews

**Features:**

#### 1. **Summary Dashboard**
- Total findings count
- Severity breakdown (pie chart visual)
- Category distribution
- Scan metadata (time, duration, tools used)

#### 2. **Interactive Filtering** ⭐
Filter findings by:
- **Tool** (Checkov, Trivy, Semgrep, Gitleaks)
- **Severity** (Critical, High, Medium, Low, Info)
- **Category** (IaC, SCA, SAST, Secrets)
- **Search** (keyword in title, file, description)

**Example Filters:**
```
Click "Semgrep" → Only SAST findings
Click "Critical" → Only critical issues
Search "SQL" → SQL-related findings
Combine: "Semgrep" + "High" → High-severity code issues
```

#### 3. **Findings Table**
- Sortable columns
- Color-coded severity badges
- Expandable details
- Copy-paste friendly
- File path links

#### 4. **Finding Details**
Each finding shows:
- Complete description
- File path and line number
- Check/Rule ID
- Severity with visual badge
- Remediation guidance
- Reference links (CWE, CVE, OWASP)
- Code snippet (if available)

**Use Cases:**
- Security team reviews
- Developer education
- Executive reports
- Stakeholder meetings

---

### SARIF Reports ⭐

**Purpose:** Industry-standard format for tool integrations

**SARIF 2.1.0 Features:**
- Full specification compliance
- Rich metadata (CWE, CVE, OWASP mappings)
- Tool driver information
- Rule definitions
- Result locations with regions
- Severity scores

**Integrations:**
- ✅ **GitHub Advanced Security** - Native code scanning
- ✅ **Azure DevOps** - Security dashboard
- ✅ **VS Code** - SARIF Viewer extension
- ✅ **IntelliJ IDEA** - SARIF plugin
- ✅ **SonarQube** - Import SARIF files

**Example Usage:**
```bash
# Generate SARIF
1security run --format sarif

# Upload to GitHub
gh api repos/$OWNER/$REPO/code-scanning/sarifs \
  -F sarif=@reports/1security-report.sarif \
  -F commit_sha=$GITHUB_SHA \
  -F ref=$GITHUB_REF
```

**Use Cases:**
- CI/CD integrations
- GitHub code scanning
- IDE integrations
- Security platforms
- Compliance tools

---

## 🔧 Automatic Tool Management ⭐

**The Problem:**
Traditional security tools require manual installation of each scanner.

**1Security Solution:**
Automatic detection and installation!

### Features

#### 1. **Check Tool Status**
```bash
1security check
```

Shows installation status for all required tools:
```
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Tool     ┃ Category      ┃ Status     ┃ Version ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
│ Checkov  │ IaC Scanner   │ ✅ Installed │ 3.2.1  │
│ Trivy    │ SCA Scanner   │ ❌ Missing   │ -      │
│ Semgrep  │ SAST Scanner  │ ✅ Installed │ 1.144.0│
│ Gitleaks │ Secrets       │ ❌ Missing   │ -      │
└──────────┴───────────────┴────────────┴─────────┘
```

#### 2. **Install Missing Tools**
```bash
# Interactive installation
1security setup

# Automatic installation (CI/CD)
1security setup --yes
```

**What it does:**
1. Reads your configuration
2. Determines required tools
3. Checks what's installed
4. Installs missing tools using:
   - `pip` for Python tools (Checkov, Semgrep)
   - `brew` for binaries (Trivy, Gitleaks)
5. Verifies installations
6. Shows installed versions

#### 3. **Integrated with Run Command**
```bash
# Automatic check before running
1security run

# Or skip check for speed
1security run --skip-tool-check
```

#### 4. **Integrated with Init Command**
```bash
1security init

# Offers:
# "Check tools now? [Y/n]:"
# "Install missing tools? [Y/n]:"
```

### Benefits

✅ **Zero Manual Setup** - One command installs everything
✅ **Smart Detection** - Only installs what you need
✅ **Configuration-Based** - Based on enabled tools
✅ **Platform-Aware** - Handles macOS/Linux differences
✅ **CI/CD Friendly** - `--yes` flag for automation
✅ **Version Verification** - Confirms installations work

**Use Cases:**
- New developer onboarding
- CI/CD environment setup
- Docker container preparation
- Team standardization

---

## 🎨 Interactive Report Filtering ⭐

**The Challenge:**
Comprehensive scans can produce 100+ findings. Finding specific issues is difficult.

**1Security Solution:**
Interactive filtering in HTML reports!

### Filter Types

#### 1. **Filter by Tool**
```
Buttons: All Tools | Checkov | Trivy | Semgrep | Gitleaks
```

**Example:**
- Click "Trivy" → See only SCA vulnerabilities
- Click "Gitleaks" → See only secret detections

#### 2. **Filter by Severity**
```
Buttons: All | Critical | High | Medium | Low | Info
```

**Example:**
- Click "Critical" → Focus on urgent issues
- Click "High" → Review high-priority findings

#### 3. **Filter by Category**
```
Buttons: All | IaC | SCA | SAST | Secrets
```

**Example:**
- Click "SAST" → See code security issues
- Click "IaC" → Review infrastructure problems

#### 4. **Search by Keyword**
```
Search box: Type to filter by title, file, or description
```

**Examples:**
- Search "SQL" → Find SQL-related issues
- Search "config.py" → Issues in specific file
- Search "CWE-89" → Find by CWE ID

### Combine Filters

**Powerful combinations:**
```
"Semgrep" + "Critical" → Critical code issues
"Trivy" + "CVE-2023" → Specific vulnerability
"High" + Search "authentication" → Auth issues
"Secrets" + "Critical" → Exposed credentials
```

### User Experience

- ✅ **Real-time filtering** - Instant results
- ✅ **Visual feedback** - Active filters highlighted
- ✅ **Result count** - Shows X of Y findings
- ✅ **Reset button** - Clear all filters
- ✅ **Keyboard shortcuts** - Power user friendly

### Implementation

Pure JavaScript - no dependencies, works offline!

---

## 🏗️ Unified Output Schema

All tools normalize to a consistent format:

```python
@dataclass
class Finding:
    tool: str              # checkov, trivy, semgrep, gitleaks
    category: Category     # IAC, SCA, SAST, SECRETS
    severity: Severity     # CRITICAL, HIGH, MEDIUM, LOW, INFO
    title: str            # Human-readable title
    description: str      # Detailed description
    file_path: str        # Relative file path
    line_number: int      # Line number (if applicable)
    check_id: str         # Tool-specific rule ID
    references: List[str] # CWE, CVE, OWASP links
    remediation: str      # Fix guidance
    code_snippet: str     # Code context
```

**Benefits:**
- Consistent reporting across tools
- Easy to parse and process
- Enables cross-tool correlation
- Simplifies report generation

---

## 🚀 CI/CD Integration

### Exit Codes

```python
0 = No issues or below fail threshold
1 = Findings at or above fail threshold
2 = Configuration error
3 = Tool execution error
```

**Example:**
```yaml
output:
  fail_on: high

# Exit code 1 if HIGH or CRITICAL found
# Exit code 0 if only MEDIUM, LOW, INFO
```

### GitHub Actions Integration

```yaml
- name: Security Scan
  run: 1security run --format sarif

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: reports/1security-report.sarif
```

### GitLab CI Integration

```yaml
security_scan:
  script:
    - 1security run --format sarif
  artifacts:
    reports:
      sast: reports/1security-report.sarif
```

---

## 🎯 Advanced Features

### 1. **Multi-Tool Orchestration**

Run multiple scanners in one command:
```bash
1security run --config config-phase2.yaml
```

Coordinates:
- Tool execution order
- Output collection
- Result normalization
- Report generation

### 2. **Configuration Flexibility**

```yaml
# Enable/disable any tool
tools:
  iac:
    enabled: true   # Turn on/off individually
  sca:
    enabled: false  # Disabled for this scan
```

### 3. **Custom Arguments**

```yaml
# Pass any arguments to underlying tools
tools:
  sast:
    runner: semgrep
    args: ["--config", "p/security-audit", "--timeout", "60", "--json", "."]
```

### 4. **Severity Mapping**

Automatic severity normalization:
```
Checkov "HIGH" → Finding.Severity.HIGH
Trivy "CRITICAL" → Finding.Severity.CRITICAL
Semgrep "WARNING" → Finding.Severity.MEDIUM
Gitleaks → Finding.Severity.CRITICAL (all secrets)
```

### 5. **Rich Terminal Output**

- Progress indicators
- Colored severity badges
- Summary tables
- Helpful error messages

---

## 📈 Feature Roadmap

### v0.2.0 (Current) ✅
- ✅ 4 security categories
- ✅ SARIF export
- ✅ Automatic tool management
- ✅ Interactive filtering

### v0.3.0 (Planned)
- [ ] Web dashboard (FastAPI + React)
- [ ] Historical trending
- [ ] Finding deduplication
- [ ] Custom policy engine
- [ ] Multi-repo scanning

### v1.0.0 (Future)
- [ ] Slack/Jira integrations
- [ ] Risk scoring
- [ ] Compliance reporting
- [ ] REST API
- [ ] User authentication

---

## 💡 Feature Highlights

### What Makes 1Security Special

1. **Unified Platform** - One tool, multiple scanners
2. **Zero Setup** - Automatic tool installation
3. **Developer-Friendly** - Beautiful reports, easy CLI
4. **Industry Standards** - SARIF, OWASP, CWE mappings
5. **Flexible** - Use one tool or all tools
6. **CI/CD Ready** - Easy integration
7. **Open Source** - MIT licensed, community-driven

---

## 📞 Learn More

- **Getting Started**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **Tool Details**: [TOOLS.md](TOOLS.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

**1Security v0.2.0** | MIT License | R Jagan Raj

