# Korean Economic & Real Estate Data API Package

A comprehensive Python package for accessing, merging, and analyzing Korean economic and real estate data from multiple government and financial sources. Features automatic data collection, English column standardization, and flexible time-based aggregation.

## 📊 Resulting Merged Data Files

The package produces three main merged datasets combining all available data sources:

| File | Size | Rows | Columns | Description |
|------|------|------|---------|-------------|
| **merged_data_monthly.csv** | 732KB | 3,965 | 82 | Monthly aggregated data (2010-2024) |
| **merged_data_quarterly.csv** | 726KB | 3,932 | 82 | Quarterly aggregated data |
| **merged_data_yearly.csv** | 724KB | 3,918 | 82 | Yearly aggregated data |

### What's Included in the Merged Data:
- **BOK Data**: Base rate, USD/KRW/EUR/CNY exchange rates
- **KB Land**: Housing price index, Jeonse index, monthly rent, transaction volume, market sentiment
- **FRED**: US Fed rate, Treasury yields, VIX, US GDP, oil prices
- **KOSIS**: Employment rates, demographic statistics
- **Derived Features**: Year-over-year changes, percentage changes, time components

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kor_macro.git
cd kor_macro

# Install dependencies with uv
uv pip install -r requirements.txt

# Or with pip
pip install -r requirements.txt
```

### Basic Usage - Data Collection

```python
from connectors import BOKConnector, KOSISConnector, SeoulDataConnector
from connectors.kbland_enhanced import KBLandEnhancedConnector
from connectors.global_data import FREDConnector

# Bank of Korea data
bok = BOKConnector()
base_rate = bok.get_base_rate('20100101', '20241231')

# KB Land real estate data  
kb = KBLandEnhancedConnector()
success, filepath = kb.download_dataset('price_index')  # Downloads Excel file

# FRED global economic data
fred = FREDConnector()
fed_rate = fred.fetch_data('DFF', '2010-01-01', '2024-12-31')
```

### Data Merging with English Columns

```python
from data_merger import KoreanMacroDataMerger

# Initialize merger
merger = KoreanMacroDataMerger()

# Load multiple data sources
merger.load_data('bok_data_final/bok_base_rate.csv', 'base_rate', source='bok')
merger.load_data('data_exports/kb_land/KB주택가격지수_20250819.xlsx', 'housing_price', source='kb')
merger.load_data('research_data_fixed/fred_us_federal_funds_rate.csv', 'fed_rate', source='fred')

# Create merged dataset with monthly aggregation
monthly_data = merger.create_research_dataset(
    freq='M',  # Options: 'D', 'W', 'M', 'Q', 'Y'
    start_date='2010-01-01',
    end_date='2024-12-31'
)

# Save in multiple formats
merger.save_merged_data('korean_macro.csv', format='csv')
merger.save_merged_data('korean_macro.xlsx', format='excel')
merger.save_merged_data('korean_macro.parquet', format='parquet')
```

## 📁 Data Sources & Available Statistics

### Bank of Korea (BOK) - 863+ Economic Statistics
```python
# Correct BOK series codes with item codes
bok_codes = {
    'Base Rate': ('722Y001', '0101000', 'D'),
    'USD/KRW Exchange': ('731Y001', '0000001', 'D'),
    'M2 Money Supply': ('101Y003', 'BBHS00', 'M'),
    'CPI': ('901Y009', '0', 'M'),
    'Housing Price Index': ('901Y062', 'P63AC', 'M'),
    'Jeonse Price Index': ('901Y063', 'P64AC', 'M'),
    'Household Credit': ('151Y001', '1000000', 'Q')
}
```

### KB Land - Real Estate Market Data
```python
kb_datasets = {
    'price_index': 'KB Housing Price Index',
    'jeonse_index': 'KB Jeonse Price Index', 
    'monthly_rent': 'Monthly Rent Index',
    'transaction_volume': 'Transaction Volume',
    'market_sentiment': 'Market Sentiment Index',
    'regional_analysis': '25 Seoul Districts + 31 Gyeonggi Cities'
}
```

### FRED - Global Economic Indicators
```python
fred_series = {
    'DFF': 'US Federal Funds Rate',
    'DGS10': 'US 10-Year Treasury',
    'VIXCLS': 'VIX Volatility Index',
    'DTWEXBGS': 'DXY Dollar Index',
    'GDP': 'US GDP',
    'DCOILWTICO': 'WTI Oil Price'
}
```

### KOSIS - Korean Statistics
```python
kosis_tables = {
    'DT_1DA7001': 'Employment Rate',
    'DT_1B8000F': 'Birth and Death Statistics',
    'DT_1YL2001': 'Apartment Price Index',
    'DT_1JC1501': 'Household Statistics'
}
```

## 🔧 Advanced Features

### Time-Based Aggregation

```python
# Aggregate daily data to different frequencies
daily_df = merger.load_data('exchange_rates.csv', 'fx', source='bok')

