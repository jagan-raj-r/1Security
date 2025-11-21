"""
Helper to read version from core package
"""
import re
from pathlib import Path


def get_version():
    """Read version from core/__init__.py"""
    init_file = Path(__file__).parent / "core" / "__init__.py"
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return "0.0.0"


__version__ = get_version()

