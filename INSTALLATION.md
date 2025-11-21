# 📦 Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager

---

## 1. Install 1Security

```bash
cd "/path/to/1Security"

# Install Python dependencies
pip install -r requirements.txt

# Install 1Security CLI
pip install -e .
```

---

## 2. Install Security Scanners

### Checkov (IaC Scanner) ✅ Python Package

```bash
pip install checkov
```

**Verify installation:**
```bash
checkov --version
```

---

### Trivy (SCA Scanner) 🔧 Binary Installation

#### macOS (Homebrew)
```bash
brew install trivy
```

#### Linux (Ubuntu/Debian)
```bash
# Add repository
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list

# Install Trivy
sudo apt-get update
sudo apt-get install trivy
```

#### Linux (RPM-based)
```bash
# Add repository
sudo vim /etc/yum.repos.d/trivy.repo
# [trivy]
# name=Trivy repository
# baseurl=https://aquasecurity.github.io/trivy-repo/rpm/releases/$releasever/$basearch/
# gpgcheck=0
# enabled=1

# Install Trivy
sudo yum -y install trivy
```

#### Using Binary Release (All Platforms)
```bash
# Download latest release
VERSION=$(curl --silent "https://api.github.com/repos/aquasecurity/trivy/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
wget https://github.com/aquasecurity/trivy/releases/download/v${VERSION}/trivy_${VERSION}_Linux-64bit.tar.gz

# Extract
tar zxvf trivy_${VERSION}_Linux-64bit.tar.gz

# Move to PATH
sudo mv trivy /usr/local/bin/

# Make executable
sudo chmod +x /usr/local/bin/trivy
```

#### Docker (if you prefer)
```bash
# Run Trivy in Docker
docker run aquasec/trivy:latest --version
```

**Verify installation:**
```bash
trivy --version
```

---

## 3. Verify Installation

```bash
# Check 1Security
python3 1security --version

# Check Checkov
checkov --version

# Check Trivy
trivy --version
```

**Expected output:**
```
1security, version 0.1.0
checkov 3.x.x
Version: 0.x.x
```

---

## 4. Initialize Configuration

```bash
python3 1security init
```

This creates a `config.yaml` file in your current directory.

---

## 5. Run Your First Scan

```bash
python3 1security run
```

---

## Troubleshooting

### Command not found: 1security

**Solution:**
```bash
# Use Python directly
python3 1security run

# Or reinstall
pip install -e .
```

### Trivy: command not found

**macOS:**
```bash
brew install trivy
```

**Linux:**
```bash
# Use the binary installation method above
# Or use Docker: docker run aquasec/trivy:latest
```

### Checkov: command not found

```bash
pip install checkov

# Or with specific version
pip install checkov==3.0.0
```

### Permission denied errors

```bash
# Make script executable
chmod +x 1security

# Or use with Python
python3 1security run
```

---

## Optional: System-wide Installation

To install 1Security system-wide:

```bash
# Instead of pip install -e .
pip install .

# Or from GitHub (future)
pip install git+https://github.com/jaganraj/1security.git
```

---

## Docker Installation (Alternative)

Coming in Phase 2 - Run everything in Docker containers without installing tools locally.

---

## IDE Integration

### VS Code

Add to `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "1Security Scan",
      "type": "shell",
      "command": "python3 1security run",
      "problemMatcher": []
    }
  ]
}
```

---

## CI/CD Integration

See `.github/workflows/1security-scan.yml` for GitHub Actions example.

---

## Next Steps

1. Edit `config.yaml` to configure your scanners
2. Run scans: `python3 1security run`
3. View reports: `open reports/1security-report.html`
4. Integrate into CI/CD

---

## Get Help

- Documentation: See `README.md` and `QUICKSTART.md`
- Issues: Open an issue on GitHub
- Examples: Check `examples/` directory

