# Global Economic Data Sources for Academic Research

## Overview
This package provides access to official global economic data from major international organizations, suitable for academic research with proper citations.

## ✅ Configured Data Sources

### 1. FRED (Federal Reserve Economic Data)
**Status**: ✅ Fully Operational  
**API Key**: Configured  
**URL**: https://api.stlouisfed.org/fred/

**Available Data**:
- **GDP**: US, China, Japan, Eurozone, UK, Korea
- **Interest Rates**: Federal Funds Rate, ECB rates, BoJ rates, 10-year Treasury yields
- **Inflation**: CPI, PCE, Core inflation measures
- **Employment**: Unemployment rates, labor force participation
- **Exchange Rates**: Major currency pairs

**Example Series IDs**:
- `GDP` - US GDP (Nominal)
- `GDPC1` - US Real GDP
- `NYGDPMKTPCDWLD` - China GDP
- `JPNNGDP` - Japan GDP
- `EUNGDP` - Eurozone GDP
- `DFF` - Federal Funds Rate
- `CPIAUCSL` - US Consumer Price Index

### 2. World Bank API
**Status**: ✅ Fully Operational  
**API Key**: Not required  
**URL**: https://api.worldbank.org/v2/

**Available Indicators**:
- `NY.GDP.MKTP.CD` - GDP (current US$)
- `NY.GDP.MKTP.KD.ZG` - GDP growth (annual %)
- `NY.GDP.PCAP.CD` - GDP per capita
- `FP.CPI.TOTL.ZG` - Inflation, consumer prices
- `SL.UEM.TOTL.ZS` - Unemployment rate
- `SP.POP.TOTL` - Population, total
- `NE.EXP.GNFS.CD` - Exports of goods and services
- `NE.IMP.GNFS.CD` - Imports of goods and services

**Country Codes**:
- `USA` - United States
- `CHN` - China
- `JPN` - Japan
- `EMU` - Euro area
- `DEU` - Germany
- `GBR` - United Kingdom
- `KOR` - Korea, Rep.

### 3. IMF (International Monetary Fund)
**Status**: ✅ Operational  
**API Key**: Not required  
**URL**: https://www.imf.org/external/datamapper/api/v1/

**Available Datasets**:
- World Economic Outlook (WEO)
- International Financial Statistics (IFS)
- Balance of Payments (BOP)
- Government Finance Statistics (GFS)

### 4. OECD Statistics
**Status**: ✅ Operational  
**API Key**: Not required (basic access)  
**URL**: https://stats.oecd.org/

**Available Data**:
- National Accounts (GDP, GNI)
- Labour Market Statistics
- Price Indices
- International Trade
- Productivity Statistics

### 5. ECB (European Central Bank)
**Status**: ✅ Operational  
**API Key**: Not required  
**URL**: https://data-api.ecb.europa.eu/

**Available Data**:
- Eurozone GDP and economic indicators
- Interest rates and monetary policy
- Exchange rates
- Inflation statistics

### 6. EIA (US Energy Information Administration)
**Status**: ✅ API Key Configured  
**API Key**: Configured  
**URL**: https://api.eia.gov/

**Available Data**:
- Energy prices (oil, gas, electricity)
- Energy production and consumption
- Renewable energy statistics
- Carbon emissions data

## Usage Examples

### Fetching GDP Data for Multiple Countries

```python
from connectors.global_data import FREDConnector, WorldBankConnector

# Using FRED (recommended for quick access)
fred = FREDConnector()

# Get US GDP
us_gdp = fred.fetch_data('GDP', '2020-01-01', '2024-12-31')

# Get GDP for multiple countries
gdp_data = fred.get_gdp_data(['us', 'china', 'japan', 'eurozone'], '2020-01-01')

# Using World Bank (for detailed country data)
wb = WorldBankConnector()

# Get GDP data for specific countries
gdp = wb.fetch_data(
    'NY.GDP.MKTP.CD',  # GDP indicator
    ['USA', 'CHN', 'JPN', 'EMU'],  # Countries
    2020,  # Start year
    2024   # End year
)
```

