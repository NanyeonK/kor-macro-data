# API Usage Examples - Complete Guide

## 🇰🇷 Korean Data APIs

### 1. Bank of Korea (BOK) - Economic Statistics

#### Basic Usage
```python
from connectors import BOKConnector

# Initialize connector
bok = BOKConnector()

# List all available datasets
datasets = bok.list_datasets()
for ds in datasets:
    print(f"{ds['name']}: {ds['id']}")
```

#### Example 1: Get Korean Base Rate
```python
# Fetch base rate data
base_rate = bok.get_base_rate('20200101', '20241231')

# Access the data
if base_rate['success']:
    for record in base_rate['data']:
        print(f"{record['TIME']}: {record['DATA_VALUE']}%")

# Output:
# 2020.01: 1.25%
# 2020.03: 0.75%
# 2020.05: 0.50%
# ...
```

#### Example 2: Get Exchange Rates
```python
# USD/KRW exchange rate
exchange_rate = bok.fetch_data('731Y001', '20230101', '20241231', 'D')

# Convert to pandas DataFrame
import pandas as pd
df = pd.DataFrame(exchange_rate['data'])
df['DATA_VALUE'] = pd.to_numeric(df['DATA_VALUE'])
print(df[['TIME', 'DATA_VALUE']].tail())
```

#### Example 3: Get Housing Price Index
```python
# Housing price index (monthly)
housing = bok.get_housing_price_index('20200101', '20241231')

if housing['success']:
    df = pd.DataFrame(housing['data'])
    # Calculate year-over-year change
    df['DATA_VALUE'] = pd.to_numeric(df['DATA_VALUE'])
    df['YoY_Change'] = df['DATA_VALUE'].pct_change(12) * 100
    print(df[['TIME', 'DATA_VALUE', 'YoY_Change']].tail())
```

### 2. KOSIS - Korean Statistics

#### Basic Usage
```python
from connectors import KOSISConnector

kosis = KOSISConnector()

# List available datasets
datasets = kosis.list_datasets()
```

#### Example 1: Population Statistics
```python
# Get population data
population = kosis.get_population_stats('202301', '202412')

if population['success']:
    df = pd.DataFrame(population['data'])
    print(f"Total records: {len(df)}")
    
    # Group by region
    by_region = df.groupby('C1_NM')['DT'].sum()
    print(by_region.head())
```

#### Example 2: Real Estate Transactions
```python
# Real estate transaction statistics
real_estate = kosis.fetch_data('DT_1YL2101', '202301', '202312')

if real_estate['success']:
    df = pd.DataFrame(real_estate['data'])
    # Filter for Seoul
    seoul_data = df[df['C1_NM'].str.contains('Seoul', na=False)]
    print(f"Seoul transactions: {len(seoul_data)}")
```

#### Example 3: Employment Data
```python
# Employment rate by age group
employment = kosis.fetch_data('DT_1DA7001S', '202301', '202412')

if employment['success']:
    df = pd.DataFrame(employment['data'])
    # Latest employment rate
    latest = df.sort_values('PRD_DE').tail(1)
    print(f"Latest employment rate: {latest['DT'].values[0]}%")
```

### 3. Seoul Open Data Plaza

#### Basic Usage
```python
from connectors import SeoulDataConnector

seoul = SeoulDataConnector()

# List available datasets
datasets = seoul.list_datasets()
```

#### Example 1: Real-time Air Quality
```python
# Get air quality for all 25 districts
air_quality = seoul.get_air_quality(1, 25)

if air_quality['success']:
    df = pd.DataFrame(air_quality['data'])
    
    # Find districts with best/worst air quality
    df['PM25'] = pd.to_numeric(df['PM25'])
    best = df.nsmallest(5, 'PM25')[['MSRSTE_NM', 'PM25']]
    worst = df.nlargest(5, 'PM25')[['MSRSTE_NM', 'PM25']]
    
    print("Best Air Quality Districts:")
    print(best)
    print("\nWorst Air Quality Districts:")
    print(worst)
```

#### Example 2: Real Estate Prices
```python
# Get real estate transaction prices
real_estate = seoul.get_real_estate_prices('2024', '01', '', 1, 100)

if real_estate['success']:
    df = pd.DataFrame(real_estate['data'])
    
    # Average price by district
    avg_price = df.groupby('SGG_NM')['OBJ_AMT'].mean()
    print("Average prices by district:")
    print(avg_price.sort_values(ascending=False).head())
```

#### Example 3: Apartment Rent Prices
```python
# Get apartment rent data
rent = seoul.get_apartment_rent('2024', '01', 1, 100)

if rent['success']:
    df = pd.DataFrame(rent['data'])
    # Analyze rent trends
    print(f"Total rent transactions: {len(df)}")
```

### 4. KB Land - Real Estate Data

#### Basic Usage
```python
from connectors.kbland_enhanced import KBLandEnhancedConnector

kb = KBLandEnhancedConnector()

# Get catalog of available data
catalog = kb.get_catalog()
print(catalog)
```

