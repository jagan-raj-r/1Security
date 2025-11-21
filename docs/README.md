# 📚 1Security Documentation

**v0.2.0** - Open Source ASPM Orchestrator

Welcome to the 1Security documentation! Everything you need to install, use, and master 1Security is here.

---

## 🚀 Start Here

New to 1Security? Start with these guides:

| Guide | Description | Time |
|-------|-------------|------|
| [**GETTING_STARTED.md**](GETTING_STARTED.md) | Complete installation and setup guide | 10 min |
| [**USER_GUIDE.md**](USER_GUIDE.md) | All commands, configurations, and workflows | 20 min |
| [**FEATURES.md**](FEATURES.md) | Explore all capabilities and features | 15 min |

---

## 📖 Complete Documentation

### Core Documentation

| Document | What's Inside | Best For |
|----------|---------------|----------|
| [**GETTING_STARTED.md**](GETTING_STARTED.md) | Installation, first scan, troubleshooting | New users, onboarding |
| [**USER_GUIDE.md**](USER_GUIDE.md) | Commands, configs, workflows, best practices | Daily usage reference |
| [**FEATURES.md**](FEATURES.md) | All features explained in detail | Understanding capabilities |
| [**TOOLS.md**](TOOLS.md) | Deep dive into each security tool | Tool-specific questions |
| [**DEVELOPMENT.md**](DEVELOPMENT.md) | Architecture, contributing, adding tools | Contributors, developers |
| [**CHANGELOG.md**](CHANGELOG.md) | Version history and changes | Tracking updates |

### Technical Reports

| Document | What's Inside | Best For |
|----------|---------------|----------|
| [**CODE_REVIEW.md**](CODE_REVIEW.md) | Complete code review (20 issues identified) | Understanding code quality |
| [**OPTIMIZATIONS.md**](OPTIMIZATIONS.md) | First round of optimizations (8 fixes) | Tracking improvements |
| [**FIXES_SUMMARY.md**](FIXES_SUMMARY.md) | All issues fixed summary (15/20 resolved) | Complete fix report |
| [**CLEANUP_ANALYSIS.md**](CLEANUP_ANALYSIS.md) | Project cleanup and .gitignore analysis | Repository maintenance |

---

## 🎯 Quick Navigation

### I want to...

**Install and set up 1Security**
→ [GETTING_STARTED.md](GETTING_STARTED.md)

**Learn all commands**
→ [USER_GUIDE.md](USER_GUIDE.md) → Quick Command Reference

**Understand what 1Security can do**
→ [FEATURES.md](FEATURES.md)

**Configure a specific security tool**
→ [TOOLS.md](TOOLS.md) → Find your tool

**Add a new security scanner**
→ [DEVELOPMENT.md](DEVELOPMENT.md) → Adding a New Security Tool

**See what's new**
→ [CHANGELOG.md](CHANGELOG.md)

**Use interactive filtering in reports**
→ [FEATURES.md](FEATURES.md) → Interactive Report Filtering

**Set up automatic tool installation**
→ [GETTING_STARTED.md](GETTING_STARTED.md) → Automatic Tool Management

**Integrate with CI/CD**
→ [USER_GUIDE.md](USER_GUIDE.md) → CI/CD Integration Examples

**Understand SARIF reports**
→ [FEATURES.md](FEATURES.md) → SARIF Reports

---

## 📊 Documentation Structure

```
docs/
├── README.md (you are here)         # Documentation index
├── GETTING_STARTED.md              # Installation & first scan (10 min read)
├── USER_GUIDE.md                   # Complete command reference (20 min read)
├── FEATURES.md                     # All features explained (15 min read)
├── TOOLS.md                        # Tool-specific guides (30 min read)
├── DEVELOPMENT.md                  # For contributors (20 min read)
└── CHANGELOG.md                    # Version history
```

**Total**: 6 focused documents (~95 min to read everything)

---

## 🎓 Learning Paths

### For New Users (30 minutes)

```
1. GETTING_STARTED.md (10 min)
   ├─ Prerequisites
   ├─ Quick Install
   ├─ First Scan
   └─ Understanding Reports

2. USER_GUIDE.md (15 min)
   ├─ Quick Command Reference
   ├─ Configuration Basics
   └─ Common Workflows

3. FEATURES.md (5 min)
   └─ Overview section
```

### For Power Users (60 minutes)

```
1. USER_GUIDE.md (complete)
   ├─ All commands and options
   ├─ Advanced configurations
   ├─ Tool-specific arguments
   └─ CI/CD integrations

2. FEATURES.md (complete)
   ├─ All security categories
   ├─ Report formats
   ├─ Advanced features
   └─ Feature details

3. TOOLS.md (selections)
   └─ Deep dive into tools you use
```

