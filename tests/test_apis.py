"""Test script to list datasets and fetch sample data from Korean APIs"""

import json
import logging
from datetime import datetime
from kor_macro.connectors import BOKConnector, KOSISConnector, SeoulDataConnector

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def print_separator():
    print("="*80)

def test_bok_api():
    """Test Bank of Korea ECOS API"""
    print_separator()
    print("Testing Bank of Korea (BOK) ECOS API")
    print_separator()
    
    try:
        bok = BOKConnector()
        
        # List available datasets
        print("\nAvailable BOK Datasets:")
        datasets = bok.list_datasets()
        for ds in datasets:
            print(f"  - {ds['name']} (ID: {ds['id']})")
        
        # Test fetching base rate data
        print("\nFetching BOK Base Rate (2023-2024):")
        base_rate_data = bok.get_base_rate('20230101', '20241231')
        
        if base_rate_data['success']:
            print(f"  Found {base_rate_data['count']} records")
            # Show first 3 records
            for i, record in enumerate(base_rate_data['data'][:3]):
                if 'TIME' in record and 'DATA_VALUE' in record:
                    print(f"  {record.get('TIME', 'N/A')}: {record.get('DATA_VALUE', 'N/A')}%")
        else:
            print(f"  Failed to fetch data: {base_rate_data.get('message')}")
            
        # Test fetching housing price index
        print("\nFetching Housing Price Index (2023-2024):")
        housing_data = bok.get_housing_price_index('20230101', '20241231')
        
        if housing_data['success']:
            print(f"  Found {housing_data['count']} records")
            # Show first 3 records
            for i, record in enumerate(housing_data['data'][:3]):
                if 'TIME' in record and 'DATA_VALUE' in record:
                    print(f"  {record.get('TIME', 'N/A')}: {record.get('DATA_VALUE', 'N/A')}")
        else:
            print(f"  Failed to fetch data: {housing_data.get('message')}")
            
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        return False

def test_kosis_api():
    """Test KOSIS API"""
    print_separator()
    print("Testing KOSIS (Korean Statistical Information Service) API")
    print_separator()
    
    try:
        kosis = KOSISConnector()
        
        # List available datasets
        print("\nAvailable KOSIS Datasets:")
        datasets = kosis.list_datasets()
        for ds in datasets:
            print(f"  - {ds['name']} (ID: {ds['id']})")
        
        # Test fetching population data
        print("\nFetching Population Statistics (2023-2024):")
        pop_data = kosis.get_population_stats('202301', '202412')
        
        if pop_data['success']:
            print(f"  Found {pop_data['count']} records")
            # Show first 3 records
            for i, record in enumerate(pop_data['data'][:3]):
                period = record.get('PRD_DE', 'N/A')
                value = record.get('DT', 'N/A')
                print(f"  Period {period}: {value}")
        else:
            print(f"  Failed to fetch data: {pop_data.get('message')}")
            
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        return False

def test_seoul_api():
    """Test Seoul Open Data API"""
    print_separator()
    print("Testing Seoul Open Data Plaza API")
    print_separator()
    
    try:
        seoul = SeoulDataConnector()
        
        # List available datasets
        print("\nAvailable Seoul Datasets:")
        datasets = seoul.list_datasets()
        for ds in datasets:
            print(f"  - {ds['name']} (ID: {ds['id']})")
        
        # Test fetching air quality data
        print("\nFetching Seoul Air Quality Data:")
        air_data = seoul.get_air_quality(1, 5)  # Get data for 5 districts
        
        if air_data['success']:
            print(f"  Found {air_data['count']} districts")
            # Show first 3 records
            for i, record in enumerate(air_data['data'][:3]):
                district = record.get('MSRSTE_NM', 'N/A')
                pm10 = record.get('PM10', 'N/A')
                pm25 = record.get('PM25', 'N/A')
                print(f"  {district}: PM10={pm10}, PM2.5={pm25}")
        else:
            print(f"  Failed to fetch data: {air_data.get('message')}")
            
        # Test fetching real estate prices
        print("\nFetching Seoul Real Estate Prices (2024-01):")
        re_data = seoul.get_real_estate_prices('2024', '01', '', 1, 5)
        
        if re_data['success']:
            print(f"  Found {re_data['count']} transactions")
            # Show first 3 records
            for i, record in enumerate(re_data['data'][:3]):
                district = record.get('SGG_NM', 'N/A')
                price = record.get('OBJ_AMT', 'N/A')
                area = record.get('BLDG_AREA', 'N/A')
                print(f"  {district}: {price}만원 ({area}㎡)")
        else:
            print(f"  Note: Real estate data might require specific parameters")
            
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    """Main test function"""
    print("\n" + "="*80)
    print(" Korean Data API Connector Test")
    print("="*80)
    
    # Track results
    results = {}
    
    # Test each API
    results['BOK'] = test_bok_api()
    print()
    
    results['KOSIS'] = test_kosis_api()
    print()
    
    results['Seoul'] = test_seoul_api()
    print()
    
    # Summary
    print_separator()
    print("Test Summary:")
    print_separator()
    for api, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {api}: {status}")
    
    print("\nNote: Some APIs may require additional configuration or valid parameters.")
    print("Check the .env file for API keys and refer to API documentation for details.")

if __name__ == "__main__":
    main()