#### Example 1: Download Housing Price Index
```python
# Download KB housing price index
success, filepath = kb.download_dataset('price_index')

if success:
    print(f"Downloaded: {filepath}")
    
    # Read the Excel file
    df = pd.read_excel(filepath)
    print(df.head())
```

#### Example 2: Get All KB Land Data
```python
# Download all available datasets
results = kb.download_all_datasets()

print(f"Total datasets: {results['total']}")
print(f"Successful downloads: {results['successful']}")

# Access individual results
for dataset_id, result in results['results'].items():
    if result['success']:
        print(f"{result['dataset']}: {result['result']}")
```

#### Example 3: Search by Region
```python
# Initialize with Selenium for dynamic content
kb = KBLandEnhancedConnector()
kb.init_driver()

# Search for Seoul data
seoul_data = kb.search_by_region('seoul')

for item in seoul_data:
    print(f"{item['name']}: {item['data_count']} records")

kb.close_driver()
```

## 🌍 Global Data APIs

### 5. FRED - Federal Reserve Economic Data

#### Basic Usage
```python
from connectors.global_data import FREDConnector

fred = FREDConnector()

# List available datasets
datasets = fred.list_datasets()
```

#### Example 1: US GDP Data
```python
# Get US GDP (quarterly)
us_gdp = fred.fetch_data('GDP', '2020-01-01', '2024-12-31')

if us_gdp['success']:
    df = pd.DataFrame(us_gdp['data'])
    df['value'] = pd.to_numeric(df['value'])
    
    # Calculate quarter-over-quarter growth
    df['QoQ_Growth'] = df['value'].pct_change() * 100
    print(df[['date', 'value', 'QoQ_Growth']].tail())

# Output:
# date        value    QoQ_Growth
# 2024-01-01  28846.664  0.35
# 2024-04-01  29019.178  0.60
# 2024-07-01  29397.961  1.30
# 2024-10-01  29723.864  1.11
```

#### Example 2: Multiple Country GDP Comparison
```python
# Get GDP for multiple countries
gdp_comparison = fred.get_gdp_data(
    countries=['us', 'china', 'japan', 'eurozone'],
    start_date='2020-01-01'
)

# Pivot for comparison
pivot = gdp_comparison.pivot(index='date', columns='country', values='value')
print(pivot.tail())

# Calculate growth rates
for country in pivot.columns:
    pivot[f'{country}_growth'] = pivot[country].pct_change(4) * 100  # YoY
```

#### Example 3: Interest Rates and Inflation
```python
# Federal Funds Rate
fed_rate = fred.fetch_data('DFF', '2020-01-01')

# US CPI (inflation)
cpi = fred.fetch_data('CPIAUCSL', '2020-01-01')

# 10-Year Treasury Yield
treasury_10y = fred.fetch_data('DGS10', '2020-01-01')

# Combine into single DataFrame
data = {
    'fed_rate': pd.DataFrame(fed_rate['data']),
    'cpi': pd.DataFrame(cpi['data']),
    'treasury_10y': pd.DataFrame(treasury_10y['data'])
}

# Merge on date
combined = pd.merge(data['fed_rate'], data['cpi'], on='date')
combined = pd.merge(combined, data['treasury_10y'], on='date')
```

### 6. World Bank API

#### Basic Usage
```python
from connectors.global_data import WorldBankConnector

wb = WorldBankConnector()
```

#### Example 1: GDP for Multiple Countries
```python
# Get GDP data for major economies
gdp_data = wb.fetch_data(
    indicator='NY.GDP.MKTP.CD',  # GDP in current US$
    countries=['USA', 'CHN', 'JPN', 'DEU', 'IND', 'GBR'],
    start_year=2015,
    end_year=2023
)

if gdp_data['success']:
    # Process data
    records = []
    for item in gdp_data['data']:
        if item and item['value']:
            records.append({
                'country': item['country']['value'],
                'year': item['date'],
                'gdp': item['value']
            })
    
    df = pd.DataFrame(records)
    pivot = df.pivot(index='year', columns='country', values='gdp')
    print(pivot / 1e12)  # Convert to trillions
```

#### Example 2: Economic Indicators Dashboard
```python
# Multiple indicators for one country
indicators = {
    'GDP': 'NY.GDP.MKTP.CD',
    'GDP_Growth': 'NY.GDP.MKTP.KD.ZG',
    'Inflation': 'FP.CPI.TOTL.ZG',
    'Unemployment': 'SL.UEM.TOTL.ZS',
    'Population': 'SP.POP.TOTL'
}

country = 'KOR'  # South Korea
year = 2022

dashboard = {}
for name, indicator in indicators.items():
    data = wb.fetch_data(indicator, [country], year, year)
    if data['success'] and data['data']:
        value = data['data'][0]['value'] if data['data'][0] else None
        dashboard[name] = value

print(f"Korea Economic Dashboard ({year}):")
for key, value in dashboard.items():
    print(f"  {key}: {value:,.2f}" if value else f"  {key}: N/A")
```

