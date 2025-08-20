# Korean Macro Data - Quick Start Guide

Get up and running with Korean Macro Data in 5 minutes! This guide provides practical, task-focused examples.

## Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Quick Start by Use Case](#quick-start-by-use-case)
3. [Common Research Workflows](#common-research-workflows)
4. [Code Recipes](#code-recipes)

---

## Installation & Setup

### 1. Install the Package

```bash
# From PyPI (when published)
pip install kor-macro-data

# From GitHub (current)
pip install git+https://github.com/NanyeonK/kor-macro-data.git

# For development
git clone https://github.com/NanyeonK/kor-macro-data.git
cd kor-macro-data
pip install -e .
```

### 2. Get Your API Keys

You'll need API keys for most data sources. Here's how to get them:

#### Bank of Korea (BOK) - **Required**
1. Visit: https://ecos.bok.or.kr/api/
2. Click "API 신청" (API Application)
3. Register with email
4. API key sent instantly to email
5. **Free**, 100,000 requests/day limit

#### KOSIS - **Required**
1. Visit: https://kosis.kr/openapi/
2. Click "인증키 신청"
3. Register and verify email
4. Get key from "마이페이지"
5. **Free**, 10,000 requests/day

#### FRED - **Recommended**
1. Visit: https://fred.stlouisfed.org/docs/api/api_key.html
2. Click "Request API Key"
3. Create account
4. Key displayed immediately
5. **Free**, 120 requests/minute

#### EIA - **Optional**
1. Visit: https://www.eia.gov/opendata/
2. Click "Register"
3. Instant key via email
4. **Free**, works without key (limited)

### 3. Configure Environment

Create a `.env` file in your project root:

```bash
# Required
BOK_API_KEY=your_bok_key_here
KOSIS_API_KEY=your_kosis_key_here

# Recommended
FRED_API_KEY=your_fred_key_here

# Optional
EIA_API_KEY=your_eia_key_here
SEOUL_API_KEY=your_seoul_key_here
```

### 4. Verify Installation

```python
from kor_macro.connectors import BOKConnector

# Test connection
bok = BOKConnector()
if bok.test_connection():
    print("✅ Successfully connected to BOK!")
else:
    print("❌ Connection failed - check your API key")
```

---

## Quick Start by Use Case

### 📈 "I want Korean housing market data"

```python
from kor_macro.connectors import KBLandConnector, BOKConnector
from kor_macro import KoreanMacroDataMerger
import pandas as pd

# Get housing price indices
kb = KBLandConnector()

# Get Seoul apartment prices (weekly)
seoul_apt = kb.get_housing_index(
    house_type='apartment',
    region='서울',
    period='2023-01'
)

# Get Jeonse prices
jeonse = kb.get_jeonse_index(
    region='서울',
    start_date='2020-01',
    end_date='2024-12'
)

# Get BOK interest rates for comparison
bok = BOKConnector()
base_rate = bok.get_base_rate('2020-01-01', '2024-12-31')

# Merge and analyze
merger = KoreanMacroDataMerger()
merger.load_dataframe(seoul_apt, 'seoul_apt_prices')
merger.load_dataframe(jeonse, 'jeonse_prices') 
merger.load_dataframe(base_rate, 'base_rate')

# Create monthly dataset
monthly_data = merger.create_research_dataset(freq='M')

# Calculate correlations
correlation = monthly_data[['value_jeonse_prices', 'value_base_rate']].corr()
print(f"Jeonse-Interest Rate Correlation: {correlation.iloc[0,1]:.3f}")

# Export for analysis
monthly_data.to_csv('korean_housing_analysis.csv')
print("✅ Data saved to korean_housing_analysis.csv")
```

### 💰 "I want to analyze monetary policy impact"

```python
from kor_macro.connectors import BOKConnector, FREDConnector
import matplotlib.pyplot as plt

# Get Korean monetary data
bok = BOKConnector()
kr_rate = bok.get_base_rate('2015-01-01', '2024-12-31')
kr_m2 = bok.get_money_supply('M2', '2015-01-01', '2024-12-31')
kr_cpi = bok.get_cpi('2015-01-01', '2024-12-31')

# Get US Fed data for comparison
fred = FREDConnector()
us_rate = fred.fetch_data('DFF', '2015-01-01', '2024-12-31')
us_m2 = fred.fetch_data('M2SL', '2015-01-01', '2024-12-31')

# Merge data
merger = KoreanMacroDataMerger()
merger.load_dataframe(kr_rate, 'kr_rate')
merger.load_dataframe(kr_m2, 'kr_m2')
merger.load_dataframe(kr_cpi, 'kr_cpi')
merger.load_dataframe(us_rate, 'us_rate')

# Create quarterly data for analysis
quarterly = merger.create_research_dataset(freq='Q')

# Calculate year-over-year changes
quarterly['kr_m2_yoy'] = quarterly['value_kr_m2'].pct_change(4) * 100
quarterly['kr_cpi_yoy'] = quarterly['value_kr_cpi'].pct_change(4) * 100

# Visualize
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Interest rates
axes[0].plot(quarterly.index, quarterly['value_kr_rate'], label='BOK Base Rate')
axes[0].plot(quarterly.index, quarterly['value_us_rate'], label='Fed Funds Rate')
axes[0].set_ylabel('Interest Rate (%)')
axes[0].legend()
axes[0].set_title('Korea vs US Monetary Policy')

# Inflation vs Money Supply
axes[1].plot(quarterly.index, quarterly['kr_cpi_yoy'], label='CPI YoY')
axes[1].plot(quarterly.index, quarterly['kr_m2_yoy'], label='M2 YoY', alpha=0.7)
axes[1].set_ylabel('YoY Change (%)')
axes[1].legend()
axes[1].set_title('Korean Inflation vs Money Supply Growth')

plt.tight_layout()
plt.savefig('monetary_policy_analysis.png')
print("✅ Analysis saved to monetary_policy_analysis.png")
```

### 🌏 "I want to compare Korea with other economies"

```python
from kor_macro.connectors import (
    BOKConnector, FREDConnector, 
    WorldBankConnector, IMFConnector
)

# Get GDP data for major economies
wb = WorldBankConnector()
gdp_data = wb.fetch_data(
    indicator='NY.GDP.MKTP.KD.ZG',  # GDP growth rate
    countries=['KOR', 'USA', 'CHN', 'JPN', 'DEU'],
    start_year=2010,
    end_year=2024
)

# Get unemployment rates
unemployment = wb.fetch_data(
    indicator='SL.UEM.TOTL.ZS',
    countries=['KOR', 'USA', 'CHN', 'JPN', 'DEU'],
    start_year=2010
)

# Get inflation data from IMF
imf = IMFConnector()
inflation = imf.fetch_data(
    indicator='PCPIPCH',
    countries=['KOR', 'USA', 'CHN', 'JPN', 'DEU']
)

# Create comparison DataFrame
comparison = pd.DataFrame({
    'Country': ['Korea', 'USA', 'China', 'Japan', 'Germany'],
    'GDP_Growth_2023': [1.4, 2.5, 5.2, 1.9, -0.3],
    'Unemployment_2023': [2.7, 3.7, 5.2, 2.6, 3.0],
    'Inflation_2023': [3.6, 4.1, 0.2, 3.3, 6.0]
})

print("\n2023 Economic Comparison:")
print(comparison.to_string(index=False))

# Get detailed Korea data
bok = BOKConnector()
korea_detail = bok.get_economic_statistics(
    stat_codes=['200Y001', '901Y009', '301Y013'],  # GDP, CPI, Trade
    start_date='2020-01-01'
)

print("\n✅ Detailed Korea data loaded for deep analysis")
```

### ⚡ "I want energy market data"

```python
from kor_macro.connectors import EIAConnector
import pandas as pd

eia = EIAConnector()

# Get oil prices
wti = eia.get_wti_crude_price('2022-01-01', '2024-12-31')
brent = eia.get_brent_crude_price('2022-01-01', '2024-12-31')

# Get Korea energy consumption
korea_oil = eia.get_korea_energy_data(
    data_type='petroleum_consumption',
    start_date='2015-01-01'
)

# Get US gasoline prices
gas_prices = eia.get_us_gasoline_price('2022-01-01')

# Analyze oil price spread
oil_spread = pd.merge(
    wti.rename(columns={'value': 'WTI'}),
    brent.rename(columns={'value': 'Brent'}),
    on='date'
)
oil_spread['spread'] = oil_spread['Brent'] - oil_spread['WTI']

print(f"Average WTI-Brent Spread: ${oil_spread['spread'].mean():.2f}")
print(f"Current WTI Price: ${wti.iloc[-1]['value']:.2f}")
print(f"Current Brent Price: ${brent.iloc[-1]['value']:.2f}")
```

---

## Common Research Workflows

### 1. Economic Event Study

Analyze impact of policy changes or economic events:

```python
from kor_macro import KoreanMacroDataMerger
from datetime import datetime
import numpy as np

# Define event date (e.g., BOK rate hike)
event_date = '2022-07-13'

# Load relevant data
merger = KoreanMacroDataMerger()

# ... load your data ...

# Create daily dataset
daily_data = merger.create_research_dataset(freq='D')

# Calculate pre/post event windows
event_idx = daily_data.index.get_loc(event_date)
pre_window = daily_data.iloc[event_idx-30:event_idx]  # 30 days before
post_window = daily_data.iloc[event_idx:event_idx+30]  # 30 days after

# Calculate abnormal returns or changes
for col in daily_data.columns:
    if 'value_' in col:
        pre_mean = pre_window[col].mean()
        post_mean = post_window[col].mean()
        change = ((post_mean - pre_mean) / pre_mean) * 100
        print(f"{col}: {change:.2f}% change")
```

### 2. Correlation Analysis

Find relationships between variables:

```python
# Load and merge your data
merger = KoreanMacroDataMerger()
# ... load multiple datasets ...

# Create monthly dataset
monthly = merger.create_research_dataset(freq='M')

# Calculate rolling correlations
window = 12  # 12-month rolling window

correlations = {}
base_series = 'value_base_rate'

for col in monthly.columns:
    if 'value_' in col and col != base_series:
        rolling_corr = monthly[base_series].rolling(window).corr(monthly[col])
        correlations[col] = rolling_corr

# Find strongest correlations
corr_summary = pd.DataFrame(correlations).mean()
print("\nAverage Correlations with Base Rate:")
print(corr_summary.sort_values(ascending=False).head(10))
```

### 3. Time Series Forecasting

Prepare data for forecasting models:

```python
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.seasonal import seasonal_decompose

# Prepare data
monthly = merger.create_research_dataset(freq='M')
target = monthly['value_housing_price'].dropna()

# Decompose time series
decomposition = seasonal_decompose(target, model='multiplicative', period=12)

# Create lagged features
lags = [1, 3, 6, 12]
features = pd.DataFrame()

for lag in lags:
    features[f'lag_{lag}'] = target.shift(lag)

# Add other economic indicators as features
features['base_rate'] = monthly['value_base_rate']
features['m2_growth'] = monthly['value_m2'].pct_change(12)
features['cpi'] = monthly['value_cpi']

# Remove NaN values
features = features.dropna()
target_aligned = target.loc[features.index]

# Scale features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

print(f"✅ Prepared {len(features)} samples with {features.shape[1]} features")
```

---

## Code Recipes

### Recipe 1: Automated Data Collection

```python
import schedule
import time
from datetime import datetime

def collect_daily_data():
    """Collect all daily data automatically"""
    
    print(f"[{datetime.now()}] Starting daily data collection...")
    
    # BOK data
    bok = BOKConnector()
    bok_data = {
        'base_rate': bok.get_base_rate(),
        'exchange_rate': bok.get_exchange_rate('USD'),
        'kospi': bok.get_stock_index('KOSPI')
    }
    
    # Save to dated file
    date_str = datetime.now().strftime('%Y%m%d')
    
    for name, df in bok_data.items():
        df.to_csv(f'data/daily/{date_str}_{name}.csv')
    
    print(f"✅ Daily data collection complete")

# Schedule daily collection
schedule.every().day.at("09:00").do(collect_daily_data)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

### Recipe 2: Data Quality Validation

```python
from kor_macro.validation import DataIntegrityChecker

def validate_research_data(filepath):
    """Comprehensive data validation"""
    
    checker = DataIntegrityChecker()
    
    # Run all checks
    checks = {
        'Date Continuity': checker.check_date_continuity(filepath),
        'Outliers': checker.check_outliers(filepath),
        'Missing Values': checker.check_missing_values(filepath),
        'Temporal Alignment': checker.check_temporal_alignment(filepath)
    }
    
    # Generate report
    print("\n📊 Data Quality Report")
    print("=" * 50)
    
    for check, result in checks.items():
        status = "✅ PASS" if result['passed'] else "❌ FAIL"
        print(f"{check}: {status}")
        if not result['passed']:
            print(f"  Issues: {result['issues']}")
    
    return all(r['passed'] for r in checks.values())

# Usage
if validate_research_data('merged_data.csv'):
    print("\n✅ Data ready for analysis!")
else:
    print("\n⚠️ Data quality issues detected")
```

### Recipe 3: Multi-Source Merge

```python
def create_comprehensive_dataset():
    """Merge all available data sources"""
    
    merger = KoreanMacroDataMerger()
    
    # Define data sources
    sources = {
        'bok': ['base_rate', 'exchange_rate', 'money_supply'],
        'kosis': ['employment', 'population'],
        'kb': ['housing_price', 'jeonse_price'],
        'fred': ['fed_rate', 'us_gdp'],
        'eia': ['wti_price', 'gas_price']
    }
    
    # Collect data
    print("Collecting data from all sources...")
    
    for source, indicators in sources.items():
        connector = get_connector(source)  # Helper function
        for indicator in indicators:
            try:
                data = fetch_indicator_data(connector, indicator)
                merger.load_dataframe(data, f"{source}_{indicator}")
                print(f"  ✅ Loaded {source}_{indicator}")
            except Exception as e:
                print(f"  ❌ Failed {source}_{indicator}: {e}")
    
    # Create merged dataset
    merged = merger.create_research_dataset(
        freq='M',
        start_date='2015-01-01',
        end_date='2024-12-31'
    )
    
    # Save with validation
    result = merger.save_merged_data(
        'comprehensive_korean_macro.csv',
        run_integrity_check=True
    )
    
    if result:
        print(f"\n✅ Successfully created comprehensive dataset")
        print(f"Shape: {merged.shape}")
        print(f"Date Range: {merged.index.min()} to {merged.index.max()}")
        print(f"Variables: {', '.join([c for c in merged.columns if 'value_' in c])}")
    
    return merged

# Run
dataset = create_comprehensive_dataset()
```

### Recipe 4: Export for Statistical Software

```python
def export_for_analysis(data, base_filename='korean_macro'):
    """Export data for R, Stata, MATLAB, etc."""
    
    # For R
    data.to_csv(f'{base_filename}.csv', index=True)
    print(f"✅ Saved {base_filename}.csv for R")
    
    # For Stata (requires statsmodels)
    try:
        import statsmodels.api as sm
        # Convert datetime index to Stata date format
        data_stata = data.copy()
        data_stata['date'] = data_stata.index
        data_stata.to_stata(f'{base_filename}.dta', 
                           write_index=False,
                           convert_dates={'date': 'td'})
        print(f"✅ Saved {base_filename}.dta for Stata")
    except ImportError:
        print("  Install statsmodels for Stata export")
    
    # For MATLAB
    import scipy.io
    # Convert to dict of arrays
    mat_data = {col: data[col].values for col in data.columns}
    mat_data['dates'] = data.index.astype(str).values
    scipy.io.savemat(f'{base_filename}.mat', mat_data)
    print(f"✅ Saved {base_filename}.mat for MATLAB")
    
    # For Excel with multiple sheets
    with pd.ExcelWriter(f'{base_filename}.xlsx') as writer:
        # Main data
        data.to_excel(writer, sheet_name='Data')
        
        # Metadata
        metadata = pd.DataFrame({
            'Variable': data.columns,
            'Type': data.dtypes,
            'Non_Missing': data.count(),
            'Mean': data.mean(),
            'Std': data.std(),
            'Min': data.min(),
            'Max': data.max()
        })
        metadata.to_excel(writer, sheet_name='Metadata')
        
        # Correlation matrix
        corr = data.corr()
        corr.to_excel(writer, sheet_name='Correlations')
    
    print(f"✅ Saved {base_filename}.xlsx with metadata")

# Usage
export_for_analysis(monthly_data, 'korea_housing_study')
```

---

## Next Steps

1. **Explore the Full API**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. **Browse Available Data**: See [DATA_CATALOG.md](DATA_CATALOG.md)
3. **Advanced Examples**: See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
4. **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Quick Tips

- 🔑 **API Keys**: Store in `.env` file, never commit to git
- ⏱️ **Rate Limits**: Add delays between requests if needed
- 📊 **Data Quality**: Always run integrity checks after merging
- 💾 **Caching**: Save frequently used data locally
- 🔄 **Updates**: Check for package updates regularly

## Need Help?

- **Issues**: [GitHub Issues](https://github.com/NanyeonK/kor-macro-data/issues)
- **Examples**: Check the `examples/` directory
- **API Docs**: [Full documentation](API_DOCUMENTATION.md)

---

**Happy researching! 🚀**