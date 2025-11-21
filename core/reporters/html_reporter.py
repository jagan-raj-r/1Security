"""
HTML reporter for 1Security scan results
"""
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from jinja2 import Template
from core.schema import ScanResult
from core.constants import HTML_REPORT_NAME
from core.utils.severity_utils import get_severity_order


class HTMLReporter:
    """Generate HTML reports from scan results."""
    
    def __init__(self, output_path: Path):
        """
        Initialize HTML reporter.
        
        Args:
            output_path: Directory to write reports to
        """
        self.output_path = Path(output_path)
        
    def generate(self, scan_results: List[ScanResult], config: Dict[str, Any]) -> Path:
        """
        Generate HTML report.
        
        Args:
            scan_results: List of ScanResult objects
            config: Configuration dictionary
            
        Returns:
            Path to generated HTML file
        """
        # Create output directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Collect data
        summary = self._generate_summary(scan_results)
        all_findings = self._collect_all_findings(scan_results)
        
        # Render template
        html_content = self._render_template(
            project_name=config.get("project", "Unknown Project"),
            summary=summary,
            scan_results=scan_results,
            all_findings=all_findings,
        )
        
        # Write to file
        output_file = self.output_path / HTML_REPORT_NAME
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_file
    
    def _generate_summary(self, scan_results: List[ScanResult]) -> dict:
        """Generate summary statistics."""
        total_findings = sum(len(sr.findings) for sr in scan_results)
        
        severity_count = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "INFO": 0,
        }
        
        for scan_result in scan_results:
            for finding in scan_result.findings:
                severity = finding.severity
                if severity in severity_count:
                    severity_count[severity] += 1
        
        return {
            "total_findings": total_findings,
            "severity_count": severity_count,
            "tools_count": len(scan_results),
        }
    
    def _collect_all_findings(self, scan_results: List[ScanResult]) -> List[dict]:
        """Collect all findings from all scans."""
        all_findings = []
        
        for scan_result in scan_results:
            for finding in scan_result.findings:
                all_findings.append(finding.to_dict())
        
        # Sort by severity
        all_findings.sort(key=lambda f: get_severity_order(f.get("severity", "UNKNOWN")))
        
        return all_findings
    
    def _render_template(self, project_name: str, summary: dict, 
                        scan_results: List[ScanResult], all_findings: List[dict]) -> str:
        """Render HTML template."""
        
        template = Template(HTML_TEMPLATE)
        
        return template.render(
            project_name=project_name,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary=summary,
            scan_results=scan_results,
            all_findings=all_findings,
            get_severity_color=self._get_severity_color,
            get_severity_badge=self._get_severity_badge,
        )
    
    @staticmethod
    def _get_severity_color(severity: str) -> str:
        """Get color for severity level."""
        colors = {
            "CRITICAL": "#dc2626",
            "HIGH": "#ea580c",
            "MEDIUM": "#ca8a04",
            "LOW": "#16a34a",
            "INFO": "#0284c7",
        }
        return colors.get(severity, "#6b7280")
    
    @staticmethod
    def _get_severity_badge(severity: str) -> str:
        """Get badge class for severity level."""
        badges = {
            "CRITICAL": "critical",
            "HIGH": "high",
            "MEDIUM": "medium",
            "LOW": "low",
            "INFO": "info",
        }
        return badges.get(severity, "unknown")


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1Security Report - {{ project_name }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: #f9fafb;
            padding: 2rem;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
        }
        
        header h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        header .meta {
            opacity: 0.9;
            font-size: 0.9rem;
        }
        
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            background: #f9fafb;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .summary-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .summary-card h3 {
            font-size: 0.875rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .summary-card .value {
            font-size: 2rem;
            font-weight: bold;
            color: #1f2937;
        }
        
        .summary-card.critical { border-left-color: #dc2626; }
        .summary-card.high { border-left-color: #ea580c; }
        .summary-card.medium { border-left-color: #ca8a04; }
        .summary-card.low { border-left-color: #16a34a; }
        .summary-card.info { border-left-color: #0284c7; }
        
        .content {
            padding: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #1f2937;
        }
        
        .filters {
            background: #f9fafb;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            border: 1px solid #e5e7eb;
        }
        
        .filters h3 {
            font-size: 1rem;
            margin-bottom: 1rem;
            color: #374151;
            font-weight: 600;
        }
        
        .filter-group {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .filter-btn {
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: 2px solid #d1d5db;
            background: white;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s;
            color: #6b7280;
        }
        
        .filter-btn:hover {
            border-color: #667eea;
            color: #667eea;
        }
        
        .filter-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .search-box {
            width: 100%;
            max-width: 400px;
            padding: 0.75rem 1rem;
            border: 2px solid #d1d5db;
            border-radius: 6px;
            font-size: 0.875rem;
            transition: border-color 0.2s;
        }
        
        .search-box:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .stats-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: #f9fafb;
            border-radius: 6px;
            margin-bottom: 1rem;
            font-size: 0.875rem;
            color: #6b7280;
        }
        
        .reset-btn {
            padding: 0.5rem 1rem;
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            transition: background 0.2s;
        }
        
        .reset-btn:hover {
            background: #dc2626;
        }
        
        .findings-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .findings-table thead {
            background: #f9fafb;
        }
        
        .findings-table th {
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.875rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 2px solid #e5e7eb;
        }
        
        .findings-table td {
            padding: 1rem;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .findings-table tr:hover {
            background: #f9fafb;
        }
        
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .badge.critical {
            background: #fee2e2;
            color: #991b1b;
        }
        
        .badge.high {
            background: #ffedd5;
            color: #9a3412;
        }
        
        .badge.medium {
            background: #fef3c7;
            color: #854d0e;
        }
        
        .badge.low {
            background: #dcfce7;
            color: #166534;
        }
        
        .badge.info {
            background: #dbeafe;
            color: #1e40af;
        }
        
        .code {
            font-family: 'Courier New', monospace;
            font-size: 0.875rem;
            color: #4b5563;
        }
        
        .location {
            color: #6b7280;
            font-size: 0.875rem;
        }
        
        .description {
            color: #4b5563;
            font-size: 0.875rem;
            max-width: 500px;
        }
        
        .no-findings {
            text-align: center;
            padding: 3rem;
            color: #6b7280;
        }
        
        .no-findings .icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        footer {
            padding: 1.5rem 2rem;
            background: #f9fafb;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
            font-size: 0.875rem;
        }
        
        .tool-badge {
            background: #e0e7ff;
            color: #3730a3;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔒 1Security Report</h1>
            <div class="meta">
                <strong>Project:</strong> {{ project_name }} | 
                <strong>Generated:</strong> {{ generated_at }}
            </div>
        </header>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Findings</h3>
                <div class="value">{{ summary.total_findings }}</div>
            </div>
            <div class="summary-card critical">
                <h3>Critical</h3>
                <div class="value">{{ summary.severity_count.CRITICAL }}</div>
            </div>
            <div class="summary-card high">
                <h3>High</h3>
                <div class="value">{{ summary.severity_count.HIGH }}</div>
            </div>
            <div class="summary-card medium">
                <h3>Medium</h3>
                <div class="value">{{ summary.severity_count.MEDIUM }}</div>
            </div>
            <div class="summary-card low">
                <h3>Low</h3>
                <div class="value">{{ summary.severity_count.LOW }}</div>
            </div>
            <div class="summary-card info">
                <h3>Info</h3>
                <div class="value">{{ summary.severity_count.INFO }}</div>
            </div>
        </div>
        
        <div class="content">
            <h2>Security Findings</h2>
            
            {% if all_findings %}
            
            <!-- Filters Section -->
            <div class="filters">
                <h3>🔍 Filter Results</h3>
                
                <div style="margin-bottom: 1rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: #374151;">Search:</label>
                    <input type="text" id="searchBox" class="search-box" placeholder="Search by title, file, or check ID...">
                </div>
                
                <div style="margin-bottom: 1rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: #374151;">Filter by Tool:</label>
                    <div class="filter-group" id="toolFilters">
                        <button class="filter-btn active" data-filter="all" data-type="tool">All Tools</button>
                        <button class="filter-btn" data-filter="checkov" data-type="tool">Checkov</button>
                        <button class="filter-btn" data-filter="trivy" data-type="tool">Trivy</button>
                        <button class="filter-btn" data-filter="semgrep" data-type="tool">Semgrep</button>
                        <button class="filter-btn" data-filter="gitleaks" data-type="tool">Gitleaks</button>
                    </div>
                </div>
                
                <div style="margin-bottom: 1rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: #374151;">Filter by Severity:</label>
                    <div class="filter-group" id="severityFilters">
                        <button class="filter-btn active" data-filter="all" data-type="severity">All Severities</button>
                        <button class="filter-btn" data-filter="CRITICAL" data-type="severity" style="border-color: #dc2626; color: #dc2626;">Critical</button>
                        <button class="filter-btn" data-filter="HIGH" data-type="severity" style="border-color: #ea580c; color: #ea580c;">High</button>
                        <button class="filter-btn" data-filter="MEDIUM" data-type="severity" style="border-color: #ca8a04; color: #ca8a04;">Medium</button>
                        <button class="filter-btn" data-filter="LOW" data-type="severity" style="border-color: #16a34a; color: #16a34a;">Low</button>
                        <button class="filter-btn" data-filter="INFO" data-type="severity" style="border-color: #0284c7; color: #0284c7;">Info</button>
                    </div>
                </div>
                
                <div style="margin-bottom: 1rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: #374151;">Filter by Category:</label>
                    <div class="filter-group" id="categoryFilters">
                        <button class="filter-btn active" data-filter="all" data-type="category">All Categories</button>
                        <button class="filter-btn" data-filter="iac" data-type="category">IaC</button>
                        <button class="filter-btn" data-filter="sca" data-type="category">SCA</button>
                        <button class="filter-btn" data-filter="sast" data-type="category">SAST</button>
                        <button class="filter-btn" data-filter="secrets" data-type="category">Secrets</button>
                    </div>
                </div>
                
                <button class="reset-btn" onclick="resetFilters()">Reset All Filters</button>
            </div>
            
            <!-- Stats Bar -->
            <div class="stats-bar">
                <span id="statsText">Showing <strong id="visibleCount">{{ all_findings|length }}</strong> of <strong>{{ all_findings|length }}</strong> findings</span>
            </div>
            
            <table class="findings-table">
                <thead>
                    <tr>
                        <th>Severity</th>
                        <th>Tool</th>
                        <th>Title</th>
                        <th>Location</th>
                        <th>Check ID</th>
                    </tr>
                </thead>
                <tbody>
                    {% for finding in all_findings %}
                    <tr class="finding-row" 
                        data-tool="{{ finding.tool }}" 
                        data-severity="{{ finding.severity }}" 
                        data-category="{{ finding.category }}"
                        data-search="{{ finding.title|lower }} {{ finding.description|lower }} {{ finding.file|lower }} {{ finding.check_id|lower }} {{ finding.rule_id|lower }}">
                        <td>
                            <span class="badge {{ get_severity_badge(finding.severity) }}">
                                {{ finding.severity }}
                            </span>
                        </td>
                        <td>
                            <span class="tool-badge">{{ finding.tool }}</span>
                        </td>
                        <td>
                            <div style="margin-bottom: 0.25rem;">{{ finding.title }}</div>
                            <div class="description">{{ finding.description }}</div>
                        </td>
                        <td>
                            <div class="location">
                                {% if finding.file %}
                                    <strong>{{ finding.file }}</strong>
                                    {% if finding.line %}:{{ finding.line }}{% endif %}
                                {% elif finding.resource %}
                                    {{ finding.resource }}
                                {% else %}
                                    N/A
                                {% endif %}
                            </div>
                        </td>
                        <td>
                            <span class="code">{{ finding.check_id or finding.rule_id or 'N/A' }}</span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="no-findings">
                <div class="icon">✅</div>
                <h3>No Security Issues Found</h3>
                <p>All security checks passed successfully!</p>
            </div>
            {% endif %}
        </div>
        
        <footer>
            <strong>1Security</strong> - Open Source ASPM Orchestrator | 
            Generated by 1Security v0.2.0
        </footer>
    </div>
    
    <script>
        // Filter state
        let filters = {
            tool: 'all',
            severity: 'all',
            category: 'all',
            search: ''
        };
        
        // Get all finding rows
        const findingRows = document.querySelectorAll('.finding-row');
        const totalFindings = findingRows.length;
        
        // Apply filters
        function applyFilters() {
            let visibleCount = 0;
            
            findingRows.forEach(row => {
                const tool = row.dataset.tool;
                const severity = row.dataset.severity;
                const category = row.dataset.category;
                const searchText = row.dataset.search;
                
                // Check if row matches all filters
                const matchesTool = filters.tool === 'all' || tool === filters.tool;
                const matchesSeverity = filters.severity === 'all' || severity === filters.severity;
                const matchesCategory = filters.category === 'all' || category === filters.category;
                const matchesSearch = filters.search === '' || searchText.includes(filters.search.toLowerCase());
                
                if (matchesTool && matchesSeverity && matchesCategory && matchesSearch) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            // Update stats
            document.getElementById('visibleCount').textContent = visibleCount;
            
            // Show message if no results
            const tbody = document.querySelector('.findings-table tbody');
            let noResultsRow = document.getElementById('noResultsRow');
            
            if (visibleCount === 0) {
                if (!noResultsRow) {
                    noResultsRow = document.createElement('tr');
                    noResultsRow.id = 'noResultsRow';
                    noResultsRow.innerHTML = '<td colspan="5" style="text-align: center; padding: 3rem; color: #6b7280;"><div style="font-size: 2rem; margin-bottom: 1rem;">🔍</div><h3>No findings match your filters</h3><p>Try adjusting your filters or reset them.</p></td>';
                    tbody.appendChild(noResultsRow);
                }
            } else {
                if (noResultsRow) {
                    noResultsRow.remove();
                }
            }
        }
        
        // Handle filter button clicks
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const filterType = this.dataset.type;
                const filterValue = this.dataset.filter;
                
                // Update active state
                const group = this.parentElement;
                group.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                // Update filter state
                filters[filterType] = filterValue;
                
                // Apply filters
                applyFilters();
            });
        });
        
        // Handle search input
        const searchBox = document.getElementById('searchBox');
        searchBox.addEventListener('input', function() {
            filters.search = this.value;
            applyFilters();
        });
        
        // Reset all filters
        function resetFilters() {
            filters = {
                tool: 'all',
                severity: 'all',
                category: 'all',
                search: ''
            };
            
            // Reset search box
            searchBox.value = '';
            
            // Reset all filter buttons
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.filter === 'all') {
                    btn.classList.add('active');
                }
            });
            
            // Apply filters
            applyFilters();
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + K to focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchBox.focus();
            }
            
            // Escape to clear search
            if (e.key === 'Escape' && document.activeElement === searchBox) {
                searchBox.value = '';
                filters.search = '';
                applyFilters();
            }
        });
        
        // Add keyboard shortcut hint
        searchBox.placeholder = 'Search... (Ctrl+K or Cmd+K)';
    </script>
</body>
</html>
"""

