#!/usr/bin/env python3
"""
Path Configuration Module for Weekly Video Production
Provides centralized path management for weekly video pipeline.
"""

from datetime import date
from pathlib import Path
from typing import Dict, Optional


def get_repo_root() -> Path:
    """
    Get the repository root directory.
    Assumes this file is in 5_Symbols/ directory.
    """
    return Path(__file__).resolve().parent.parent


def get_simulations_base() -> Path:
    """Get the base 3_Simulations directory."""
    return get_repo_root() / "3_Simulation"


def generate_weekly_id(week_date: Optional[date] = None) -> str:
    """
    Generate a weekly ID string based on date.
    
    Args:
        week_date: Optional date object. If None, uses today's date.
    
    Returns:
        Weekly ID string in format 'YYYY-MM-DD'
    
    Example:
        >>> generate_weekly_id(date(2026, 2, 10))
        '2026-02-10'
    """
    if week_date is None:
        week_date = date.today()
    return week_date.strftime("%Y-%m-%d")


def get_weekly_paths(weekly_id: Optional[str] = None) -> Dict[str, Path]:
    """
    Get input and output paths for a weekly video production.
    
    Args:
        weekly_id: Optional weekly identifier (e.g., '2026-02-10').
                  If None, generates one based on today's date.
    
    Returns:
        Dictionary with keys:
            - 'weekly_id': The weekly identifier used
            - 'base': Base directory for this week (3_Simulation/<weekly_id>)
            - 'input': Input directory (3_Simulation/<weekly_id>/input)
            - 'output': Output directory (3_Simulation/<weekly_id>/output)
    
    Example:
        >>> paths = get_weekly_paths('2026-02-10')
        >>> print(paths['input'])
        /path/to/repo/3_Simulation/2026-02-10/input
        >>> print(paths['output'])
        /path/to/repo/3_Simulation/2026-02-10/output
    """
    if weekly_id is None:
        weekly_id = generate_weekly_id()
    
    base_dir = get_simulations_base() / weekly_id
    
    return {
        'weekly_id': weekly_id,
        'base': base_dir,
        'input': base_dir / 'input',
        'output': base_dir / 'output',
    }


def ensure_weekly_structure(weekly_id: Optional[str] = None) -> Dict[str, Path]:
    """
    Ensure the weekly directory structure exists and return paths.
    Creates input/ and output/ directories if they don't exist.
    
    Args:
        weekly_id: Optional weekly identifier. If None, generates one based on today's date.
    
    Returns:
        Dictionary with weekly paths (same as get_weekly_paths)
    """
    paths = get_weekly_paths(weekly_id)
    
    # Create directories if they don't exist
    paths['input'].mkdir(parents=True, exist_ok=True)
    paths['output'].mkdir(parents=True, exist_ok=True)
    
    return paths


if __name__ == "__main__":
    # Example usage / self-test
    print("Path Configuration Module")
    print("=" * 60)
    print(f"Repository root: {get_repo_root()}")
    print(f"Simulations base: {get_simulations_base()}")
    print()
    
    # Test with today's date
    print("Using automatic weekly ID (today):")
    paths = get_weekly_paths()
    for key, value in paths.items():
        print(f"  {key}: {value}")
    print()
    
    # Test with explicit weekly ID
    print("Using explicit weekly ID '2026-02-10':")
    paths = get_weekly_paths('2026-02-10')
    for key, value in paths.items():
        print(f"  {key}: {value}")
    print()
    
    # Test structure creation
    print("Testing structure creation with '2026-02-10':")
    paths = ensure_weekly_structure('2026-02-10')
    print(f"  Created/verified: {paths['input']}")
    print(f"  Created/verified: {paths['output']}")
