# Korean Macro Data Package - API Documentation

## 🚨 CRITICAL UPDATES - Connector Standardization

**All connectors have been updated to resolve critical inconsistencies:**

### ✅ Fixed Issues
1. **DataFrame Return Format**: All methods now return `pandas.DataFrame` objects instead of dictionaries
2. **Standardized Parameters**: All methods use `start_date`/`end_date` (YYYY-MM-DD format) instead of mixed formats
3. **Consistent Structure**: All DataFrames have standardized columns: `['date', 'value', ...]`
4. **Error Handling**: Proper fallback to empty DataFrames on errors
5. **Analysis-Ready**: Direct compatibility with plotting and statistical analysis

### 🔧 Before vs After

**OLD FORMAT (Dictionary)**:
```python
result = bok.get_base_rate('20200101', '20241231')
# Returns: {'success': True, 'dataset_id': '722Y001', 'data': [...]}
# Required manual DataFrame conversion
```

**NEW FORMAT (DataFrame)**:
```python
df = bok.get_base_rate('2020-01-01', '2024-12-31')
# Returns: pandas.DataFrame with columns ['date', 'value', 'unit', 'item']
# Direct analysis: df.plot(x='date', y='value')
```

---

## Table of Contents
1. [Core Classes](#core-classes)
2. [Data Connectors](#data-connectors)
3. [Data Integrity](#data-integrity)
4. [Utility Functions](#utility-functions)
5. [Configuration](#configuration)
6. [Examples](#examples)

---

## Core Classes

### `KoreanMacroDataMerger`

Main class for merging and aggregating Korean macroeconomic data.

```python
from kor_macro import KoreanMacroDataMerger

merger = KoreanMacroDataMerger(data_dir='./data')
```

#### Methods

##### `__init__(data_dir: Union[str, Path] = None)`
Initialize the data merger.

**Parameters:**
- `data_dir` (str, Path, optional): Directory containing data files. Defaults to current directory.

---

##### `load_data(filepath: str, name: str, source: str = 'auto') -> pd.DataFrame`
Load data from a file and standardize column names.

**Parameters:**
- `filepath` (str): Path to the data file
- `name` (str): Identifier for this dataset
- `source` (str): Data source type ('bok', 'kosis', 'fred', 'kb', 'auto')

**Returns:**
- `pd.DataFrame`: Loaded and standardized dataframe

**Example:**
```python
df = merger.load_data('bok_base_rate.csv', 'base_rate', source='bok')
```

---

##### `create_research_dataset(freq: str = 'M', start_date: str = None, end_date: str = None) -> pd.DataFrame`
Create a merged research dataset with specified frequency.

**Parameters:**
- `freq` (str): Frequency for aggregation ('D', 'W', 'M', 'Q', 'Y')
- `start_date` (str): Start date in 'YYYY-MM-DD' format
- `end_date` (str): End date in 'YYYY-MM-DD' format

**Returns:**
- `pd.DataFrame`: Merged dataset with all loaded data

**Example:**
```python
monthly_data = merger.create_research_dataset(
    freq='M',
    start_date='2020-01-01',
    end_date='2024-12-31'
)
```

---

##### `save_merged_data(filepath: str, format: str = 'csv', run_integrity_check: bool = True) -> Optional[bool]`
Save merged data with automatic integrity checking.

**Parameters:**
- `filepath` (str): Output file path
- `format` (str): Output format ('csv', 'excel', 'parquet')
- `run_integrity_check` (bool): Whether to run integrity check (default: True)

**Returns:**
- `bool`: True if integrity check passed, False if issues found, None if skipped

**Example:**
```python
result = merger.save_merged_data('output.csv', run_integrity_check=True)
if result:
    print("Data validated successfully")
```

---

##### `aggregate_time_series(df: pd.DataFrame, freq: str, agg_func: Union[str, dict] = 'mean') -> pd.DataFrame`
Aggregate time series data to specified frequency.

**Parameters:**
- `df` (pd.DataFrame): Input dataframe with datetime index
- `freq` (str): Target frequency ('D', 'W', 'M', 'Q', 'Y')
- `agg_func` (str, dict): Aggregation function or dict of column-specific functions

**Returns:**
- `pd.DataFrame`: Aggregated dataframe

**Example:**
```python
weekly = merger.aggregate_time_series(daily_df, freq='W', agg_func='mean')

# Custom aggregation
quarterly = merger.aggregate_time_series(
    daily_df, 
    freq='Q',
    agg_func={'price': 'mean', 'volume': 'sum'}
)
```

---

## Data Connectors

### `BOKConnector`

Bank of Korea ECOS API connector.

```python
from kor_macro.connectors import BOKConnector

bok = BOKConnector(api_key='YOUR_API_KEY')
```

#### Methods

##### `fetch_data(dataset_id: str, start_date: str = '2020-01-01', end_date: str = None, period: str = 'M', **params) -> pd.DataFrame`
Fetch data from BOK ECOS API.

**Parameters:**
- `dataset_id` (str): Statistics code (e.g., '722Y001' for base rate)
- `start_date` (str): Start date in 'YYYY-MM-DD' format (default: '2020-01-01')
- `end_date` (str): End date in 'YYYY-MM-DD' format (default: current date)
- `period` (str): Period type ('D': Daily, 'M': Monthly, 'Q': Quarterly, 'Y': Yearly)

**Returns:**
- `pd.DataFrame`: DataFrame with standardized columns: 'date', 'value', and optional 'unit', 'item'

**Example:**
```python
data = bok.fetch_data('722Y001', '2024-01-01', '2024-12-31', 'M')
print(data.head())
#         date  value unit       item
# 0 2024-01-01   3.50    %  Base Rate
# 1 2024-02-01   3.25    %  Base Rate
```

---

##### `get_base_rate(start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame`
Fetch BOK base rate data.

**Parameters:**
- `start_date` (str): Start date in 'YYYY-MM-DD' format
- `end_date` (str): End date in 'YYYY-MM-DD' format

**Returns:**
- `pd.DataFrame`: Base rate data with standardized columns

**Example:**
```python
base_rate = bok.get_base_rate('2024-01-01', '2024-12-31')
print(f"Latest rate: {base_rate.iloc[-1]['value']:.2f}%")
```

---

##### `get_exchange_rate(currency: str, start_date: str, end_date: str) -> pd.DataFrame`
Fetch exchange rate data.

**Parameters:**
- `currency` (str): Currency code ('USD', 'EUR', 'JPY', 'CNY')
- `start_date` (str): Start date in 'YYYYMMDD' format
- `end_date` (str): End date in 'YYYYMMDD' format

**Returns:**
- `pd.DataFrame`: Exchange rate data

---

##### `get_statistics_list() -> pd.DataFrame`
Get list of all available BOK statistics.

**Returns:**
- `pd.DataFrame`: Available statistics with codes and descriptions

---

### `KBLandConnector`

KB Land real estate data connector for Korean housing market data.

```python
from kor_macro.connectors import KBLandConnector

kb = KBLandConnector()
```

#### Methods

##### `get_housing_index(house_type='apartment', region='서울', period=None, start_date=None, end_date=None) -> pd.DataFrame`
Get housing price index data.

**Parameters:**
- `house_type` (str): Type of housing ('apartment', 'house', 'officetel')
- `region` (str): Region name in Korean (e.g., '서울', '부산', '강남구')
- `period` (str, optional): Specific period (e.g., '2024-01')
- `start_date` (str, optional): Start date in 'YYYY-MM-DD' format
- `end_date` (str, optional): End date in 'YYYY-MM-DD' format

**Returns:**
- `pd.DataFrame`: Housing price index with columns: date, region, price_index, mom_change, yoy_change

##### `get_jeonse_index(region='서울', start_date=None, end_date=None) -> pd.DataFrame`
Get Jeonse (전세) price index data.

**Returns:**
- `pd.DataFrame`: Jeonse price index data

##### `get_rent_index(region='서울', start_date=None, end_date=None) -> pd.DataFrame`
Get monthly rent index data.

**Returns:**
- `pd.DataFrame`: Monthly rent index data

##### `get_market_trend(region='서울', start_date=None, end_date=None) -> pd.DataFrame`
Get market trend indicators (supply/demand balance).

**Returns:**
- `pd.DataFrame`: Market trend data with supply_demand and transaction_volume

##### `get_price_outlook(region='서울', start_date=None, end_date=None) -> pd.DataFrame`
Get price outlook/sentiment index.

**Returns:**
- `pd.DataFrame`: Price outlook data with outlook_index and sentiment

##### `get_regional_comparison(house_type='apartment', regions=None, date=None) -> pd.DataFrame`
Compare housing indices across multiple regions.

**Parameters:**
- `house_type` (str): Type of housing
- `regions` (List[str]): List of regions to compare
- `date` (str): Specific date for comparison

**Returns:**
- `pd.DataFrame`: Regional comparison data

**Example:**
```python
# Get Seoul apartment prices
kb = KBLandConnector()
apt_prices = kb.get_housing_index(
    house_type='apartment',
    region='서울',
    start_date='2023-01-01',
    end_date='2024-12-31'
)

# Get Jeonse prices
jeonse = kb.get_jeonse_index('서울')

# Get market sentiment
market = kb.get_market_trend('서울')
print(f"Market: {market.iloc[-1]['supply_demand']}")

# Regional comparison
comparison = kb.get_regional_comparison(
    regions=['서울', '부산', '대구']
)
```

---

### `KOSISConnector`

Korean Statistical Information Service connector.

```python
from kor_macro.connectors import KOSISConnector

kosis = KOSISConnector(api_key='YOUR_API_KEY')
```

#### Methods

##### `fetch_data(table_id: str, start_date: str = '2020-01-01', end_date: str = None, **params) -> pd.DataFrame`
Fetch data from KOSIS API.

**Parameters:**
- `table_id` (str): KOSIS table ID (e.g., 'DT_1B040A3')
- `start_date` (str): Start date in 'YYYY-MM-DD' format
- `end_date` (str): End date in 'YYYY-MM-DD' format

**Returns:**
- `pd.DataFrame`: DataFrame with standardized columns: 'date', 'value', and optional 'item', 'category', 'unit'

**Example:**
```python
data = kosis.fetch_data('DT_1B040A3', '2020-01-01', '2024-12-31')
print(data.head())
#         date      value           item  category    unit
# 0 2020-01-01   51600000  Total Population  National  Persons
# 1 2021-01-01   51700000  Total Population  National  Persons
```

---

### `KBLandEnhancedConnector`

KB Land real estate data connector with Excel support.

```python
from kor_macro.connectors import KBLandEnhancedConnector

kb = KBLandEnhancedConnector()
```

#### Methods

##### `download_dataset(dataset_type: str, save_dir: str = './data') -> Tuple[bool, str]`
Download KB Land dataset as Excel file.

**Parameters:**
- `dataset_type` (str): Type of dataset ('price_index', 'jeonse_index', 'monthly_rent', 'transaction_volume', 'market_sentiment')
- `save_dir` (str): Directory to save downloaded file

**Returns:**
- `Tuple[bool, str]`: Success status and file path

---

### `EIAConnector`

U.S. Energy Information Administration data connector for energy market data.

```python
from kor_macro.connectors import EIAConnector

eia = EIAConnector()
```

#### Methods

##### `get_wti_crude_price(start_date: str = '2010-01-01', end_date: str = None) -> pd.DataFrame`
Get WTI crude oil spot prices.

**Returns:**
- `pd.DataFrame`: Daily WTI prices with date and value columns

##### `get_brent_crude_price(start_date: str = '2010-01-01', end_date: str = None) -> pd.DataFrame`
Get Brent crude oil spot prices.

**Returns:**
- `pd.DataFrame`: Daily Brent prices with date and value columns

##### `get_henry_hub_gas_price(start_date: str = '2010-01-01', end_date: str = None) -> pd.DataFrame`
Get Henry Hub natural gas spot prices.

**Returns:**
- `pd.DataFrame`: Daily natural gas prices with date and value columns

##### `get_us_gasoline_price(start_date: str = '2010-01-01', end_date: str = None) -> pd.DataFrame`
Get US regular gasoline retail prices.

**Returns:**
- `pd.DataFrame`: Weekly gasoline prices with date and value columns

##### `get_korea_energy_data(data_type: str = 'petroleum_consumption', start_date: str = '2010-01-01', end_date: str = None) -> pd.DataFrame`
Get Korea energy consumption and generation data.

**Parameters:**
- `data_type` (str): Type of data ('petroleum_consumption' or 'electricity_generation')
- `start_date` (str): Start date in 'YYYY-MM-DD' format
- `end_date` (str): End date in 'YYYY-MM-DD' format

**Returns:**
- `pd.DataFrame`: Annual Korea energy data

##### `get_crude_oil_inventories(start_date: str = '2010-01-01', end_date: str = None) -> pd.DataFrame`
Get US crude oil inventory levels.

**Returns:**
- `pd.DataFrame`: Weekly inventory data with date and value columns

##### `get_renewable_generation(start_date: str = '2010-01-01', end_date: str = None) -> pd.DataFrame`
Get US renewable electricity generation data.

**Returns:**
- `pd.DataFrame`: Monthly renewable generation data

**Example:**
```python
# Get WTI crude prices
wti = eia.get_wti_crude_price('2023-01-01', '2024-01-01')

# Get Korea petroleum consumption
korea_oil = eia.get_korea_energy_data('petroleum_consumption', '2015-01-01')

# Get US gasoline prices
gas_prices = eia.get_us_gasoline_price('2023-01-01')
```

---

### `FREDConnector`

Federal Reserve Economic Data connector.

```python
from kor_macro.connectors import FREDConnector

fred = FREDConnector(api_key='YOUR_API_KEY')
```

#### Methods

##### `fetch_data(series_id: str, start_date: str, end_date: str) -> pd.DataFrame`
Fetch FRED time series data.

**Parameters:**
- `series_id` (str): FRED series ID (e.g., 'DFF' for Fed Funds Rate)
- `start_date` (str): Start date in 'YYYY-MM-DD' format
- `end_date` (str): End date in 'YYYY-MM-DD' format

**Returns:**
- `pd.DataFrame`: FRED data

**Common Series IDs:**
- `DFF`: Federal Funds Rate
- `DGS10`: 10-Year Treasury Rate
- `VIXCLS`: VIX Volatility Index
- `DCOILWTICO`: WTI Oil Price
- `DEXKOUS`: KRW/USD Exchange Rate

---

## Data Integrity

### `DataIntegrityChecker`

Validates temporal alignment and data quality.

```python
from kor_macro.validation import DataIntegrityChecker

checker = DataIntegrityChecker()
```

#### Methods

##### `check_merge_integrity(merged_file: str) -> None`
Run comprehensive integrity check on merged dataset.

**Parameters:**
- `merged_file` (str): Path to merged CSV file

**Example:**
```python
checker.check_merge_integrity('korean_macro_complete.csv')

# Check results
if checker.issues:
    print(f"Found {len(checker.issues)} issues")
else:
    print("All checks passed")
```

---

##### `check_date_alignment(original_file: str, merged_df: pd.DataFrame, source_name: str) -> None`
Check if dates are properly aligned between original and merged data.

**Parameters:**
- `original_file` (str): Path to original data file
- `merged_df` (pd.DataFrame): Merged dataframe
- `source_name` (str): Name of the data source

---

## Utility Functions

### `quick_merge_korean_data`

One-line function to merge multiple data sources.

```python
from kor_macro import quick_merge_korean_data

merged = quick_merge_korean_data(
    bok_files=['base_rate.csv', 'exchange.csv'],
    kb_files=['housing.xlsx'],
    fred_files=['fed_rate.csv'],
    kosis_files=['employment.csv'],
    frequency='M',
    output_file='merged.csv'
)
```

**Parameters:**
- `bok_files` (list): List of BOK data files
- `kb_files` (list): List of KB Land Excel files
- `fred_files` (list): List of FRED data files
- `kosis_files` (list): List of KOSIS data files
- `frequency` (str): Aggregation frequency ('D', 'W', 'M', 'Q', 'Y')
- `output_file` (str): Output file path

**Returns:**
- `pd.DataFrame`: Merged dataframe

---

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Bank of Korea
BOK_API_KEY=your_bok_api_key

# KOSIS
KOSIS_API_KEY=your_kosis_api_key

# Seoul Open Data
SEOUL_API_KEY=your_seoul_api_key

# FRED
FRED_API_KEY=your_fred_api_key

# Optional
EIA_API_KEY=your_eia_api_key
WORLD_BANK_API_KEY=your_world_bank_key
```

### Column Mappings

Access and modify column name mappings:

```python
from kor_macro import KoreanMacroDataMerger

merger = KoreanMacroDataMerger()

# View current mappings
print(merger.COLUMN_MAPPINGS)

# Add custom mappings
merger.COLUMN_MAPPINGS.update({
    '사용자정의': 'custom_field',
    '새로운열': 'new_column'
})
```

---

## Examples

### Complete Workflow Example

```python
from kor_macro import KoreanMacroDataMerger
from kor_macro.connectors import BOKConnector, FREDConnector
import pandas as pd

# 1. Initialize connectors
bok = BOKConnector()
fred = FREDConnector()

# 2. Fetch fresh data
base_rate = bok.get_base_rate('20200101', '20241231')
fed_rate = fred.fetch_data('DFF', '2020-01-01', '2024-12-31')

# 3. Save fetched data
base_rate.to_csv('base_rate.csv', index=False)
fed_rate.to_csv('fed_rate.csv', index=False)

# 4. Initialize merger
merger = KoreanMacroDataMerger()

# 5. Load data
merger.load_data('base_rate.csv', 'base_rate', source='bok')
merger.load_data('fed_rate.csv', 'fed_rate', source='fred')

# 6. Create merged dataset
merged = merger.create_research_dataset(
    freq='M',
    start_date='2020-01-01',
    end_date='2024-12-31'
)

# 7. Add derived features
merged['rate_spread'] = merged['value_base_rate'] - merged['value_fed_rate']

# 8. Save with integrity check
result = merger.save_merged_data('analysis_data.csv')

if result:
    print("✅ Data successfully merged and validated")
    
    # 9. Analyze correlations
    correlation = merged[['value_base_rate', 'value_fed_rate']].corr()
    print(f"Correlation: {correlation.iloc[0, 1]:.3f}")
```

### Handling Different Frequencies

```python
# Daily to Monthly
daily_df = pd.read_csv('daily_prices.csv')
monthly = merger.aggregate_time_series(daily_df, freq='M', agg_func='mean')

# Quarterly data with forward fill
quarterly_df = pd.read_csv('gdp_quarterly.csv')
monthly_filled = merger.aggregate_time_series(
    quarterly_df, 
    freq='M',
    agg_func='ffill'  # Forward fill for quarterly data
)

# Mixed aggregation
mixed = merger.aggregate_time_series(
    daily_df,
    freq='W',
    agg_func={
        'price': 'mean',
        'volume': 'sum',
        'high': 'max',
        'low': 'min'
    }
)
```

### Error Handling

```python
from kor_macro import KoreanMacroDataMerger
from kor_macro.exceptions import DataIntegrityError, MergeError

merger = KoreanMacroDataMerger()

try:
    # Load and merge data
    merger.load_data('data.csv', 'test', source='bok')
    merged = merger.create_research_dataset()
    
    # Save with integrity check
    result = merger.save_merged_data('output.csv')
    
    if result is False:
        raise DataIntegrityError("Integrity check failed")
        
except FileNotFoundError as e:
    print(f"File not found: {e}")
except DataIntegrityError as e:
    print(f"Data integrity issue: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Custom Data Sources

```python
# Add custom data source
class CustomConnector(BaseConnector):
    def fetch_data(self, params):
        # Custom implementation
        return pd.DataFrame(data)

# Use with merger
custom = CustomConnector()
data = custom.fetch_data({'param': 'value'})
data.to_csv('custom_data.csv')

merger.load_data('custom_data.csv', 'custom', source='auto')
```

---

## Performance Tips

1. **Use Parquet for large datasets**
   ```python
   merger.save_merged_data('large_data.parquet', format='parquet')
   ```

2. **Disable integrity check for performance**
   ```python
   merger.save_merged_data('data.csv', run_integrity_check=False)
   ```

3. **Cache API responses**
   ```python
   import functools
   
   @functools.lru_cache(maxsize=100)
   def cached_fetch(series_id, start, end):
       return fred.fetch_data(series_id, start, end)
   ```

4. **Use chunking for very large files**
   ```python
   for chunk in pd.read_csv('huge_file.csv', chunksize=10000):
       process(chunk)
   ```

---

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure `.env` file exists and contains valid keys
   - Check environment variable names match exactly

2. **Date Format Issues**
   - BOK uses 'YYYYMMDD'
   - FRED uses 'YYYY-MM-DD'
   - KOSIS uses 'YYYYMM'

3. **Memory Issues with Large Datasets**
   - Use `dtype` optimization
   - Process in chunks
   - Use Parquet format

4. **Integrity Check Failures**
   - Review `data_integrity_report.txt`
   - Check for date shifts
   - Verify frequency conversions

---

## Support

For additional help:
- GitHub Issues: https://github.com/yourusername/kor-macro-data/issues
- Documentation: https://kor-macro-data.readthedocs.io
- Examples: See `/examples` directory in the repository