# Korean Macro Data - Complete Data Catalog

This comprehensive catalog lists all available data series from our 10 integrated data sources. Use this guide to find the exact indicators you need for your research.

## Table of Contents
1. [Korean Data Sources](#korean-data-sources)
   - [Bank of Korea (BOK)](#1-bank-of-korea-bok)
   - [KOSIS](#2-kosis)
   - [KB Land](#3-kb-land)
   - [Seoul Open Data](#4-seoul-open-data)
2. [Global Data Sources](#global-data-sources)
   - [EIA](#5-eia-energy-information-administration)
   - [FRED](#6-fred-federal-reserve-economic-data)
   - [World Bank](#7-world-bank)
   - [IMF](#8-imf-international-monetary-fund)
   - [OECD](#9-oecd)
   - [ECB](#10-ecb-european-central-bank)
3. [Quick Reference](#quick-reference)

---

## Korean Data Sources

### 1. Bank of Korea (BOK)

**Access**: Direct API | **Update Frequency**: Daily/Monthly/Quarterly | **History**: 1960-present

#### Key Economic Indicators (20 Series)
```python
# Example: Get base rate
bok = BOKConnector()
data = bok.get_base_rate('2020-01-01', '2024-12-31')
```

| Series Code | Description | Frequency | Start Date |
|------------|-------------|-----------|------------|
| `722Y001/0101000` | Base Rate | Daily | 1999-05 |
| `721Y001/0101000` | Call Rate (Overnight) | Daily | 1991-01 |
| `731Y003/1070000` | USD/KRW Exchange Rate | Daily | 1964-01 |
| `731Y003/1070001` | EUR/KRW Exchange Rate | Daily | 1999-01 |
| `731Y003/1070002` | JPY/KRW Exchange Rate | Daily | 1964-01 |
| `901Y014/AI1AA` | M1 Money Supply | Monthly | 1970-01 |
| `901Y014/AI2AA` | M2 Money Supply | Monthly | 1970-01 |
| `901Y015/AI1BB` | Lf Money Supply | Monthly | 2001-12 |
| `200Y001/I16A` | GDP (Nominal) | Quarterly | 1960-Q1 |
| `200Y001/I16B` | GDP (Real) | Quarterly | 1960-Q1 |

#### Price Indices (15 Series)
| Series Code | Description | Frequency | Start Date |
|------------|-------------|-----------|------------|
| `901Y009/0` | Consumer Price Index (All Items) | Monthly | 1965-01 |
| `901Y009/1` | CPI Core (Excluding Food & Energy) | Monthly | 1975-01 |
| `404Y014/6AA` | Producer Price Index | Monthly | 1965-01 |
| `404Y014/6AB` | PPI Core | Monthly | 1968-01 |
| `404Y015/CAA` | Import Price Index | Monthly | 1971-01 |
| `404Y015/CAB` | Export Price Index | Monthly | 1971-01 |

#### Financial Markets (25 Series)
| Series Code | Description | Frequency | Start Date |
|------------|-------------|-----------|------------|
| `817Y002/KOSPI` | KOSPI Index | Daily | 1980-01 |
| `817Y002/KOSDAQ` | KOSDAQ Index | Daily | 1996-07 |
| `721Y001/[5030000-5030012]` | Government Bond Yields (1Y-30Y) | Daily | Various |
| `721Y001/5030003` | Treasury Bond 3-Year | Daily | 1995-01 |
| `721Y001/5030005` | Treasury Bond 5-Year | Daily | 1995-01 |
| `721Y001/5030010` | Treasury Bond 10-Year | Daily | 2000-10 |

#### Housing & Real Estate (30 Series)
| Series Code | Description | Frequency | Coverage |
|------------|-------------|-----------|----------|
| `901Y066/KB01` | KB National Housing Price Index | Monthly | National |
| `901Y066/KB02` | KB Seoul Housing Price Index | Monthly | Seoul |
| `901Y066/KB03` | KB Apartment Price Index | Monthly | National |
| `901Y067/KB01` | KB Jeonse Price Index | Monthly | National |
| `901Y067/KB02` | KB Seoul Jeonse Index | Monthly | Seoul |
| `901Y068/KB01` | KB Monthly Rent Index | Monthly | National |

#### Trade & Balance of Payments (20 Series)
| Series Code | Description | Frequency | Start Date |
|------------|-------------|-----------|------------|
| `301Y013/1` | Exports (Total) | Monthly | 1965-01 |
| `301Y013/2` | Imports (Total) | Monthly | 1965-01 |
| `301Y013/3` | Trade Balance | Monthly | 1965-01 |
| `301Y017/*` | Current Account | Monthly | 1980-01 |
| `301Y018/*` | Capital Account | Monthly | 1980-01 |

#### Employment & Labor (15 Series)
| Series Code | Description | Frequency | Start Date |
|------------|-------------|-----------|------------|
| `901Y016/1` | Unemployment Rate | Monthly | 1999-06 |
| `901Y016/2` | Employment Rate | Monthly | 1999-06 |
| `901Y016/3` | Labor Force Participation | Monthly | 1999-06 |
| `901Y017/*` | Average Wages | Monthly | 1993-01 |

---

### 2. KOSIS

**Access**: Direct API | **Update Frequency**: Monthly/Quarterly/Yearly | **History**: 1970-present

#### Population & Demographics
```python
# Example: Get population data
kosis = KOSISConnector()
data = kosis.fetch_data('DT_1B040A3', start_year=2010)
```

| Table ID | Description | Update | Coverage |
|----------|-------------|--------|----------|
| `DT_1B040A3` | Population by Age and Gender | Annual | National/Regional |
| `DT_1B040B1` | Birth Statistics | Monthly | National/Regional |
| `DT_1B040B2` | Death Statistics | Monthly | National/Regional |
| `DT_1B040M1` | Marriage & Divorce | Monthly | National/Regional |
| `DT_1B35001` | Household Projections | Annual | National |

#### Employment & Wages
| Table ID | Description | Update | Coverage |
|----------|-------------|--------|----------|
| `DT_118N_LFA9` | Employment by Industry | Monthly | National |
| `DT_118N_PAIE01` | Average Wages by Industry | Quarterly | National |
| `DT_118N_MON033` | Working Hours | Monthly | National |
| `DT_1DA7004S` | Youth Employment | Monthly | National |

#### Regional Economics
| Table ID | Description | Update | Coverage |
|----------|-------------|--------|----------|
| `DT_1C86` | Regional GDP (GRDP) | Annual | 17 Regions |
| `DT_1YL20631` | Regional CPI | Monthly | Major Cities |
| `DT_2KAA308` | Regional Employment | Quarterly | 17 Regions |

---

### 3. KB Land

**Access**: API Connector | **Update Frequency**: Weekly/Monthly | **History**: 2003-present

#### Housing Price Indices
```python
# Example: Get apartment prices
kb = KBLandConnector()

# Get monthly apartment price index
apt_prices = kb.get_housing_index(
    house_type='apartment',  # 'apartment', 'house', 'officetel'
    region='서울',           # Korean region name
    start_date='2023-01-01',
    end_date='2024-12-31'
)

# Get latest values
print(f"Latest index: {apt_prices.iloc[-1]['price_index']:.2f}")
print(f"MoM change: {apt_prices.iloc[-1]['mom_change']:.2f}%")
print(f"YoY change: {apt_prices.iloc[-1]['yoy_change']:.2f}%")
```

| Dataset | Description | Frequency | Regional Coverage |
|---------|-------------|-----------|-------------------|
| **매매가격지수** | Purchase Price Index | Monthly | 250+ regions |
| - 아파트 | Apartments | Weekly/Monthly | National/Regional/District |
| - 단독주택 | Detached Houses | Monthly | National/Regional |
| - 연립주택 | Row Houses | Monthly | National/Regional |
| - 오피스텔 | Officetels | Monthly | Major Cities |

#### Jeonse (전세) Indices
```python
# Get Jeonse price index
jeonse = kb.get_jeonse_index(
    region='서울',
    start_date='2023-01-01',
    end_date='2024-12-31'
)
```

| Dataset | Description | Frequency | Coverage |
|---------|-------------|-----------|----------|
| **전세가격지수** | Jeonse Price Index | Monthly | 250+ regions |
| - 아파트 전세 | Apartment Jeonse | Weekly/Monthly | All districts |
| - 단독주택 전세 | House Jeonse | Monthly | Major cities |
| - 연립주택 전세 | Row House Jeonse | Monthly | Major cities |

#### Monthly Rent Indices
| Dataset | Description | Frequency | Coverage |
|---------|-------------|-----------|----------|
| **월세가격지수** | Monthly Rent Index | Monthly | National/Regional |
| - 아파트 월세 | Apartment Rent | Monthly | All districts |
| - 오피스텔 월세 | Officetel Rent | Monthly | Major cities |
| - 월세전환율 | Jeonse-to-Rent Conversion Rate | Monthly | National |

#### Market Indicators
```python
# Get market trends and sentiment
market = kb.get_market_trend(region='서울')
outlook = kb.get_price_outlook(region='서울')

# Regional comparison
comparison = kb.get_regional_comparison(
    house_type='apartment',
    regions=['서울', '부산', '대구', '인천', '경기']
)
```

| Indicator | Description | Frequency | Coverage |
|-----------|-------------|-----------|----------|
| **매매수급동향** | Supply-Demand Trends | Weekly | National |
| **전세수급동향** | Jeonse Supply-Demand | Weekly | National |
| **가격전망지수** | Price Outlook Index | Monthly | National |
| **거래동향** | Transaction Volume | Monthly | Regional |

---

### 4. Seoul Open Data

**Access**: Open API | **Update Frequency**: Real-time/Daily/Monthly | **History**: 2010-present

```python
# Example: Get Seoul real estate transactions
seoul = SeoulDataConnector()
data = seoul.get_real_estate_transactions('apartment', '2024-01')
```

| Service | Description | Update | Records |
|---------|-------------|--------|---------|
| **부동산 실거래가** | Real Estate Transactions | Daily | 1M+ |
| **상권분석** | Commercial District Analysis | Quarterly | 100K+ |
| **인구통계** | Population Statistics | Monthly | District-level |
| **교통량** | Traffic Volume | Hourly | Real-time |
| **대기질** | Air Quality | Hourly | 50+ stations |

---

## Global Data Sources

### 5. EIA (Energy Information Administration)

**Access**: Direct API | **Update Frequency**: Daily/Weekly/Monthly | **History**: 1986-present

#### Petroleum Markets
```python
# Example: Get WTI crude prices
eia = EIAConnector()
data = eia.get_wti_crude_price('2023-01-01', '2024-01-01')
```

| Series ID | Description | Frequency | Unit |
|-----------|-------------|-----------|------|
| `PET.RWTC.D` | WTI Crude Oil Spot Price | Daily | $/barrel |
| `PET.RBRTE.D` | Brent Crude Oil Spot Price | Daily | $/barrel |
| `PET.EMM_EPM0_PTE_NUS_DPG.W` | US Gasoline Retail Price | Weekly | $/gallon |
| `PET.WCESTUS1.W` | US Crude Oil Inventories | Weekly | Thousand barrels |
| `PET.WCRFPUS2.W` | US Crude Oil Production | Weekly | Thousand barrels/day |
| `PET.STEO.COPR_OPEC.M` | OPEC Production | Monthly | Million barrels/day |

#### Natural Gas Markets
| Series ID | Description | Frequency | Unit |
|-----------|-------------|-----------|------|
| `NG.RNGWHHD.D` | Henry Hub Spot Price | Daily | $/MMBtu |
| `NG.N9070US2.M` | US Natural Gas Production | Monthly | Billion cubic feet |
| `NG.N3010US2.M` | US Natural Gas Consumption | Monthly | Billion cubic feet |
| `NG.N5010US1.W` | US Natural Gas Storage | Weekly | Billion cubic feet |

#### Korea Energy Data
| Series ID | Description | Frequency | Unit |
|-----------|-------------|-----------|------|
| `INTL.5-2-KOR-TBPD.A` | Korea Petroleum Consumption | Annual | Thousand barrels/day |
| `INTL.2-12-KOR-BKWH.A` | Korea Electricity Generation | Annual | Billion kWh |
| `INTL.5-2-JPN-TBPD.A` | Japan Petroleum Consumption | Annual | Thousand barrels/day |
| `INTL.5-2-CHN-TBPD.A` | China Petroleum Consumption | Annual | Thousand barrels/day |

---

### 6. FRED (Federal Reserve Economic Data)

**Access**: Direct API | **Update Frequency**: Real-time/Daily/Monthly | **History**: 1947-present

#### Major Economy GDP
```python
# Example: Get US GDP data
fred = FREDConnector()
data = fred.fetch_data('GDP', start_date='2010-01-01')
```

| Series ID | Description | Frequency | Countries |
|-----------|-------------|-----------|-----------|
| `GDP` | US GDP (Nominal) | Quarterly | US |
| `GDPC1` | US GDP (Real) | Quarterly | US |
| `A191RL1Q225SBEA` | US GDP Growth Rate | Quarterly | US |
| `KORNGDP` | South Korea GDP | Annual | Korea |
| `JPNNGDP` | Japan GDP | Annual | Japan |
| `CLVMNACSCAB1GQDE` | Germany GDP (Real) | Quarterly | Germany |

#### Interest Rates
| Series ID | Description | Frequency | Source |
|-----------|-------------|-----------|--------|
| `DFF` | Federal Funds Rate | Daily | Fed |
| `DGS10` | US 10-Year Treasury | Daily | Treasury |
| `DGS2` | US 2-Year Treasury | Daily | Treasury |
| `ECBDFR` | ECB Deposit Rate | Daily | ECB |
| `IRSTCB01JPM156N` | Bank of Japan Rate | Monthly | BOJ |

#### Inflation Indicators
| Series ID | Description | Frequency | Coverage |
|-----------|-------------|-----------|----------|
| `CPIAUCSL` | US CPI All Items | Monthly | US |
| `CPILFESL` | US Core CPI | Monthly | US |
| `PCEPI` | US PCE Index | Monthly | US |
| `CP0000EZ19M086NEST` | Eurozone CPI | Monthly | Eurozone |

---

### 7. World Bank

**Access**: Direct API | **Update Frequency**: Annual/Quarterly | **History**: 1960-present

```python
# Example: Get GDP data for multiple countries
wb = WorldBankConnector()
data = wb.fetch_data('NY.GDP.MKTP.CD', countries=['USA', 'KOR', 'CHN', 'JPN'])
```

| Indicator Code | Description | Frequency | Countries |
|---------------|-------------|-----------|-----------|
| `NY.GDP.MKTP.CD` | GDP (current US$) | Annual | 200+ |
| `NY.GDP.MKTP.KD.ZG` | GDP growth (annual %) | Annual | 200+ |
| `NY.GDP.PCAP.CD` | GDP per capita | Annual | 200+ |
| `FP.CPI.TOTL.ZG` | Inflation (CPI) | Annual | 200+ |
| `SL.UEM.TOTL.ZS` | Unemployment rate | Annual | 200+ |
| `SP.POP.TOTL` | Total population | Annual | 200+ |
| `NE.EXP.GNFS.CD` | Exports | Annual | 200+ |
| `NE.IMP.GNFS.CD` | Imports | Annual | 200+ |

---

### 8. IMF (International Monetary Fund)

**Access**: Direct API | **Update Frequency**: Quarterly/Annual | **History**: 1980-present

```python
# Example: Get IMF World Economic Outlook data
imf = IMFConnector()
data = imf.fetch_data('NGDP_RPCH', countries=['USA', 'KOR', 'CHN'])
```

| Dataset | Indicators | Frequency | Coverage |
|---------|------------|-----------|----------|
| **WEO** | World Economic Outlook | Semi-annual | 190+ countries |
| - `NGDP_RPCH` | Real GDP Growth | Annual | All |
| - `PCPIPCH` | Inflation Rate | Annual | All |
| - `LUR` | Unemployment Rate | Annual | All |
| **IFS** | International Financial Statistics | Monthly | 190+ countries |
| **BOP** | Balance of Payments | Quarterly | 190+ countries |
| **GFS** | Government Finance Statistics | Annual | 190+ countries |

---

### 9. OECD

**Access**: Direct API | **Update Frequency**: Monthly/Quarterly | **History**: 1970-present

```python
# Example: Get OECD economic indicators
oecd = OECDConnector()
data = oecd.fetch_data('SNA_TABLE1')  # GDP statistics
```

| Dataset | Description | Frequency | Coverage |
|---------|-------------|-----------|----------|
| `SNA_TABLE1` | GDP Statistics | Quarterly | OECD members |
| `PRICES_CPI` | Consumer Prices | Monthly | OECD members |
| `STLABOUR` | Labor Statistics | Monthly | OECD members |
| `IMTS` | International Trade | Monthly | OECD members |
| `KEI` | Key Economic Indicators | Monthly | OECD members |

---

### 10. ECB (European Central Bank)

**Access**: Direct API | **Update Frequency**: Daily/Monthly | **History**: 1999-present

```python
# Example: Get ECB exchange rates
ecb = ECBConnector()
data = ecb.fetch_data('EXR')  # Exchange rates
```

| Dataset | Description | Frequency | Coverage |
|---------|-------------|-----------|----------|
| `ICP` | Inflation and Consumer Prices | Monthly | Eurozone |
| `MIR` | Interest Rates | Daily | Eurozone |
| `EXR` | Exchange Rates | Daily | Major currencies |
| `GDP` | GDP and Economic Activity | Quarterly | Eurozone |

---

## Quick Reference

### By Research Topic

#### **Monetary Policy Analysis**
- BOK: Base rate, money supply (M1/M2)
- FRED: Federal funds rate, treasury yields
- ECB: ECB rates
- IMF: Global interest rates

#### **Housing Market Research**
- KB Land: All housing indices (매매/전세/월세)
- BOK: Housing price indices
- Seoul Data: Real estate transactions
- KOSIS: Household statistics

#### **Energy Markets**
- EIA: Oil prices (WTI/Brent), gas prices
- EIA: Korea energy consumption
- World Bank: Energy indicators

#### **International Trade**
- BOK: Exports/imports, trade balance
- OECD: International trade statistics
- World Bank: Trade indicators
- IMF: Balance of payments

#### **Labor Markets**
- KOSIS: Employment by industry, wages
- BOK: Unemployment rate
- OECD: Labor statistics
- World Bank: Labor indicators

### By Update Frequency

#### **Real-time/Daily**
- BOK: Exchange rates, interest rates
- FRED: Treasury yields, Fed funds rate
- EIA: Oil prices
- ECB: Exchange rates

#### **Weekly**
- KB Land: Housing indices (주간 아파트)
- EIA: Gasoline prices, oil inventories

#### **Monthly**
- BOK: CPI, money supply
- KOSIS: Employment, wages
- KB Land: Housing indices (monthly)
- FRED: Economic indicators

#### **Quarterly/Annual**
- BOK: GDP
- World Bank: Development indicators
- IMF: Economic outlook
- OECD: National accounts

### Data Coverage Timeline

| Source | Earliest Data | Latest Update | Total Series |
|--------|--------------|---------------|--------------|
| BOK | 1960 | Real-time | 863+ |
| KOSIS | 1970 | Monthly | 1000+ |
| KB Land | 2003 | Weekly | 100+ |
| Seoul | 2010 | Daily | 50+ |
| EIA | 1986 | Daily | 200+ |
| FRED | 1947 | Real-time | 500,000+ |
| World Bank | 1960 | Annual | 1000+ |
| IMF | 1980 | Quarterly | 500+ |
| OECD | 1970 | Monthly | 300+ |
| ECB | 1999 | Daily | 200+ |

---

## Usage Examples

### Getting Started with Specific Data

```python
from kor_macro.connectors import *

# Korean housing market analysis
kb = KBLandConnector()
jeonse = kb.get_jeonse_index('서울', '2020-01', '2024-12')

# Global oil market analysis  
eia = EIAConnector()
wti = eia.get_wti_crude_price('2023-01-01')
brent = eia.get_brent_crude_price('2023-01-01')

# Interest rate comparison
bok = BOKConnector()
fred = FREDConnector()
kr_rate = bok.get_base_rate('2023-01-01')
us_rate = fred.fetch_data('DFF', '2023-01-01')

# Merge all data
from kor_macro import KoreanMacroDataMerger
merger = KoreanMacroDataMerger()
# ... load and merge data
```

---

## Notes

- **API Keys Required**: BOK, KOSIS, FRED, EIA (optional)
- **Rate Limits**: Respect API rate limits (typically 1-2 requests/second)
- **Data Quality**: All data undergoes integrity validation
- **Updates**: Data catalog updated quarterly

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).
For usage examples, see [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md).