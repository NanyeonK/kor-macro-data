# Representative Data Catalog - All APIs

## 📊 Korean Data Sources

### 1. Bank of Korea (BOK) - 863+ Economic Statistics

#### Representative Datasets:
| Category | Dataset ID | Description | Frequency | Period |
|----------|------------|-------------|-----------|--------|
| **Monetary Policy** | 722Y001 | Base Rate (기준금리) | Monthly | 1999-Present |
| **Exchange Rates** | 731Y001 | USD/KRW Exchange Rate | Daily | 1980-Present |
| **Money Supply** | 101Y004 | M2 Money Supply | Monthly | 1970-Present |
| **GDP** | 200Y001 | Gross Domestic Product | Quarterly | 1960-Present |
| **Inflation** | 901Y009 | Consumer Price Index | Monthly | 1965-Present |
| **Housing** | 901Y067 | Housing Price Index | Monthly | 1986-Present |
| **Trade** | 301Y013 | Exports and Imports | Monthly | 1970-Present |
| **Employment** | 901Y016 | Unemployment Rate | Monthly | 1999-Present |
| **Financial Markets** | 817Y002 | KOSPI Index | Daily | 1980-Present |
| **Interest Rates** | 721Y001 | Market Interest Rates | Daily | 1995-Present |

#### Sample Data Structure:
```json
{
  "STAT_CODE": "722Y001",
  "STAT_NAME": "Base Rate",
  "TIME": "2024.10",
  "DATA_VALUE": "3.25",
  "UNIT_NAME": "%"
}
```

### 2. KOSIS (Korean Statistical Information Service)

#### Representative Datasets:
| Category | Table ID | Description | Coverage | Update |
|----------|----------|-------------|----------|---------|
| **Population** | DT_1B040A3 | Population Census | National/Regional | Monthly |
| **Employment** | DT_1DA7001S | Employment Rate | By Age/Gender | Monthly |
| **Real Estate** | DT_1YL2001 | Apartment Price Index | By Region | Monthly |
| **Transactions** | DT_1YL2101 | Real Estate Transactions | By Type | Monthly |
| **Household** | DT_1JC1501 | Household Statistics | By Region | Annual |
| **Wages** | DT_1J17001 | Average Wages | By Industry | Monthly |
| **Regional GDP** | DT_1C61 | GRDP | By Province | Annual |
| **Construction** | DT_1YL1601 | Building Permits | By Type | Monthly |
| **Demographics** | DT_1B8000F | Birth/Death Statistics | National | Monthly |
| **Education** | DT_1YL8001 | Education Statistics | By Level | Annual |

#### Sample Data Structure:
```json
{
  "PRD_DE": "202401",
  "C1_NM": "Seoul",
  "C2_NM": "Apartment",
  "DT": "51430018",
  "UNIT_NM": "People"
}
```

### 3. Seoul Open Data Plaza

#### Representative Datasets:
| Service | ID | Description | Format | Real-time |
|---------|-----|-------------|--------|-----------|
| **Air Quality** | RealtimeCityAir | PM10, PM2.5, O3, NO2 | JSON | Yes |
| **Real Estate** | tbLnOpendataRtmsV | Transaction Prices | JSON | Monthly |
| **Transportation** | CardSubwayStatsNew | Subway Passengers | JSON | Daily |
| **Parking** | GetParkInfo | Public Parking | JSON | Real-time |
| **Population** | PopulationDensityOfSeoul | Population by District | JSON | Quarterly |
| **Budget** | OpenFinanceData | City Budget | JSON | Annual |
| **Business** | landBizInfo | Commercial Properties | JSON | Quarterly |
| **Rent** | tbLnOpendataRentV | Rental Prices | JSON | Monthly |
| **Weather** | WeatherInformation | Temperature, Rain | JSON | Hourly |
| **Traffic** | TrafficSpeed | Road Speed | JSON | Real-time |

#### Sample Data Structure:
```json
{
  "MSRSTE_NM": "Gangnam",
  "PM10": "35",
  "PM25": "18",
  "O3": "0.045",
  "MSRDT": "202408191700"
}
```

### 4. KB Land (KB부동산) - Real Estate Focus

#### Representative Datasets:
| Category | Dataset | Description | Format | Frequency |
|----------|---------|-------------|--------|-----------|
| **Price Index** | price_index | KB Housing Price Index | Excel | Monthly |
| **Jeonse** | jeonse_index | Jeonse Price Index | Excel | Monthly |
| **Rent** | monthly_rent | Monthly Rent Index | Excel | Monthly |
| **Transactions** | transaction_volume | Transaction Volume | Excel/CSV | Monthly |
| **Sentiment** | market_sentiment | Market Sentiment Index | Excel | Monthly |
| **Regional** | regional_analysis | 25 Seoul Districts + 31 Gyeonggi Cities | Excel | Monthly |
| **Rankings** | apartment_ranking | Top 100 Complexes | CSV | Weekly |
| **Commercial** | office_retail | Office/Retail Market | Excel | Quarterly |
| **Land** | land_price | Land Price Index | Excel | Quarterly |
| **Policy** | policy_impact | Policy Impact Analysis | PDF/Excel | As needed |

