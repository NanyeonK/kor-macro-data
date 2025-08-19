"""
Korean Macro Data Package

A comprehensive Python package for accessing, merging, and analyzing 
Korean economic and real estate data with automatic integrity validation.
"""

__version__ = "1.0.0"
__author__ = "NanyeonK"
__email__ = "your.email@example.com"

from .data_merger import KoreanMacroDataMerger
from .data_integrity_checker import DataIntegrityChecker

__all__ = [
    'KoreanMacroDataMerger',
    'DataIntegrityChecker',
    '__version__',
]

# Convenience function
def quick_merge_korean_data(**kwargs):
    """Quick merge function for Korean macro data."""
    merger = KoreanMacroDataMerger()
    return merger.create_research_dataset(**kwargs)