#### Example 3: Trade Balance Analysis
```python
# Exports and Imports
exports = wb.fetch_data('NE.EXP.GNFS.CD', ['USA', 'CHN', 'JPN'], 2020, 2023)
imports = wb.fetch_data('NE.IMP.GNFS.CD', ['USA', 'CHN', 'JPN'], 2020, 2023)

# Calculate trade balance
if exports['success'] and imports['success']:
    exp_df = pd.DataFrame(exports['data'])
    imp_df = pd.DataFrame(imports['data'])
    
    # Process and calculate balance
    # ... (data processing code)
```

### 7. IMF Data

#### Basic Usage
```python
from connectors.global_data import IMFConnector

imf = IMFConnector()
```

#### Example 1: Real GDP Growth
```python
# Get real GDP growth for G7 countries
gdp_growth = imf.fetch_data(
    'NGDP_RPCH',  # Real GDP growth
    countries=['USA', 'JPN', 'DEU', 'GBR', 'FRA', 'ITA', 'CAN']
)

if gdp_growth['success']:
    # Extract recent years
    for country, data in gdp_growth['data']['values'].items():
        recent = list(data.items())[-3:]  # Last 3 years
        print(f"{country}: {recent}")
```

#### Example 2: Government Debt Analysis
```python
# Government debt as % of GDP
debt = imf.fetch_data('GGXWDG', ['USA', 'JPN', 'CHN', 'DEU'])

if debt['success']:
    # Analyze debt trends
    for country, values in debt['data']['values'].items():
        years = sorted(values.keys())[-5:]  # Last 5 years
        print(f"\n{country} Debt/GDP ratio:")
        for year in years:
            print(f"  {year}: {values[year]}%")
```

### 8. Combining Multiple Sources

#### Example: Comprehensive Economic Analysis
```python
# Combine data from multiple sources for comprehensive analysis

# 1. Get GDP from FRED
fred = FREDConnector()
us_gdp = fred.fetch_data('GDP', '2020-01-01')

# 2. Get population from World Bank
wb = WorldBankConnector()
population = wb.fetch_data('SP.POP.TOTL', ['USA'], 2020, 2023)

# 3. Get inflation from FRED
inflation = fred.fetch_data('CPIAUCSL', '2020-01-01')

# 4. Combine all data
analysis = {
    'gdp': pd.DataFrame(us_gdp['data']),
    'inflation': pd.DataFrame(inflation['data']),
    # Process population data...
}

# Create comprehensive dashboard
dashboard = pd.merge(analysis['gdp'], analysis['inflation'], on='date')
dashboard.columns = ['date', 'gdp', 'cpi']

# Calculate real GDP
dashboard['real_gdp'] = dashboard['gdp'] / (dashboard['cpi'] / 100)

print(dashboard.tail())
```

## 📊 Data Export Examples

### Export to CSV
```python
# Export any data to CSV
df = pd.DataFrame(data)
df.to_csv('data_exports/my_data.csv', index=False, encoding='utf-8-sig')
```

### Export to Excel with Multiple Sheets
```python
# Create Excel file with multiple datasets
with pd.ExcelWriter('data_exports/economic_data.xlsx') as writer:
    gdp_df.to_excel(writer, sheet_name='GDP', index=False)
    inflation_df.to_excel(writer, sheet_name='Inflation', index=False)
    rates_df.to_excel(writer, sheet_name='Interest Rates', index=False)
```

### Create Time Series Plot
```python
import matplotlib.pyplot as plt

# Plot multiple time series
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# GDP
axes[0, 0].plot(gdp_df['date'], gdp_df['value'])
axes[0, 0].set_title('GDP')

# Inflation
axes[0, 1].plot(inflation_df['date'], inflation_df['value'])
axes[0, 1].set_title('Inflation')

# Exchange Rate
axes[1, 0].plot(exchange_df['date'], exchange_df['value'])
axes[1, 0].set_title('Exchange Rate')

# Interest Rate
axes[1, 1].plot(rate_df['date'], rate_df['value'])
axes[1, 1].set_title('Interest Rate')

plt.tight_layout()
plt.savefig('data_exports/economic_indicators.png')
```

## 🔧 Error Handling

### Basic Error Handling
```python
try:
    data = connector.fetch_data(series_id)
    if data['success']:
        # Process data
        df = pd.DataFrame(data['data'])
    else:
        print(f"Error: {data.get('message', 'Unknown error')}")
except Exception as e:
    print(f"Connection error: {e}")
```

### Retry Logic
```python
from time import sleep

max_retries = 3
for attempt in range(max_retries):
    try:
        data = connector.fetch_data(series_id)
        if data['success']:
            break
    except:
        if attempt < max_retries - 1:
            sleep(2 ** attempt)  # Exponential backoff
            continue
        else:
            raise
```

## 📝 Notes

1. **API Keys**: Ensure all required API keys are in `.env` file
2. **Rate Limits**: Most APIs have rate limits; the connectors handle this automatically
3. **Data Formats**: All data can be converted to pandas DataFrames for analysis
4. **Time Zones**: Most data uses local time zones; be aware when comparing
5. **Missing Data**: Some historical data may be incomplete; always check coverage
6. **Citations**: Remember to cite data sources in academic work