#### Sample Data Structure:
```
District | Apartment_Index | Jeonse_Index | Transaction_Count
---------|-----------------|--------------|------------------
Gangnam  | 125.3          | 118.7        | 523
Seocho   | 122.1          | 115.4        | 412
```

## 🌍 Global Data Sources

### 5. FRED (Federal Reserve Economic Data)

#### Representative Series:
| Category | Series ID | Description | Frequency | History |
|----------|-----------|-------------|-----------|---------|
| **US GDP** | GDP | Nominal GDP | Quarterly | 1947-Present |
| **Real GDP** | GDPC1 | Real GDP | Quarterly | 1947-Present |
| **China GDP** | NYGDPMKTPCDWLD | China GDP | Annual | 1960-Present |
| **Japan GDP** | JPNNGDP | Japan GDP | Quarterly | 1994-Present |
| **EU GDP** | EUNGDP | Eurozone GDP | Quarterly | 1995-Present |
| **Fed Rate** | DFF | Federal Funds Rate | Daily | 1954-Present |
| **US CPI** | CPIAUCSL | Consumer Price Index | Monthly | 1947-Present |
| **Unemployment** | UNRATE | US Unemployment Rate | Monthly | 1948-Present |
| **10Y Treasury** | DGS10 | 10-Year Treasury Rate | Daily | 1962-Present |
| **Oil Price** | DCOILWTICO | WTI Crude Oil | Daily | 1986-Present |

#### Sample Data Structure:
```json
{
  "date": "2024-10-01",
  "series_id": "GDP",
  "value": "29723.864",
  "units": "Billions of Dollars"
}
```

### 6. World Bank

#### Representative Indicators:
| Indicator | Code | Description | Countries | Years |
|-----------|------|-------------|-----------|-------|
| **GDP** | NY.GDP.MKTP.CD | GDP (current US$) | 217 | 1960-2023 |
| **GDP Growth** | NY.GDP.MKTP.KD.ZG | GDP growth (%) | 217 | 1961-2023 |
| **GDP Per Capita** | NY.GDP.PCAP.CD | GDP per capita | 217 | 1960-2023 |
| **Inflation** | FP.CPI.TOTL.ZG | Inflation rate | 217 | 1960-2023 |
| **Unemployment** | SL.UEM.TOTL.ZS | Unemployment (%) | 217 | 1991-2023 |
| **Population** | SP.POP.TOTL | Total population | 217 | 1960-2023 |
| **Exports** | NE.EXP.GNFS.CD | Exports (US$) | 217 | 1960-2023 |
| **Imports** | NE.IMP.GNFS.CD | Imports (US$) | 217 | 1960-2023 |
| **FDI** | BX.KLT.DINV.CD.WD | Foreign Direct Investment | 217 | 1970-2023 |
| **Debt** | DT.DOD.DECT.CD | External debt | 217 | 1970-2023 |

#### Sample Data Structure:
```json
{
  "country": {"id": "USA", "value": "United States"},
  "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP"},
  "date": "2023",
  "value": 27360935000000
}
```

### 7. IMF (International Monetary Fund)

#### Representative Datasets:
| Dataset | Code | Description | Coverage | Frequency |
|---------|------|-------------|----------|-----------|
| **WEO GDP** | NGDP_RPCH | Real GDP Growth | 190 countries | Semi-annual |
| **Inflation** | PCPIPCH | Inflation Rate | 190 countries | Semi-annual |
| **Current Account** | BCA | Current Account Balance | 190 countries | Annual |
| **Debt** | GGXWDG | Government Debt/GDP | 190 countries | Annual |
| **Unemployment** | LUR | Unemployment Rate | 190 countries | Annual |
| **Exchange Rates** | ENDA | Exchange Rate | 190 countries | Monthly |
| **Reserves** | RESA | Foreign Reserves | 190 countries | Monthly |
| **Trade Balance** | TB | Trade Balance | 190 countries | Quarterly |
| **Budget Balance** | GGB | Government Budget | 190 countries | Annual |
| **Interest Rates** | FPOLM | Policy Rate | 190 countries | Monthly |

### 8. OECD