# Weekly average
weekly = merger.aggregate_time_series(daily_df, freq='W', agg_func='mean')

# Monthly sum
monthly = merger.aggregate_time_series(daily_df, freq='M', agg_func='sum')

# Quarterly with custom aggregation
quarterly = merger.aggregate_time_series(
    daily_df, 
    freq='Q',
    agg_func={'price': 'mean', 'volume': 'sum', 'high': 'max', 'low': 'min'}
)
```

### Column Name Standardization

All Korean and original column names are automatically converted to English:

| Original (Korean/BOK) | English |
|----------------------|---------|
| 날짜/시점 | date |
| 지역 | region |
| 아파트 | apartment_index |
| 전세 | jeonse_price |
| 매매 | sale_price |
| DATA_VALUE | value |
| STAT_CODE | stat_code |

### Quick Merge Function

```python
from data_merger import quick_merge_korean_data

# One-line merge of all data sources
merged = quick_merge_korean_data(
    bok_files=['bok_data/base_rate.csv', 'bok_data/exchange.csv'],
    kb_files=['kb_data/housing.xlsx', 'kb_data/jeonse.xlsx'],
    fred_files=['fred_data/fed_rate.csv', 'fred_data/vix.csv'],
    kosis_files=['kosis_data/employment.csv'],
    frequency='M',  # Monthly aggregation
    output_file='final_research_data.csv'
)
```

## 📈 Real-World Example: Korean Real Estate Market Analysis

```python
# Complete workflow for econometric analysis
from data_merger import KoreanMacroDataMerger
import pandas as pd

# 1. Initialize and load all data
merger = KoreanMacroDataMerger()

# Load BOK data (interest rates, exchange rates)
merger.load_data('bok_data_final/bok_base_rate.csv', 'base_rate')
merger.load_data('bok_data_final/bok_usd_krw_exchange_rate.csv', 'usd_krw')

# Load KB Land real estate data
merger.load_data('data_exports/kb_land/KB주택가격지수_20250819.xlsx', 'housing')
merger.load_data('data_exports/kb_land/KB전세가격지수_20250819.xlsx', 'jeonse')

# Load FRED global indicators
merger.load_data('research_data_fixed/fred_us_federal_funds_rate.csv', 'fed_rate')
merger.load_data('research_data_fixed/fred_vix_index.csv', 'vix')

# 2. Create research dataset with monthly frequency
research_data = merger.create_research_dataset(
    freq='M',
    start_date='2010-01-01',
    end_date='2024-12-31'
)

# 3. Analyze correlations
correlations = research_data[['value_base_rate', 'value_housing', 
                              'value_jeonse', 'value_fed_rate']].corr()
print("Correlation Matrix:")
print(correlations)

# 4. Calculate year-over-year changes
for col in ['value_housing', 'value_jeonse']:
    research_data[f'{col}_yoy'] = research_data[col].pct_change(12) * 100

# 5. Export for statistical analysis
research_data.to_stata('korean_real_estate.dta')  # For Stata
research_data.to_csv('korean_real_estate.csv')    # For R
```

## 📊 Dataset Discovery

```python
from dataset_discovery import DatasetDiscovery

discovery = DatasetDiscovery()

# Discover all available datasets
bok_stats = discovery.discover_bok_statistics()      # 863+ BOK statistics
kosis_stats = discovery.discover_kosis_statistics()  # KOSIS datasets
seoul_datasets = discovery.discover_seoul_datasets() # Seoul open data

