"""
File utility functions
"""
from pathlib import Path
from typing import Union


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def clean_path(path: Union[str, Path]) -> str:
    """
    Clean and normalize path.
    
    Args:
        path: File or directory path
        
    Returns:
        Cleaned path string
    """
    if not path:
        return ""
    
    path = Path(path)
    try:
        # Try to make it relative to current directory
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        # If not possible, return as is
        return str(path)


def get_relative_path(path: Union[str, Path], base: Union[str, Path] = None) -> str:
    """
    Get relative path from base directory.
    
    Args:
        path: Target path
        base: Base directory (defaults to cwd)
        
    Returns:
        Relative path string
    """
    if not path:
        return ""
    
    path = Path(path)
    base = Path(base) if base else Path.cwd()
    
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)

