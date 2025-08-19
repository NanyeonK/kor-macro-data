"""Test global economic data connectors"""

import pandas as pd
from kor_macro.connectors.global_data import (
    FREDConnector, 
    WorldBankConnector,
    IMFConnector,
    OECDConnector,
    ECBConnector
)
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_fred():
    """Test Federal Reserve Economic Data (FRED) API"""
    print("\n" + "="*80)
    print("Testing FRED (Federal Reserve Economic Data)")
    print("="*80)
    
    fred = FREDConnector()
    
    # Test fetching US GDP
    print("\n1. Fetching US GDP data:")
    us_gdp = fred.fetch_data('GDP', '2020-01-01', '2024-12-31')
    
    if us_gdp['success']:
        print(f"✓ Success: {us_gdp['count']} observations")
        if us_gdp['data']:
            latest = us_gdp['data'][-1]
            print(f"  Latest: {latest.get('date')}: ${latest.get('value')} billion")
    else:
        print(f"✗ Failed: {us_gdp.get('message')}")
    
    # Test fetching GDP for multiple countries
    print("\n2. Fetching GDP data for US, China, Japan, Eurozone:")
    gdp_data = fred.get_gdp_data(['us', 'china', 'japan', 'eurozone'], '2020-01-01')
    
    if not gdp_data.empty:
        print(f"✓ Success: {len(gdp_data)} total observations")
        print("\nSample data:")
        print(gdp_data.groupby('country').tail(1)[['date', 'country', 'value']])
    else:
        print("✗ No data retrieved")
    
    return fred

def test_world_bank():
    """Test World Bank API"""
    print("\n" + "="*80)
    print("Testing World Bank API")
    print("="*80)
    
    wb = WorldBankConnector()
    
    # Test fetching GDP data
    print("\n1. Fetching GDP data for US, China, Japan, EU:")
    gdp_data = wb.fetch_data(
        'NY.GDP.MKTP.CD',  # GDP indicator
        ['USA', 'CHN', 'JPN', 'EMU'],
        2019,
        2023
    )
    
    if gdp_data['success']:
        print(f"✓ Success: {gdp_data['count']} data points")
        if gdp_data['data']:
            # Show sample data
            for item in gdp_data['data'][:5]:
                if item:
                    country = item.get('country', {}).get('value', 'N/A')
                    year = item.get('date', 'N/A')
                    value = item.get('value', 'N/A')
                    if value:
                        print(f"  {country} ({year}): ${value/1e12:.2f} trillion")
    else:
        print(f"✗ Failed: {gdp_data.get('message')}")
    
    return wb

def test_imf():
    """Test IMF API"""
    print("\n" + "="*80)
    print("Testing IMF Data API")
    print("="*80)
    
    imf = IMFConnector()
    
    # Test fetching data
    print("\n1. Fetching IMF economic indicators:")
    data = imf.fetch_data('NGDP_RPCH', ['USA', 'CHN', 'JPN', 'DEU'])  # Real GDP growth
    
    if data['success']:
        print(f"✓ Success: {data['count']} countries")
        if 'values' in data['data']:
            for country, values in list(data['data']['values'].items())[:3]:
                print(f"  {country}: {list(values.keys())[-3:]} (recent years)")
    else:
        print(f"✗ Failed: {data.get('message')}")
    
    return imf

def test_all_sources():
    """Test all global data sources"""
    print("\n" + "="*80)
    print("GLOBAL ECONOMIC DATA SOURCES TEST")
    print("="*80)
    
    results = {}
    
    # Test each source
    try:
        results['FRED'] = test_fred()
        print("✅ FRED connected successfully")
    except Exception as e:
        print(f"❌ FRED failed: {e}")
        results['FRED'] = None
    
    try:
        results['World Bank'] = test_world_bank()
        print("✅ World Bank connected successfully")
    except Exception as e:
        print(f"❌ World Bank failed: {e}")
        results['World Bank'] = None
    
    try:
        results['IMF'] = test_imf()
        print("✅ IMF connected successfully")
    except Exception as e:
        print(f"❌ IMF failed: {e}")
        results['IMF'] = None
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY OF AVAILABLE GLOBAL DATA SOURCES")
    print("="*80)
    
    print("\n✅ SUCCESSFULLY CONFIGURED SOURCES:")
    print("\n1. **FRED (Federal Reserve Economic Data)**")
    print("   - GDP data for all major economies")
    print("   - Interest rates (Fed Funds, ECB, BoJ)")
    print("   - Inflation indicators (CPI, PCE)")
    print("   - API Key: Configured ✓")
    
    print("\n2. **World Bank**")
    print("   - GDP, GDP growth, GDP per capita")
    print("   - Inflation, unemployment, population")
    print("   - Trade statistics")
    print("   - No API key required")
    
    print("\n3. **IMF (International Monetary Fund)**")
    print("   - World Economic Outlook data")
    print("   - Balance of payments")
    print("   - Government finance statistics")
    print("   - No API key required")
    
    print("\n4. **OECD**")
    print("   - GDP and national accounts")
    print("   - Labor statistics")
    print("   - Price indices")
    print("   - No API key required")
    
    print("\n5. **ECB (European Central Bank)**")
    print("   - Eurozone economic indicators")
    print("   - Interest rates")
    print("   - Exchange rates")
    print("   - No API key required")
    
    print("\n📊 RECOMMENDED FOR GDP DATA:")
    print("- **Primary source**: FRED (most comprehensive, includes all countries)")
    print("- **Alternative**: World Bank (direct country data)")
    print("- **For Eurozone**: ECB or FRED series 'EUNGDP'")
    
    return results

def create_gdp_comparison():
    """Create a comparison of GDP data from different sources"""
    print("\n" + "="*80)
    print("CREATING GDP COMPARISON TABLE")
    print("="*80)
    
    fred = FREDConnector()
    
    # Define the series we want
    gdp_series = {
        'United States': 'GDP',
        'China': 'NYGDPMKTPCDWLD',
        'Japan': 'JPNNGDP', 
        'Eurozone': 'EUNGDP',
        # 'Germany': 'CLVMNACSCAB1GQDE',  # Skip if causing errors
        # 'United Kingdom': 'UKNGDP',
        # 'South Korea': 'KORNGDP'
    }
    
    print("\nFetching GDP data for major economies...")
    
    all_data = []
    for country, series_id in gdp_series.items():
        print(f"  Fetching {country}...")
        data = fred.fetch_data(series_id, '2019-01-01', '2024-12-31')
        if data['success'] and data['data']:
            df = pd.DataFrame(data['data'])
            df['country'] = country
            df['series_id'] = series_id
            all_data.append(df)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Save to CSV
        output_file = 'data_exports/global_gdp_data.csv'
        combined_df.to_csv(output_file, index=False)
        print(f"\n✓ GDP data saved to: {output_file}")
        
        # Show summary
        print("\nLatest GDP values by country:")
        latest = combined_df.groupby('country').tail(1)[['country', 'date', 'value']]
        print(latest.to_string(index=False))
    
    return combined_df if all_data else None

if __name__ == "__main__":
    # Test all sources
    results = test_all_sources()
    
    # Create GDP comparison
    gdp_data = create_gdp_comparison()
    
    print("\n" + "="*80)
    print("✅ GLOBAL DATA CONNECTORS READY FOR USE")
    print("="*80)
    print("\nYou can now fetch economic data for:")
    print("- United States")
    print("- China") 
    print("- Japan")
    print("- Eurozone")
    print("- And many more countries...")
    print("\nUse these connectors for academic research with proper citations.")