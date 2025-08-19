"""
Setup configuration for Korean Macro Data Package
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kor-macro-data",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive Python package for Korean economic and real estate data with automatic merging and integrity validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kor-macro-data",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/kor-macro-data/issues",
        "Documentation": "https://github.com/yourusername/kor-macro-data/wiki",
        "Source Code": "https://github.com/yourusername/kor-macro-data",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
        "viz": [
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
            "plotly>=5.14.0",
        ],
        "ml": [
            "scikit-learn>=1.3.0",
            "statsmodels>=0.14.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kor-macro=kor_macro.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "kor_macro": [
            "data/*.csv",
            "config/*.json",
            "templates/*.html",
        ],
    },
    keywords=[
        "korea",
        "economics",
        "finance",
        "real-estate",
        "data",
        "api",
        "bok",
        "kosis",
        "fred",
        "time-series",
        "econometrics",
        "jeonse",
        "housing",
        "macroeconomics",
    ],
)