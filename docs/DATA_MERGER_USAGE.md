# Data Merger Module - Complete Usage Guide

## Overview
The Data Merger module provides powerful functionality to merge and aggregate Korean macroeconomic data with standardized English column names and flexible time-based aggregation.

## Key Features
- **English Column Names**: All data columns standardized to English
- **Time-Based Aggregation**: Daily, Weekly, Monthly, Quarterly, Yearly
- **Multi-Source Support**: BOK, KOSIS, KB Land, FRED, World Bank
- **Automatic Date Alignment**: Smart merging across different frequencies
- **Derived Features**: Automatic calculation of percentage changes, YoY growth

## Installation

```python
from data_merger import KoreanMacroDataMerger, quick_merge_korean_data
```

## Basic Usage

### 1. Initialize the Merger

```python
merger = KoreanMacroDataMerger()
```

### 2. Load Data Files

```python
# Load BOK data
merger.load_data('bok_data_final/bok_base_rate.csv', 'base_rate', source='bok')
merger.load_data('bok_data_final/bok_usd_krw_exchange_rate.csv', 'usd_krw', source='bok')

# Load KB Land data (Excel files)
merger.load_data('data_exports/kb_land/KB주택가격지수_20250819.xlsx', 'housing_price', source='kb')
merger.load_data('data_exports/kb_land/KB전세가격지수_20250819.xlsx', 'jeonse_price', source='kb')

# Load FRED data
merger.load_data('research_data_fixed/fred_us_federal_funds_rate.csv', 'fed_rate', source='fred')
merger.load_data('research_data_fixed/fred_vix_index.csv', 'vix', source='fred')

# Load KOSIS data
merger.load_data('research_data_fixed/kosis_DT_1DA7001.csv', 'employment', source='kosis')
```

### 3. Create Merged Research Dataset

```python
# Monthly aggregation (recommended for most analysis)
monthly_data = merger.create_research_dataset(
    freq='M',  # 'D', 'W', 'M', 'Q', 'Y'
    start_date='2010-01-01',
    end_date='2024-12-31'
)

# Save the merged data
merger.save_merged_data('korean_macro_monthly.csv', format='csv')
merger.save_merged_data('korean_macro_monthly.xlsx', format='excel')
```

## Column Name Mappings

### BOK Columns
| Original | English |
|----------|---------|
| STAT_CODE | stat_code |
| STAT_NAME | stat_name |
| DATA_VALUE | value |
| TIME | date |
| UNIT_NAME | unit |

### KB Land Columns
| Korean | English |
|--------|---------|
| 날짜/시점 | date |
| 지역 | region |
| 종합 | total_index |
| 아파트 | apartment_index |
| 서울 | seoul |
| 강남 | gangnam |
| 전세 | jeonse_price |
| 매매 | sale_price |
| 거래량 | transaction_volume |
| 심리지수 | sentiment_index |

### KOSIS Columns
| Original | English |
|----------|---------|
| PRD_DE | date |
| C1_NM | region |
| C2_NM | category |
| DT | value |

## Time Aggregation Examples

### Daily to Monthly
```python
# Aggregate daily exchange rates to monthly averages
monthly_rates = merger.aggregate_time_series(
    df=exchange_rate_df,
    freq='M',
    agg_func='mean',  # or 'sum', 'min', 'max', 'last'
    value_col='value',
    date_col='date'
)
```

### Custom Aggregation
```python
# Different aggregation for different columns
custom_agg = merger.aggregate_time_series(
    df=data,
    freq='Q',
    agg_func={
        'price': 'mean',      # Average prices
        'volume': 'sum',      # Total volume
        'high': 'max',        # Maximum high
        'low': 'min'          # Minimum low
    }
)
```

## Quick Merge Function

For simple merging tasks:

```python
merged = quick_merge_korean_data(
    bok_files=['bok_data/base_rate.csv', 'bok_data/exchange_rate.csv'],
    kb_files=['kb_data/housing_price.xlsx', 'kb_data/jeonse_price.xlsx'],
    fred_files=['fred_data/fed_rate.csv', 'fred_data/vix.csv'],
    kosis_files=['kosis_data/employment.csv'],
    frequency='M',  # Monthly aggregation
    output_file='merged_korean_macro.csv'
)
```

## Saving Data with Automatic Integrity Checking

The merger automatically validates data integrity when saving:

```python
# Save with automatic integrity check (default behavior)
integrity_result = merger.save_merged_data(
    'korean_macro_data.csv',
    format='csv',
    run_integrity_check=True  # Default is True
)

# Check the result
if integrity_result is True:
    print("✅ Data validated - no date shifts or misalignments")
elif integrity_result is False:
    print("⚠️ Integrity issues detected - check data_integrity_report.txt")
else:
    print("ℹ️ Integrity check skipped")

# Save without integrity check (faster for large datasets)
merger.save_merged_data('large_dataset.csv', run_integrity_check=False)

# Save in other formats (integrity check only for CSV)
merger.save_merged_data('data.xlsx', format='excel')  # No check for Excel
merger.save_merged_data('data.parquet', format='parquet')  # No check for Parquet
```

The integrity checker validates:
- ✅ No temporal shifts (dates not moved forward/backward)
- ✅ Correct value-to-date mapping
- ✅ Proper frequency conversion
- ✅ Complete date series
- ✅ Monotonic date ordering