### For Contributors (45 minutes)

```
1. DEVELOPMENT.md (complete)
   ├─ Project structure
   ├─ Architecture overview
   ├─ Adding new tools
   └─ Testing & debugging

2. CHANGELOG.md
   └─ Understand evolution

3. Codebase exploration
   └─ Review actual code
```

---

## 🔍 Find by Topic

### Installation & Setup
- [Quick Install](GETTING_STARTED.md#quick-install-recommended)
- [Manual Setup](GETTING_STARTED.md#manual-setup-if-needed)
- [Tool Installation](GETTING_STARTED.md#automatic-tool-management)
- [Troubleshooting](GETTING_STARTED.md#troubleshooting)

### Usage & Commands
- [Command Reference](USER_GUIDE.md#quick-command-reference)
- [Configuration Guide](USER_GUIDE.md#configuration-guide)
- [Common Workflows](USER_GUIDE.md#common-workflows)
- [Best Practices](USER_GUIDE.md#best-practices)

### Security Tools
- [Checkov (IaC)](TOOLS.md#checkov---infrastructure-as-code-scanner)
- [Trivy (SCA)](TOOLS.md#trivy---vulnerability-scanner)
- [Semgrep (SAST)](TOOLS.md#semgrep---static-application-security-testing)
- [Gitleaks (Secrets)](TOOLS.md#gitleaks---secrets-detection)

### Features
- [Security Categories](FEATURES.md#security-scanning-categories)
- [Report Formats](FEATURES.md#report-formats)
- [Interactive Filtering](FEATURES.md#interactive-report-filtering)
- [Automatic Tool Management](FEATURES.md#automatic-tool-management)
- [SARIF Export](FEATURES.md#sarif-reports)

### Development
- [Architecture](DEVELOPMENT.md#architecture-overview)
- [Adding Tools](DEVELOPMENT.md#adding-a-new-security-tool)
- [Testing](DEVELOPMENT.md#testing)
- [Contributing](DEVELOPMENT.md#contributing)

---

## 💡 Documentation Tips

### Reading Efficiently

- **Scannable Headers**: Use headers to jump to relevant sections
- **Code Examples**: All examples are copy-paste ready
- **Internal Links**: Click links to related sections
- **Tables**: Quick reference for comparisons

### Using the Docs

**First Time User:**
```bash
# Follow this sequence:
1. Read GETTING_STARTED.md
2. Do the Quick Install
3. Run your first scan
4. Browse USER_GUIDE.md as needed
```

**Returning User:**
```bash
# Quick lookup:
- Need a command? → USER_GUIDE.md
- Forgot a config? → USER_GUIDE.md → Configuration Guide
- Tool question? → TOOLS.md
- Feature details? → FEATURES.md
```

**Developer:**
```bash
# Development workflow:
1. Read DEVELOPMENT.md completely
2. Explore actual codebase
3. Refer back to DEVELOPMENT.md for patterns
```

---

## 🎯 What's Covered

### ✅ GETTING_STARTED.md

Complete setup guide covering:
- Prerequisites and installation
- Automatic tool management
- Running your first scan
- Understanding reports
- Configuration basics
- Troubleshooting
- Verification checklist

**Who needs this:** Everyone (start here!)

---

### ✅ USER_GUIDE.md

Comprehensive reference covering:
- All CLI commands
- Configuration templates
- Tool-specific arguments
- Output formats
- Common workflows
- Severity levels
- HTML report features
- Advanced configurations
- CI/CD integrations
- Troubleshooting guide
- Best practices

**Who needs this:** Daily users, DevOps, Security teams

---

### ✅ FEATURES.md

Feature deep-dives covering:
- 4 security categories (IaC, SCA, SAST, Secrets)
- 3 report formats (JSON, HTML, SARIF)
- Automatic tool management
- Interactive report filtering
- Unified output schema
- CI/CD integration
- Advanced features
- Feature roadmap

**Who needs this:** Everyone wanting to understand capabilities

---

### ✅ TOOLS.md

Tool-specific guides covering:
- **Checkov**: IaC scanning, frameworks, arguments
- **Trivy**: SCA scanning, languages, performance
- **Semgrep**: SAST scanning, rulesets, customization
- **Gitleaks**: Secrets detection, patterns, configuration
- Tool comparison
- When to use each tool
- Tool-specific tips

**Who needs this:** Users wanting deep tool knowledge

---

### ✅ DEVELOPMENT.md

Developer documentation covering:
- Project structure
- Architecture overview
- Design principles
- Data flow
- Adding new security tools (step-by-step)
- Testing procedures
- Code style guide
- Debugging tips
- Release process
- Contributing guidelines

**Who needs this:** Contributors, developers, maintainers

---

### ✅ CHANGELOG.md

Version history covering:
- Release notes for all versions
- New features per release
- Breaking changes
- Bug fixes
- Roadmap for future versions

**Who needs this:** Everyone tracking updates

---

## 📈 Documentation Stats

| Metric | Value |
|--------|-------|
| **Total Documents** | 6 core files + README |
| **Total Lines** | ~3,000 lines |
| **Estimated Reading Time** | 95 minutes (complete) |
| **Code Examples** | 100+ |
| **Quick Start Time** | 10 minutes |
| **Reduction from Previous** | 22 files → 6 files (73% reduction) |

---

## 🎨 Documentation Features

✅ **Clear Structure** - Logical organization, easy to navigate  
✅ **Scannable** - Headers, tables, lists for quick lookup  
✅ **Complete** - Everything documented, no gaps  
✅ **Examples** - Real code, real commands, copy-paste ready  
✅ **Cross-Referenced** - Links between related sections  
✅ **Progressive** - Start simple, get detailed as needed  
✅ **Maintained** - Updated with each release  

---

## 🆘 Need Help?

### Quick Answers

| Question | Answer |
|----------|--------|
| How do I install? | [GETTING_STARTED.md](GETTING_STARTED.md) |
| What are the commands? | [USER_GUIDE.md](USER_GUIDE.md) → Quick Command Reference |
| How do I configure X? | [USER_GUIDE.md](USER_GUIDE.md) → Configuration Guide |
| What does Tool Y do? | [TOOLS.md](TOOLS.md) → Find your tool |
| How does Feature Z work? | [FEATURES.md](FEATURES.md) → Search for feature |
| Something's not working | [GETTING_STARTED.md](GETTING_STARTED.md) → Troubleshooting |

### Still Stuck?

1. **Search this documentation** - Use Ctrl/Cmd+F
2. **Check examples** - See `examples/` directory in project
3. **Review changelog** - [CHANGELOG.md](CHANGELOG.md) for recent changes
4. **Open an issue** - GitHub Issues for bug reports
5. **Start a discussion** - GitHub Discussions for questions

---

## 🔗 External Resources

- **Main README**: [../README.md](../README.md)
- **GitHub Repository**: https://github.com/jaganraj/1security
- **License**: [../LICENSE](../LICENSE)
- **Example Configs**: `../examples/`

---

## 📝 Documentation Principles

Our documentation follows these principles:

1. **Start Simple** - Quick start first, details later
2. **Be Complete** - Cover everything, leave no gaps
3. **Show Examples** - Code speaks louder than words
4. **Stay Current** - Update with every release
5. **Be Scannable** - Headers, tables, lists
6. **Cross-Reference** - Link related content
7. **Be Practical** - Focus on real usage

---

## 🎉 Documentation Improvements (Nov 2025)

### What Changed

**Before:** 22 scattered files, significant overlap, hard to navigate  
**After:** 6 focused files, clear structure, easy to find information

### Consolidations Made

```
QUICKSTART.md + INSTALLATION.md + TOOL_MANAGEMENT.md
  → GETTING_STARTED.md

QUICK_REFERENCE.md + usage examples
  → USER_GUIDE.md

FEATURE_*.md files + REPORT_FILTERING.md + Phase docs
  → FEATURES.md

TRIVY_INTEGRATION.md + other tool docs
  → TOOLS.md

CODE_REVIEW.md + implementation docs
  → DEVELOPMENT.md

CHANGES.md
  → CHANGELOG.md
```

### Benefits

✅ **73% Fewer Files** - Easier to manage  
✅ **Zero Redundancy** - Each topic covered once  
✅ **Better Organization** - Logical grouping  
✅ **Faster Navigation** - Find what you need quickly  
✅ **Easier Maintenance** - Update one place, not many  
✅ **Professional** - Industry-standard structure  

---

## 📞 Feedback

Found an issue with the documentation? Please:
- **Open an issue** on GitHub
- **Suggest improvements** in Discussions
- **Submit a PR** to fix it yourself

We appreciate your feedback!

---

**Version**: 1Security v0.2.0  
**Documentation Status**: Complete & Optimized ✅  
**Last Updated**: November 21, 2025

---

*Clean, comprehensive, and easy to navigate - documentation done right.* 🚀

---

**1Security** | MIT License | R Jagan Raj