# Search for specific topics
housing_data = discovery.search_datasets('housing')
interest_data = discovery.search_datasets('interest rate')
gdp_data = discovery.search_datasets('GDP')
```

## 📁 Project Structure

```
kor_macro/
├── connectors/                    # API connectors
│   ├── base.py                  # Base connector class
│   ├── bok.py                   # Bank of Korea connector
│   ├── kosis.py                 # KOSIS connector
│   ├── seoul.py                 # Seoul data connector
│   ├── kbland_enhanced.py       # KB Land connector with Excel download
│   └── global_data.py           # FRED, World Bank, IMF connectors
├── data_merger.py                # Data merging and aggregation module
├── merged_data_monthly.csv       # Final merged monthly data (3,965 rows × 82 cols)
├── merged_data_quarterly.csv     # Final merged quarterly data
├── merged_data_yearly.csv        # Final merged yearly data
├── bok_data_final/               # Downloaded BOK data
├── data_exports/kb_land/         # Downloaded KB Land Excel files
├── research_data_fixed/          # Downloaded FRED and KOSIS data
├── DATA_MERGER_USAGE.md         # Complete merger documentation
├── USAGE_EXAMPLES.md            # API usage examples
└── .env                         # API keys configuration
```

## 🔑 API Keys Required

Create a `.env` file with your API keys:

```bash
# Bank of Korea ECOS API
BOK_API_KEY=your_bok_api_key

# KOSIS Open API  
KOSIS_API_KEY=your_kosis_api_key

# Seoul Open Data
SEOUL_API_KEY=your_seoul_api_key

# FRED (Federal Reserve Economic Data)
FRED_API_KEY=your_fred_api_key

# EIA (US Energy Information Administration) - Optional
EIA_API_KEY=your_eia_api_key
```

## 📚 Complete Documentation

- **[DATA_MERGER_USAGE.md](DATA_MERGER_USAGE.md)** - Complete guide for data merging module
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Detailed API usage examples
- **[REPRESENTATIVE_DATA_CATALOG.md](REPRESENTATIVE_DATA_CATALOG.md)** - All available datasets
- **[GLOBAL_DATA_SOURCES.md](GLOBAL_DATA_SOURCES.md)** - Global data API documentation
- **[KB_LAND_DATA_CATALOG.md](KB_LAND_DATA_CATALOG.md)** - KB Land datasets documentation

## 🛠️ Installation Requirements

```txt
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
python-dotenv>=1.0.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
openpyxl>=3.1.0  # For Excel file support
selenium>=4.0.0  # Optional, for dynamic web content
matplotlib>=3.7.0  # Optional, for data visualization
```

## 🔍 Data Integrity Validation

The package includes a comprehensive data integrity checker that validates temporal alignment:

```python
from data_integrity_checker import DataIntegrityChecker

# Run integrity check on merged data
checker = DataIntegrityChecker()
checker.check_merge_integrity('korean_macro_complete.csv')
```

The integrity checker validates:
- ✅ No date shifts or temporal misalignments
- ✅ Correct value mapping to dates
- ✅ Proper frequency conversion (daily→monthly, quarterly→monthly)
- ✅ Complete date series without gaps
- ✅ Monotonic date ordering

## 📊 Output Data Format

The merged datasets include:
- **Date columns**: Standardized datetime format
- **Value columns**: `value_{dataset_name}` for each data source
- **Source flags**: `source_{dataset_name}` boolean indicators
- **Frequency**: Aggregation frequency indicator
- **Derived features**: Year, quarter, month, percentage changes, YoY changes
- **Metadata**: Units, categories, regions where applicable

## 🚦 Performance

- **Data collection**: ~30 seconds for all sources
- **Monthly aggregation**: ~1-2 seconds for 10 years of daily data
- **Merging 10+ datasets**: ~3-5 seconds
- **Excel loading**: ~1 second per file
- **CSV export**: <1 second for 4,000 rows

## 📈 Integration with Statistical Software

### R
```r
data <- read.csv("merged_data_monthly.csv")
```

### Stata
```stata
import delimited "merged_data_monthly.csv", clear
```

### Python (Pandas)
```python
import pandas as pd
df = pd.read_csv("merged_data_monthly.csv")
```

### MATLAB
```matlab
data = readtable('merged_data_monthly.csv');
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License

## 📧 Support

For issues or questions:
1. Check the documentation files (DATA_MERGER_USAGE.md, USAGE_EXAMPLES.md)
2. Review the example scripts (merge_example.py, test_apis.py)
3. Create an issue in the repository