## Advanced Features

### 1. Derived Features
The merger automatically adds useful derived features:

```python
merged_data = merger.create_research_dataset(freq='M')

# Automatically includes:
# - year, quarter, month, week columns
# - day_of_week (0=Monday, 6=Sunday)
# - is_quarter_end, is_month_end flags
# - pct_change (period-over-period % change)
# - pct_change_yoy (year-over-year % change)
```

### 2. Data Summary
```python
# Get overview of all loaded datasets
summary = merger.get_data_summary()
print(summary)

# Output:
#         dataset  rows  columns           date_range  numeric_columns  missing_values
# 0     base_rate  5478       14  2010-01-01 to 2024-12-31             9               0
# 1  housing_price   180       25  2010-01-01 to 2024-12-31            20               5
```

### 3. Merge Options
```python
# Inner join (only matching dates)
inner_merged = merger.merge_datasets(
    datasets={'base_rate': df1, 'housing': df2},
    on='date',
    how='inner'
)

# Left join (keep all dates from first dataset)
left_merged = merger.merge_datasets(
    datasets=merger.datasets,
    on='date',
    how='left'
)
```

## Real-World Example: Korean Real Estate Analysis

```python
# Complete workflow for real estate market analysis
merger = KoreanMacroDataMerger()

# 1. Load all relevant data
datasets = {
    'bok_base_rate.csv': 'base_rate',
    'bok_usd_krw_exchange_rate.csv': 'usd_krw',
    'KB주택가격지수.xlsx': 'housing_price',
    'KB전세가격지수.xlsx': 'jeonse_price',
    'fred_us_federal_funds_rate.csv': 'fed_rate',
    'fred_vix_index.csv': 'vix',
    'kosis_employment.csv': 'employment'
}

for file, name in datasets.items():
    source = 'bok' if 'bok' in file else 'kb' if 'KB' in file else 'fred' if 'fred' in file else 'kosis'
    merger.load_data(file, name, source=source)

# 2. Create monthly dataset for econometric analysis
monthly = merger.create_research_dataset(
    freq='M',
    start_date='2010-01-01',
    end_date='2024-12-31'
)

# 3. Calculate correlations
correlations = monthly[['value_base_rate', 'value_housing_price', 
                       'value_jeonse_price', 'value_fed_rate']].corr()

# 4. Export for statistical software
merger.save_merged_data('real_estate_analysis.csv', format='csv')
merger.save_merged_data('real_estate_analysis.xlsx', format='excel')
merger.save_merged_data('real_estate_analysis.parquet', format='parquet')

print(f"Dataset ready: {monthly.shape[0]} observations, {monthly.shape[1]} variables")
```

## Output Format

The merged dataset includes:
- **date**: Standardized date column
- **value_{dataset_name}**: Value columns from each dataset
- **source_{dataset_name}**: Boolean flags indicating data availability
- **frequency**: Aggregation frequency indicator
- **Derived features**: Year, quarter, month, percentage changes
- **Metadata columns**: Units, categories, regions (where applicable)

## Tips for Best Results

1. **Date Alignment**: The merger automatically aligns dates across different frequencies
2. **Missing Data**: Use `how='inner'` for complete cases only, `how='outer'` to keep all dates
3. **Aggregation**: Choose appropriate aggregation functions (mean for rates, sum for volumes)
4. **Memory**: For large datasets, process in chunks or use specific date ranges
5. **Excel Files**: Ensure openpyxl is installed for Excel file support

## Common Issues and Solutions

### Issue: Date parsing errors
```python
# Solution: Specify date format explicitly
df = pd.read_csv('file.csv', parse_dates=['date'], 
                 date_parser=lambda x: pd.to_datetime(x, format='%Y%m%d'))
merger.datasets['name'] = merger.standardize_columns(df)
```

### Issue: Memory errors with large datasets
```python
# Solution: Load and process in chunks
for year in range(2010, 2025):
    data = merger.create_research_dataset(
        freq='M',
        start_date=f'{year}-01-01',
        end_date=f'{year}-12-31'
    )
    data.to_csv(f'merged_{year}.csv')
```

### Issue: Different column names in Excel files
```python
# Solution: Add custom mappings
merger.COLUMN_MAPPINGS.update({
    'Your Column': 'english_name',
    '사용자정의': 'custom_field'
})
```

## Performance Considerations

- Monthly aggregation: ~1-2 seconds for 10 years of daily data
- Merging 10 datasets: ~3-5 seconds
- Excel file loading: Slower than CSV, use CSV when possible
- Parquet format: Fastest for large datasets, maintains data types

## Integration with Statistical Software

### Export for R
```python
monthly_data.to_csv('korean_macro.csv', index=False)
# In R: data <- read.csv('korean_macro.csv')
```

### Export for Stata
```python
# Requires pyreadstat package
monthly_data.to_stata('korean_macro.dta')
```

### Export for MATLAB
```python
# Save as CSV or use scipy.io.savemat
from scipy.io import savemat
savemat('korean_macro.mat', {'data': monthly_data.values, 
                             'columns': monthly_data.columns.tolist()})
```

## Support

For issues or questions, please refer to the main package documentation or create an issue in the repository.