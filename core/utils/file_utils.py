"""
File utility functions
"""
from pathlib import Path
from typing import Union
import os


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


def make_path_relative(file_path: str) -> str:
    """
    Convert absolute path to relative path if possible.
    Centralized utility used by all parsers.
    
    Args:
        file_path: File path (absolute or relative)
        
    Returns:
        Relative path string
    """
    if not file_path:
        return ""
    
    if file_path.startswith("/"):
        try:
            return str(Path(file_path).relative_to(Path.cwd()))
        except ValueError:
            pass  # Keep absolute path if can't make relative
    
    return file_path


def validate_path(path: Union[str, Path], base_dir: Union[str, Path] = None) -> Path:
    """
    Validate and sanitize file path to prevent path traversal attacks.
    
    Args:
        path: Path to validate
        base_dir: Base directory to restrict access to (defaults to cwd)
        
    Returns:
        Validated Path object
        
    Raises:
        ValueError: If path attempts traversal outside base directory
    """
    if not path:
        raise ValueError("Path cannot be empty")
    
    path = Path(path)
    base_dir = Path(base_dir) if base_dir else Path.cwd()
    
    # Resolve to absolute path
    try:
        resolved_path = path.resolve()
        resolved_base = base_dir.resolve()
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Invalid path: {e}")
    
    # Check if resolved path is within base directory
    try:
        resolved_path.relative_to(resolved_base)
    except ValueError:
        raise ValueError(
            f"Path traversal detected: {path} is outside {base_dir}"
        )
    
    return resolved_path


def safe_join(base: Union[str, Path], *paths: str) -> Path:
    """
    Safely join paths, preventing path traversal.
    
    Args:
        base: Base directory
        *paths: Path components to join
        
    Returns:
        Safe joined Path
        
    Raises:
        ValueError: If resulting path is outside base directory
    """
    base = Path(base)
    joined = base.joinpath(*paths)
    return validate_path(joined, base)

