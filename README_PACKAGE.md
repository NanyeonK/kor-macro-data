# Korean Macro Data Package

[![PyPI version](https://badge.fury.io/py/kor-macro-data.svg)](https://pypi.org/project/kor-macro-data/)
[![Python Support](https://img.shields.io/pypi/pyversions/kor-macro-data)](https://pypi.org/project/kor-macro-data/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/kor-macro-data/badge/?version=latest)](https://kor-macro-data.readthedocs.io/)
[![Downloads](https://pepy.tech/badge/kor-macro-data)](https://pepy.tech/project/kor-macro-data)

A comprehensive Python package for accessing, merging, and analyzing Korean economic and real estate data with automatic integrity validation.

## ✨ Key Features

- **🏦 Multi-Source Data Integration**: Bank of Korea, KOSIS, KB Land, FRED, and more
- **🔄 Automatic Data Merging**: Intelligent temporal alignment across different frequencies
- **✅ Data Integrity Validation**: Automatic detection of date shifts and misalignments
- **🌏 English Standardization**: All Korean column names automatically translated
- **📊 Flexible Aggregation**: Daily, weekly, monthly, quarterly, and yearly aggregation
- **🚀 High Performance**: Optimized for large datasets with minimal memory footprint
- **📈 Ready for Analysis**: Direct integration with pandas, R, Stata, and MATLAB

## 🎯 Why Korean Macro Data?

Researchers and analysts working with Korean economic data face several challenges:
- Multiple data sources with different formats and languages
- Complex date alignment across different frequencies
- Korean column names requiring translation
- Manual data validation and quality checks

This package solves these problems by providing:
- Unified API for all major Korean data sources
- Automatic data merging with integrity validation
- English standardization for all data fields
- Production-ready data for econometric analysis

## 📦 Installation

```bash
pip install kor-macro-data
```

For development version:
```bash
pip install git+https://github.com/yourusername/kor-macro-data.git
```

## 🚀 Quick Start

```python
from kor_macro import KoreanMacroDataMerger, BOKConnector

# Fetch data from Bank of Korea
bok = BOKConnector()  # Uses API key from environment
base_rate = bok.get_base_rate('20200101', '20241231')

# Initialize merger and create research dataset
merger = KoreanMacroDataMerger()
merger.load_data('base_rate.csv', 'base_rate', source='bok')
merger.load_data('exchange_rate.csv', 'usd_krw', source='bok')

# Create merged dataset with automatic integrity checking
monthly_data = merger.create_research_dataset(freq='M')
merger.save_merged_data('output.csv')  # Automatic validation

print("✅ Data merged and validated successfully!")
```

## 📊 Supported Data Sources

### Bank of Korea (BOK) - 863+ Economic Statistics
- Base rates, exchange rates, money supply
- CPI, GDP, trade statistics
- Housing and real estate indices

### KOSIS - Korean Statistical Information Service
- Employment and labor statistics
- Population and demographics
- Regional economic indicators

### KB Land - Real Estate Market Data
- Housing price indices (apartments, houses)
- Jeonse (전세) price indices
- Monthly rent indices
- Transaction volumes
- Market sentiment indicators

### FRED - Global Economic Indicators
- US Federal Reserve rates
- Treasury yields, VIX
- Commodity prices (oil, gold)
- Global GDP and trade data

## 🔧 Core Functionality

### Data Merging with Integrity Validation

```python
from kor_macro import KoreanMacroDataMerger

merger = KoreanMacroDataMerger()

# Load multiple data sources
merger.load_data('bok_rates.csv', 'rates', source='bok')
merger.load_data('kb_housing.xlsx', 'housing', source='kb')
merger.load_data('fred_indicators.csv', 'global', source='fred')

# Merge with automatic integrity checking
merged = merger.create_research_dataset(
    freq='M',  # Monthly aggregation
    start_date='2020-01-01',
    end_date='2024-12-31'
)

# Save with validation (default behavior)
result = merger.save_merged_data('research_data.csv')
if result:
    print("✅ All integrity checks passed")
```

### Time-Based Aggregation

```python
# Aggregate daily data to different frequencies
daily_df = merger.load_data('daily_prices.csv', 'prices')

weekly = merger.aggregate_time_series(daily_df, freq='W', agg_func='mean')
monthly = merger.aggregate_time_series(daily_df, freq='M', agg_func='mean')
quarterly = merger.aggregate_time_series(daily_df, freq='Q', 
                                        agg_func={'price': 'mean', 'volume': 'sum'})
```

### Data Integrity Validation

```python
from kor_macro.validation import DataIntegrityChecker

checker = DataIntegrityChecker()
checker.check_merge_integrity('merged_data.csv')

# Validation checks:
# ✅ No temporal shifts (dates not moved)
# ✅ Correct value-to-date mapping
# ✅ Proper frequency conversion
# ✅ Complete date series
# ✅ Monotonic date ordering
```

## 📈 Real-World Example

Complete workflow for Korean real estate analysis:

```python
from kor_macro import KoreanMacroDataMerger
import pandas as pd

# Initialize merger
merger = KoreanMacroDataMerger()

# Load economic indicators
merger.load_data('bok_base_rate.csv', 'base_rate', source='bok')
merger.load_data('kb_jeonse_index.xlsx', 'jeonse', source='kb')
merger.load_data('fred_fed_rate.csv', 'fed_rate', source='fred')

# Create research dataset
data = merger.create_research_dataset(freq='M', 
                                     start_date='2015-01-01',
                                     end_date='2024-12-31')

# Calculate correlations
correlations = data[['value_base_rate', 'value_jeonse', 'value_fed_rate']].corr()
print(f"Jeonse-Base Rate Correlation: {correlations.loc['value_jeonse', 'value_base_rate']:.3f}")

# Add derived features
data['rate_spread'] = data['value_base_rate'] - data['value_fed_rate']
data['jeonse_yoy'] = data['value_jeonse'].pct_change(12) * 100

# Export for statistical analysis
data.to_stata('korean_real_estate.dta')  # For Stata
data.to_csv('korean_real_estate.csv')    # For R/Python
```

## 🔑 Configuration

Create `.env` file with your API keys:

```bash
# Required API Keys
BOK_API_KEY=your_bok_api_key        # Bank of Korea
KOSIS_API_KEY=your_kosis_api_key    # KOSIS
FRED_API_KEY=your_fred_api_key      # FRED

# Optional
SEOUL_API_KEY=your_seoul_api_key    # Seoul Open Data
EIA_API_KEY=your_eia_api_key        # US Energy Information
```

Get API keys from:
- BOK: https://ecos.bok.or.kr/api/
- KOSIS: https://kosis.kr/openapi/
- FRED: https://fred.stlouisfed.org/docs/api/

## 📚 Documentation

- [API Documentation](https://github.com/yourusername/kor-macro-data/blob/main/API_DOCUMENTATION.md)
- [Data Source Catalog](https://github.com/yourusername/kor-macro-data/blob/main/DATA_CATALOG.md)
- [Usage Examples](https://github.com/yourusername/kor-macro-data/blob/main/examples/)
- [Contributing Guide](https://github.com/yourusername/kor-macro-data/blob/main/CONTRIBUTING.md)

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=kor_macro tests/

# Run specific test
pytest tests/test_merger.py
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas where we need help:
- Additional data source connectors
- Visualization modules
- Machine learning integration
- Documentation translations
- Performance optimizations

## 📊 Performance

- **Data Collection**: ~30 seconds for all sources
- **Monthly Aggregation**: ~1-2 seconds for 10 years of daily data
- **Merging 10+ Datasets**: ~3-5 seconds
- **Integrity Validation**: <1 second for standard datasets

## 🔄 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

- **v1.0.0** (2024-08-19): Initial release with full feature set
- **v0.9.0** (2024-08-15): Beta release
- **v0.8.0** (2024-08-10): Alpha release

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bank of Korea for ECOS API access
- KOSIS for statistical data access
- KB Land for real estate market data
- Federal Reserve for FRED API

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/kor-macro-data/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/kor-macro-data/discussions)
- **Email**: support@kor-macro-data.org

## 📈 Project Status

![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/kor-macro-data)
![GitHub issues](https://img.shields.io/github/issues/yourusername/kor-macro-data)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/kor-macro-data)
![GitHub stars](https://img.shields.io/github/stars/yourusername/kor-macro-data?style=social)

## Citation

If you use this package in your research, please cite:

```bibtex
@software{kor_macro_data,
  title = {Korean Macro Data: A Python Package for Korean Economic Data},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/yourusername/kor-macro-data},
  version = {1.0.0}
}
```

---

**Made with ❤️ for the Korean economic research community**