#### Representative Statistics:
| Category | Dataset | Description | Countries | Frequency |
|----------|---------|-------------|-----------|-----------|
| **GDP** | SNA_TABLE1 | National Accounts | 38 OECD | Quarterly |
| **Prices** | PRICES_CPI | Consumer Prices | 38 OECD | Monthly |
| **Labor** | STLABOUR | Employment/Unemployment | 38 OECD | Monthly |
| **Trade** | IMTS | International Trade | 38 OECD | Monthly |
| **Production** | PRINTO01 | Industrial Production | 38 OECD | Monthly |
| **Finance** | MEI_FIN | Financial Indicators | 38 OECD | Daily/Monthly |
| **Housing** | HOUSE_PRICES | House Price Indices | 38 OECD | Quarterly |
| **Productivity** | PDB_LV | Labor Productivity | 38 OECD | Annual |
| **Education** | EAG_NEAC | Education Statistics | 38 OECD | Annual |
| **Health** | HEALTH_STAT | Health Statistics | 38 OECD | Annual |

### 9. ECB (European Central Bank)

#### Representative Data:
| Category | Key | Description | Frequency | Coverage |
|----------|-----|-------------|-----------|----------|
| **GDP** | MNA.Q.Y.I8.W2.S1.S1.B.B1GQ | Eurozone GDP | Quarterly | 1995-Present |
| **Inflation** | ICP.M.U2.N.000000.4.ANR | HICP Inflation | Monthly | 1996-Present |
| **Interest Rates** | FM.M.U2.EUR.RT.MM.EURIBOR3MD | EURIBOR | Daily | 1999-Present |
| **Exchange Rates** | EXR.D.USD.EUR.SP00.A | EUR/USD | Daily | 1999-Present |
| **Money Supply** | BSI.M.U2.N.A.L10.X.1.Z5.0000.Z01.E | M3 | Monthly | 1997-Present |
| **Unemployment** | LFSI.M.I8.S.UNEHRT.TOTAL0.15_74.T | Unemployment | Monthly | 1998-Present |
| **Trade** | TRD.M.I8.N.TTTT.MM.X.V | Trade Balance | Monthly | 1999-Present |
| **Banking** | CBD2.M.U2.W0.67._Z._Z.A.F.I2004._Z.S.1.G1 | Bank Lending | Monthly | 2003-Present |
| **Securities** | SEC.M.I8.1000.F51100.N.I.EUR | Bond Issuance | Monthly | 1999-Present |
| **Confidence** | BS.M.I8.SENT.BAL.OVRL.EA.INDEX | Economic Sentiment | Monthly | 1985-Present |

### 10. EIA (US Energy Information Administration)

#### Representative Data:
| Category | Series ID | Description | Frequency | Units |
|----------|-----------|-------------|-----------|-------|
| **Oil Price** | PET.RWTC.D | WTI Crude Oil Price | Daily | $/barrel |
| **Gas Price** | PET.EMM_EPM0_PTE_NUS_DPG.W | Gasoline Price | Weekly | $/gallon |
| **Natural Gas** | NG.RNGWHHD.D | Natural Gas Price | Daily | $/MMBtu |
| **Electricity** | ELEC.PRICE.US-ALL.M | Electricity Price | Monthly | cents/kWh |
| **Oil Production** | PET.MCRFPUS2.M | US Oil Production | Monthly | Million barrels/day |
| **Oil Inventory** | PET.WCESTUS1.W | Oil Inventories | Weekly | Million barrels |
| **Renewable** | ELEC.GEN.ALL-US-99.M | Renewable Generation | Monthly | MWh |
| **CO2 Emissions** | EMISS.CO2-TOTV-TT-TO-US.A | CO2 Emissions | Annual | Million metric tons |
| **Energy Consumption** | TOTAL.TETCBUS.A | Total Energy Use | Annual | Quadrillion Btu |
| **Coal Production** | COAL.PRODUCTION.TOT.A | Coal Production | Annual | Million short tons |

## Data Availability Summary

### Coverage by Region:
- **Korea**: Comprehensive economic, financial, and real estate data
- **United States**: Complete economic indicators from 1947
- **China**: World Bank data from 1960, limited high-frequency data
- **Japan**: Quarterly GDP from 1994, monthly indicators available
- **Eurozone**: Data from 1995-1999 depending on indicator
- **Global**: 217 countries via World Bank, 190 via IMF

### Update Frequencies:
- **Real-time**: Seoul air quality, KB apartment rankings
- **Daily**: Exchange rates, stock indices, oil prices
- **Weekly**: KB apartment rankings, EIA oil inventories  
- **Monthly**: Most economic indicators, real estate prices
- **Quarterly**: GDP, national accounts
- **Annual**: Population, education, health statistics

### Historical Data Depth:
- **Longest**: US data from 1947 (FRED)
- **Korea**: BOK from 1960s, detailed from 1980s
- **Global**: World Bank from 1960 for most countries
- **Recent**: Eurozone from 1995-1999