### Fetching Interest Rates

```python
from connectors.global_data import FREDConnector

fred = FREDConnector()

# Federal Funds Rate
fed_rate = fred.fetch_data('DFF', '2020-01-01')

# ECB Deposit Rate
ecb_rate = fred.fetch_data('ECBDFR', '2020-01-01')

# 10-Year Treasury Yield
treasury_10y = fred.fetch_data('DGS10', '2020-01-01')
```

### Fetching Inflation Data

```python
# US Consumer Price Index
us_cpi = fred.fetch_data('CPIAUCSL', '2020-01-01')

# Eurozone Inflation
euro_cpi = fred.fetch_data('CP0000EZ19M086NEST', '2020-01-01')
```

## Data for Academic Research

### Recommended Sources by Topic

**GDP and Economic Growth**:
- Primary: FRED (most comprehensive, real-time updates)
- Secondary: World Bank (annual data, all countries)
- For detailed analysis: OECD (quarterly national accounts)

**Monetary Policy**:
- Primary: FRED (central bank rates, monetary aggregates)
- For Eurozone: ECB API
- For emerging markets: IMF IFS

**Inflation**:
- Primary: FRED (CPI, PCE, core inflation)
- For international comparison: World Bank, OECD

**Trade Statistics**:
- Primary: World Bank (exports, imports, trade balance)
- Detailed: OECD (by product category)

**Labor Markets**:
- Primary: FRED (unemployment, participation rates)
- International: OECD Labour Statistics

## Citation Guidelines

When using data from these sources in academic research:

### FRED Data
```
Federal Reserve Bank of St. Louis, [Series Name], retrieved from FRED, 
Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/[SERIES_ID], [Date].
```

### World Bank Data
```
World Bank. [Year]. [Indicator Name]. World Development Indicators. 
Washington, DC: The World Bank. Retrieved [Date] from https://data.worldbank.org
```

### IMF Data
```
International Monetary Fund. [Year]. [Dataset Name]. 
Retrieved [Date] from https://www.imf.org/en/Data
```

### OECD Data
```
OECD ([Year]), "[Dataset Name]", OECD Statistics, 
https://doi.org/[DOI] (accessed on [Date]).
```

### ECB Data
```
European Central Bank Statistical Data Warehouse. [Series Name]. 
Retrieved [Date] from https://sdw.ecb.europa.eu
```

## Data Update Frequencies

- **FRED**: Real-time to daily updates (varies by series)
- **World Bank**: Annual updates for most indicators
- **IMF**: Quarterly/Annual (WEO updated twice yearly)
- **OECD**: Monthly/Quarterly for most series
- **ECB**: Daily to monthly updates

## Available Time Periods

- **US GDP**: 1947 - Present (FRED)
- **China GDP**: 1960 - Present (World Bank)
- **Japan GDP**: 1960 - Present (World Bank)
- **Eurozone GDP**: 1995 - Present (ECB/FRED)
- **Historical data**: Some series available from 1900s

## File Output

Data can be exported to:
- CSV format for Excel/R/Stata
- JSON format for programmatic access
- Pandas DataFrames for Python analysis

## Notes for Researchers

1. **Data Consistency**: When comparing across countries, ensure you're using the same metric (nominal vs. real, local currency vs. USD)

2. **Seasonal Adjustment**: Check if data is seasonally adjusted (SA) or not seasonally adjusted (NSA)

3. **Revision Policy**: Economic data is often revised. Always note the vintage date of your data

4. **Missing Data**: Some countries/periods may have incomplete data. Always check coverage before analysis

5. **Real-time vs. Revised**: FRED provides both real-time and revised data for many series

## Support

For API documentation:
- FRED: https://fred.stlouisfed.org/docs/api/fred/
- World Bank: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
- IMF: https://www.imf.org/en/Data
- OECD: https://data.oecd.org/api/
- ECB: https://sdw.ecb.europa.eu/