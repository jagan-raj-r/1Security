# 1Security — Open Source ASPM Orchestrator

## 🚀 Overview
**1Security** is a lightweight, open-source **Application Security Posture Management (ASPM)** tool that unifies the best security scanners from each category — **SCA**, **SAST**, **DAST**, **IaC**, **Secrets**, and **Container** — into a single, developer-friendly platform.

It lets you run, normalize, and visualize all security scans from one command or CI/CD step.

---

## 🎯 Vision
Today, dev and security teams run multiple tools independently, each with different formats, reports, and severities.  
**1Security** provides a single control plane to orchestrate them all, correlate results, and apply policies consistently — all open-source and pluggable.

---

## 🧩 Core Categories and Example Tools

| Category | Purpose | Example Tools |
|-----------|----------|----------------|
| **SCA (Software Composition Analysis)** | Detect vulnerable dependencies | Syft, Grype, Dependency-Track |
| **SAST (Static Application Security Testing)** | Find insecure code patterns | Semgrep, CodeQL |
| **IaC Scanning** | Detect misconfigurations in infrastructure code | Checkov, Tfsec |
| **DAST (Dynamic App Security Testing)** | Simulate runtime attacks | OWASP ZAP, Nuclei |
| **Secrets Detection** | Detect API keys and credentials in code | Gitleaks, TruffleHog |
| **Container Security** | Scan Docker images | Trivy, Dockle |

---

## ⚙️ Lightweight Architecture

```mermaid
flowchart LR
    Dev[CLI / GitHub Action] --> |1security run| Orchestrator

    subgraph Core
      Orchestrator[Orchestrator]
      Config[Config Loader (YAML)]
      Bus[Result Bus (JSON/SARIF)]
      Normalizer[Normalizer (per-tool adapters)]
      Correlate[Dedup + Correlate (CWE/CVE/OWASP)]
      Policy[Policy Gate (fail/waive rules)]
      Store[(Local Store: FS/SQLite)]
      Reporters[Reporters (HTML/JSON/SARIF)]
    end

    Orchestrator --> Config
    Orchestrator --> Runners
    Runners -->|STDOUT/Files| Normalizer --> Bus --> Correlate --> Policy --> Reporters --> Dev
    Correlate --> Store

    subgraph Runners [Tool Runners]
      SCA[Syft/Grype]
      SAST[Semgrep/CodeQL]
      IaC[Checkov/Tfsec]
      Secrets[Gitleaks]
      DAST[ZAP/Nuclei]
      Container[Trivy/Dockle]
    end

    Orchestrator --> SCA
    Orchestrator --> SAST
    Orchestrator --> IaC
    Orchestrator --> Secrets
    Orchestrator --> DAST
    Orchestrator --> Container

    Reporters -->|PR comments/status| SCM[GitHub/GitLab]
    Reporters -->|Alerts| Chat[Slack]
    Reporters -->|Issues| Tracker[Jira]
```

---

## 🧱 Folder Structure

```
1security/
├── core/
│   ├── orchestrator.py
│   ├── parsers/
│   ├── reporters/
│   ├── correlator.py
│   ├── policy.py
│   └── store.py
├── tools.yaml
├── cli.py
├── web/
└── examples/
    └── config.example.yaml
```

---

## ⚡ MVP Roadmap

### Phase 1 — CLI + Two Tool Integrations
- [x] Command-line runner (`1security run`)
- [x] YAML-based config for enabling tools  
- [x] Integrate **Semgrep** (SAST)  
- [x] Integrate **Trivy** (SCA/Container)
- [x] Normalize outputs into unified JSON  
- [x] Basic HTML report generation  

### Phase 2 — Policy + CI/CD Integration
- [ ] Define severity thresholds (fail on `critical`)  
- [ ] Add SARIF export for GitHub  
- [ ] GitHub Action + GitLab CI support  
- [ ] Slack/Jira notifications  

### Phase 3 — Dashboard + Plugins
- [ ] Web dashboard (FastAPI + React)
- [ ] Plugin system for adding tools easily  
- [ ] Risk scoring + trending reports  
- [ ] Central SQLite or MongoDB store  

---

## 🧩 Example `config.yaml`

```yaml
project: myapp
language: python

tools:
  sast:
    enabled: true
    runner: semgrep
    args: ["--config", "p/owasp-top-ten"]
  sca:
    enabled: true
    runner: trivy
    args: ["fs", "."]
  iac:
    enabled: false
  dast:
    enabled: false
  secrets:
    enabled: true
    runner: gitleaks
    args: ["detect", "--source", "."]

output:
  format: json
  report_path: reports/
  fail_on: critical
```

---

## 🧠 How It Works (Step-by-Step)

1. **`1security run`** — CLI reads `config.yaml`.
2. **Orchestrator** launches enabled scanners (in Docker or local).
3. Each tool’s **output is parsed** into a unified JSON schema.
4. **Normalizer** converts results → SARIF-compatible structure.
5. **Correlator** deduplicates, enriches with CWE/CVE/OWASP data.
6. **Policy Gate** enforces org-defined thresholds.
7. **Reporter** generates:
   - JSON output for automation
   - HTML report for humans
   - Optional CI/CD status + alerts

---

## 🧩 Output Schema (Example)

```json
{
  "tool": "semgrep",
  "category": "sast",
  "file": "src/app.py",
  "line": 42,
  "rule": "python.lang.security.insecure-hash",
  "severity": "HIGH",
  "message": "Use of MD5 is insecure",
  "cwe": "CWE-327",
  "recommendation": "Use SHA-256 or better"
}
```

---

## 🧠 Design Principles

- **Pluggable**: Each tool adapter is self-contained.  
- **Lightweight**: No server required for basic usage.  
- **Extensible**: Add new tools easily.  
- **Unified**: Outputs normalized to one format.  
- **Developer-first**: Runs locally or in CI/CD.  

---

## 🔌 Integrations (Future)
- SCM: GitHub, GitLab
- Notifications: Slack, Teams
- Issue Tracking: Jira, Linear
- Storage: SQLite, MongoDB
- Cloud: S3, GCS

---

## 🧰 Tech Stack
- **Language:** Python  
- **Web Dashboard:** FastAPI + React  
- **Storage:** SQLite  
- **Reporting:** Jinja2  
- **Packaging:** Docker + PyInstaller  

---

## 🔒 Security Goals
- Reduce alert fatigue through deduplication and correlation.  
- Provide visibility across SDLC.  
- Make ASPM accessible to all teams.

---

## 📅 Next Steps
1. Scaffold CLI  
2. Build Semgrep adapter  
3. Build Trivy adapter  
4. Design output schema  
5. Generate JSON + HTML reports  
6. Add policy engine  
7. Integrate into CI/CD  

---

## 💡 Example Command Flow

```bash
1security init
1security run --config config.yaml
1security report --format html
1security policy check
```

---

## 🧭 Future Enhancements
- AI-based prioritization  
- Plugin registry  
- SBOM correlation  
- REST API  
- Multi-repo visibility  

---

## 🧑‍💻 Author & License
**Author:** R Jagan Raj  
**License:** MIT  
**Repository:** [github.com/jaganraj/1security](https://github.com/jaganraj/1security)
