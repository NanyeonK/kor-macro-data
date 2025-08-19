# Changelog

All notable changes to the Korean Macro Data package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-08-19

### 🎉 Initial Release

#### Added
- **Core Features**
  - Comprehensive Korean economic data API connectors
  - Automatic data merging with temporal alignment
  - Data integrity validation system
  - English column name standardization
  - Time-based aggregation (daily, weekly, monthly, quarterly, yearly)

- **Data Sources**
  - Bank of Korea (BOK) ECOS API connector - 863+ economic statistics
  - KOSIS (Korean Statistical Information Service) connector
  - KB Land real estate data connector with Excel support
  - FRED (Federal Reserve Economic Data) global indicators
  - Seoul Open Data portal connector
  - Support for World Bank and IMF data (experimental)

- **Data Integrity System**
  - Automatic date shift detection
  - Temporal alignment validation
  - Value mapping verification
  - Frequency conversion checks
  - Complete date series validation
  - Detailed integrity reports

- **Data Processing**
  - Multi-source data merging
  - Automatic frequency harmonization
  - Missing data handling with forward-fill for quarterly/annual data
  - Derived features (percentage changes, YoY growth)
  - Support for multiple output formats (CSV, Excel, Parquet)

- **Column Standardization**
  - Korean to English translation for all column names
  - Consistent naming conventions across data sources
  - Comprehensive column mapping dictionary

- **Documentation**
  - Complete API documentation
  - Usage examples and tutorials
  - Data source catalog
  - Contributing guidelines
  - Integration guides for R, Stata, MATLAB

- **Quality Assurance**
  - Unit tests for core functionality
  - Integration tests for API connectors
  - Example scripts and notebooks
  - Performance benchmarks

#### Key Components
- `KoreanMacroDataMerger`: Main class for data merging and aggregation
- `DataIntegrityChecker`: Validates temporal alignment and data quality
- `BOKConnector`: Bank of Korea ECOS API interface
- `KOSISConnector`: Korean statistics portal interface
- `KBLandEnhancedConnector`: Real estate data with Excel support
- `FREDConnector`: Global economic indicators interface

#### Example Datasets Included
- `korean_macro_complete.csv`: 180 months × 46 indicators (2010-2024)
- Complete BOK monetary policy data
- Real estate price indices (housing, jeonse, monthly rent)
- Employment and demographic statistics
- Global economic indicators (Fed rate, oil prices, VIX)

### Technical Details
- **Python Support**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Dependencies**: pandas 2.0+, numpy 1.24+, requests 2.31+
- **License**: MIT

### Known Issues
- KB Land Excel files may have encoding issues with certain Korean characters
- Some KOSIS employment data only available until 2017
- CNY/KRW exchange rate data starts from 2016 (BOK limitation)

### Performance
- Monthly aggregation: ~1-2 seconds for 10 years of daily data
- Merging 10+ datasets: ~3-5 seconds
- Integrity validation: <1 second for standard datasets

### Contributors
- Initial development and release

---

## [Unreleased]

### Planned Features
- Additional visualization modules
- Machine learning integration for forecasting
- Real-time data streaming support
- Enhanced CLI with interactive mode
- Web dashboard for data exploration
- Additional language support (Japanese, Chinese)

### Under Consideration
- Docker containerization
- REST API server mode
- Cloud storage integration (AWS S3, Google Cloud Storage)
- Automated data quality monitoring
- Historical data backfilling utilities

---

## Version History

### Pre-release Development

#### [0.9.0] - 2024-08-15 (Beta)
- Beta testing with selected users
- Performance optimizations
- Bug fixes from alpha testing

#### [0.8.0] - 2024-08-10 (Alpha)
- Alpha release for internal testing
- Core functionality implemented
- Basic documentation

#### [0.7.0] - 2024-08-01 (Pre-alpha)
- Initial proof of concept
- BOK and KOSIS connectors
- Basic merging functionality

---

## Upgrade Guide

### From 0.x to 1.0.0

1. **API Changes**
   - `merge_data()` now includes automatic integrity checking by default
   - Column names have been standardized to English
   - New `run_integrity_check` parameter in save methods

2. **Configuration**
   - API keys now use environment variables
   - New `.env` file format for configuration

3. **Breaking Changes**
   - Korean column names no longer supported directly
   - Must use `COLUMN_MAPPINGS` for translation

### Migration Example

Before (0.x):
```python
merger = DataMerger()
merger.merge_data(files, output='merged.csv')
```

After (1.0.0):
```python
merger = KoreanMacroDataMerger()
merger.load_data('file.csv', 'name', source='bok')
merger.save_merged_data('merged.csv', run_integrity_check=True)
```

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/yourusername/kor-macro-data/issues
- Documentation: https://kor-macro-data.readthedocs.io
- Email: support@kor-macro-data.org