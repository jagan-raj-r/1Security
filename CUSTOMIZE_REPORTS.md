# 🎨 Customizing 1Security HTML Reports

## Overview

The HTML template is defined in `core/reporters/html_reporter.py` as a constant string (`HTML_TEMPLATE`). It uses **Jinja2** templating to render dynamic data at runtime.

---

## Quick Customization Guide

### 1. Change Colors

**Location:** `core/reporters/html_reporter.py` → `HTML_TEMPLATE` → `<style>` section

**Example - Change Header Color:**

```python
# Find this section (around line 175):
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  # Current: Purple gradient
    color: white;
    padding: 2rem;
}

# Change to:
header {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);  # Blue gradient
    color: white;
    padding: 2rem;
}
```

**Example - Change Severity Badge Colors:**

```python
# Find severity color function (around line 110):
@staticmethod
def _get_severity_color(severity: str) -> str:
    colors = {
        "CRITICAL": "#dc2626",  # Red - Keep for critical
        "HIGH": "#ea580c",      # Orange - Change to #ff6b00 for brighter
        "MEDIUM": "#ca8a04",    # Yellow - Change to #fbbf24 for softer
        "LOW": "#16a34a",       # Green - Keep
        "INFO": "#0284c7",      # Blue - Keep
    }
    return colors.get(severity, "#6b7280")
```

---

### 2. Change Fonts

**Current Font Stack:**
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
```

**Custom Font:**
```css
/* Add Google Font in <head>: */
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

/* Then in body style: */
body {
    font-family: 'Inter', sans-serif;
    ...
}
```

---

### 3. Add Company Logo

**Find the header section (around line 252):**

```html
<!-- Current: -->
<header>
    <h1>🔒 1Security Report</h1>
    <div class="meta">...</div>
</header>

<!-- Change to: -->
<header>
    <div style="display: flex; align-items: center; gap: 1rem;">
        <img src="https://your-company.com/logo.png" alt="Logo" style="height: 40px;">
        <h1>🔒 1Security Report</h1>
    </div>
    <div class="meta">...</div>
</header>
```

---

### 4. Change Layout/Spacing

**Make Summary Cards Larger:**

```css
.summary-card {
    background: white;
    padding: 2rem;  /* Change from 1.5rem to 2rem */
    border-radius: 8px;
    border-left: 4px solid #667eea;
}
```

**Adjust Table Density:**

```css
.findings-table td {
    padding: 1.5rem;  /* Change from 1rem to 1.5rem for more breathing room */
    border-bottom: 1px solid #e5e7eb;
}
```

---

## Advanced: External Template File

For easier management in the future, move the template to an external file.

### Step 1: Create Template Directory

```bash
mkdir -p core/reporters/templates
```

### Step 2: Move Template to File

```bash
# Create the file
touch core/reporters/templates/report.html

# Copy the HTML_TEMPLATE content to this file
```

### Step 3: Update html_reporter.py

```python
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path

class HTMLReporter:
    def __init__(self, output_path: Path):
        self.output_path = Path(output_path)
        # Load template from file
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    def _render_template(self, project_name: str, summary: dict, 
                        scan_results: List[ScanResult], all_findings: List[dict]) -> str:
        """Render HTML template from file."""
        
        # Load template from file instead of string
        template = self.env.get_template('report.html')
        
        return template.render(
            project_name=project_name,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary=summary,
            scan_results=scan_results,
            all_findings=all_findings,
            get_severity_color=self._get_severity_color,
            get_severity_badge=self._get_severity_badge,
        )
```

**Benefits:**
- ✅ Easier to edit (syntax highlighting)
- ✅ Can use template inheritance
- ✅ Separate concerns (code vs presentation)
- ✅ Easier version control for templates

---

## Template Variables Reference

These Jinja2 variables are available in the template:

| Variable | Type | Description |
|----------|------|-------------|
| `project_name` | string | From config.yaml |
| `generated_at` | string | Timestamp of report generation |
| `summary` | dict | Contains `total_findings`, `severity_count`, `tools_count` |
| `scan_results` | list | List of ScanResult objects |
| `all_findings` | list | List of all findings (dicts) |
| `get_severity_color()` | function | Returns hex color for severity |
| `get_severity_badge()` | function | Returns CSS class for severity |

### Usage Examples:

```html
<!-- Display project name -->
<h1>{{ project_name }}</h1>

<!-- Loop through findings -->
{% for finding in all_findings %}
    <tr>
        <td>{{ finding.title }}</td>
        <td>{{ finding.severity }}</td>
    </tr>
{% endfor %}

<!-- Conditional rendering -->
{% if summary.total_findings > 0 %}
    <p>Found {{ summary.total_findings }} issues!</p>
{% else %}
    <p>No issues found!</p>
{% endif %}

<!-- Use Python functions -->
<span style="color: {{ get_severity_color(finding.severity) }}">
    {{ finding.severity }}
</span>
```

---

## Dark Mode Example

Add a dark mode toggle by including this CSS:

```css
@media (prefers-color-scheme: dark) {
    body {
        background: #1f2937;
        color: #f3f4f6;
    }
    
    .container {
        background: #111827;
    }
    
    .findings-table tr:hover {
        background: #374151;
    }
    
    /* ... more dark mode styles ... */
}
```

---

## Multiple Template Support (Future)

For Phase 3, support multiple report templates:

```python
# In orchestrator or config
template_choices = {
    "default": "report.html",
    "executive": "executive_summary.html",
    "detailed": "detailed_report.html",
    "dark": "report_dark.html"
}

# In config.yaml
output:
  format: html
  html_template: executive  # Choose template
```

---

## Tips

1. **Test Changes Locally** - Make changes, run a scan, check the output
2. **Keep Backups** - Copy original template before major changes
3. **Use Browser DevTools** - Open report in browser, inspect elements, test CSS changes
4. **Responsive Design** - Test on mobile/tablet if needed
5. **Performance** - Keep CSS inline for now (single file distribution)

---

## Common Customizations

### Add More Summary Stats

```html
<!-- In summary section -->
<div class="summary-card">
    <h3>Scan Duration</h3>
    <div class="value">{{ scan_duration }}s</div>
</div>
```

### Add Filtering/Search

```html
<input type="text" id="searchFindings" placeholder="Search findings...">
<script>
document.getElementById('searchFindings').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('.findings-table tbody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
});
</script>
```

### Export to PDF Button

```html
<button onclick="window.print()">Export to PDF</button>
<style>
@media print {
    /* Print-specific styles */
}
</style>
```

---

## Need Help?

- Check Jinja2 docs: https://jinja.palletsprojects.com/
- MDN CSS reference: https://developer.mozilla.org/en-US/docs/Web/CSS
- Open an issue on GitHub

---

**Remember:** The template is reused for every scan, so changes affect all future reports!

