# KB Land Complete Data Catalog

## Overview
KB Land (KB부동산) provides comprehensive Korean real estate market data through their data portal.

## Data Access Information
- **Main Portal**: https://data.kbland.kr
- **Format**: Excel (.xlsx), CSV, PDF
- **Update Schedule**: Monthly (last Monday), Quarterly, Weekly (varies by dataset)
- **Language**: Korean (some English headers available)

## Complete Dataset List

### Summary Table

| No | Dataset | Korean Name | Format | Frequency |
|----|---------|-------------|--------|----------|
| 1 | KB Housing Price Index | KB주택가격지수 | Excel | Monthly |
| 2 | KB Jeonse Price Index | KB전세가격지수 | Excel | Monthly |
| 3 | KB Monthly Rent Index | KB월세가격지수 | Excel | Monthly |
| 4 | Real Estate Transaction Volume | 부동산거래량 | Excel/CSV | Monthly |
| 5 | Market Sentiment Index | 시장심리지수 | Excel | Monthly |
| 6 | Regional Market Analysis | 지역별 시장분석 | Excel | Monthly |
| 7 | Apartment Complex Rankings | 아파트 단지 순위 | CSV | Weekly |
| 8 | Office & Retail Market | 오피스/상가 시장 | Excel | Quarterly |
| 9 | Land Price Index | 토지가격지수 | Excel | Quarterly |
| 10 | Policy Impact Analysis | 정책영향분석 | PDF/Excel | As needed |

## Detailed Dataset Descriptions

### 1. KB Housing Price Index (KB주택가격지수)

- **Dataset ID**: `price_index`
- **URL**: https://data.kbland.kr/kbstats/wmh
- **Format**: Excel
- **Update Frequency**: Monthly
- **Data Contents**:
  - Apartment price index (아파트)
  - House price index (단독주택)
  - Row house price index (연립주택)
  - National composite index (전국종합)

### 2. KB Jeonse Price Index (KB전세가격지수)

- **Dataset ID**: `jeonse_index`
- **URL**: https://data.kbland.kr/kbstats/wjs
- **Format**: Excel
- **Update Frequency**: Monthly
- **Data Contents**:
  - Jeonse price index (전세가격지수)
  - Jeonse ratio (전세가율)
  - Regional jeonse trends

### 3. KB Monthly Rent Index (KB월세가격지수)

- **Dataset ID**: `monthly_rent`
- **URL**: https://data.kbland.kr/kbstats/wmr
- **Format**: Excel
- **Update Frequency**: Monthly
- **Data Contents**:
  - Monthly rent index
  - Deposit conversion rate
  - Regional rent trends

### 4. Real Estate Transaction Volume (부동산거래량)

- **Dataset ID**: `transaction_volume`
- **URL**: https://data.kbland.kr/kbstats/wmt
- **Format**: Excel/CSV
- **Update Frequency**: Monthly
- **Data Contents**:
  - Transaction count by region
  - Transaction volume by type
  - YoY comparison

### 5. Market Sentiment Index (시장심리지수)

- **Dataset ID**: `market_sentiment`
- **URL**: https://data.kbland.kr/kbstats/wms
- **Format**: Excel
- **Update Frequency**: Monthly
- **Data Contents**:
  - Consumer sentiment
  - Expert outlook
  - Price expectation

### 6. Regional Market Analysis (지역별 시장분석)

- **Dataset ID**: `regional_analysis`
- **URL**: https://data.kbland.kr/kbstats/wra
- **Format**: Excel
- **Update Frequency**: Monthly
- **Data Contents**:
  - Seoul 25 districts
  - Gyeonggi 31 cities
  - Metropolitan cities
  - Price rankings

### 7. Apartment Complex Rankings (아파트 단지 순위)

- **Dataset ID**: `apartment_ranking`
- **URL**: https://data.kbland.kr/kbstats/war
- **Format**: CSV
- **Update Frequency**: Weekly
- **Data Contents**:
  - Top 100 by price
  - Top gainers/losers
  - Transaction leaders

### 8. Office & Retail Market (오피스/상가 시장)

- **Dataset ID**: `office_retail`
- **URL**: https://data.kbland.kr/kbstats/wor
- **Format**: Excel
- **Update Frequency**: Quarterly
- **Data Contents**:
  - Office rent index
  - Retail space prices
  - Vacancy rates

### 9. Land Price Index (토지가격지수)

- **Dataset ID**: `land_price`
- **URL**: https://data.kbland.kr/kbstats/wlp
- **Format**: Excel
- **Update Frequency**: Quarterly
- **Data Contents**:
  - Residential land
  - Commercial land
  - Industrial land

### 10. Policy Impact Analysis (정책영향분석)

- **Dataset ID**: `policy_impact`
- **URL**: https://data.kbland.kr/kbstats/wpi
- **Format**: PDF/Excel
- **Update Frequency**: As needed
- **Data Contents**:
  - Tax policy effects
  - Regulation impacts
  - Market interventions

## Usage with Python Package

### Basic Usage
```python
from connectors.kbland_enhanced import KBLandEnhancedConnector

# Initialize connector
kb = KBLandEnhancedConnector()

# Get catalog
catalog = kb.get_catalog()

# Download specific dataset
success, filepath = kb.download_dataset('price_index')

# Download all datasets
results = kb.download_all_datasets()
```

### Available Dataset IDs
- `price_index` - KB Housing Price Index
- `jeonse_index` - KB Jeonse Price Index
- `monthly_rent` - KB Monthly Rent Index
- `transaction_volume` - Real Estate Transaction Volume
- `market_sentiment` - Market Sentiment Index
- `regional_analysis` - Regional Market Analysis
- `apartment_ranking` - Apartment Complex Rankings
- `office_retail` - Office & Retail Market
- `land_price` - Land Price Index
- `policy_impact` - Policy Impact Analysis

## Data Update Schedule
- **Monthly Data**: Released on the last Monday of each month
- **Quarterly Data**: Released in January, April, July, October
- **Weekly Rankings**: Updated every Monday
- **Special Reports**: Released as needed for policy changes

## Notes
- Data lag: Approximately 1 month (e.g., January data released end of February)
- Historical data: Available from 1986 for major indices
- Regional coverage: Nationwide with special focus on Seoul metropolitan area
- Excel files typically contain multiple sheets with different regional breakdowns
