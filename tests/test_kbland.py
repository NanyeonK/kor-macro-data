"""Test KB Land web scraper"""

import logging
from kor_macro.connectors import KBLandConnector
from pathlib import Path
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_kbland_basic():
    """Test basic KB Land functionality without Selenium"""
    print("\n" + "="*60)
    print("Testing KB Land Connector (Basic Mode)")
    print("="*60)
    
    # Initialize connector without Selenium
    kb = KBLandConnector(use_selenium=False)
    
    # List available datasets
    print("\nAvailable KB Land Datasets:")
    datasets = kb.list_datasets()
    for ds in datasets:
        print(f"  - {ds['name']} (ID: {ds['id']})")
        print(f"    {ds['description']}")
    
    # Test fetching apartment price data
    print("\nFetching Apartment Price Index:")
    price_data = kb.get_apartment_price_index()
    
    if price_data['success']:
        print(f"  ✓ Success: Retrieved {price_data.get('count', 0)} records")
        if price_data['data'] and len(price_data['data']) > 0:
            print(f"  Sample data: {price_data['data'][0]}")
    else:
        print(f"  ✗ Failed: {price_data.get('message', 'Unknown error')}")
    
    # Test fetching jeonse rate
    print("\nFetching Jeonse Rate Data:")
    jeonse_data = kb.get_jeonse_rate()
    
    if jeonse_data['success']:
        print(f"  ✓ Success: Retrieved {jeonse_data.get('count', 0)} records")
    else:
        print(f"  ✗ Failed: {jeonse_data.get('message', 'Unknown error')}")
    
    return kb

def test_kbland_selenium():
    """Test KB Land with Selenium for dynamic content"""
    print("\n" + "="*60)
    print("Testing KB Land Connector (Selenium Mode)")
    print("="*60)
    
    try:
        # Initialize connector with Selenium
        kb = KBLandConnector(use_selenium=True)
        
        # Test fetching market trends
        print("\nFetching Market Trends (Dynamic Content):")
        trends_data = kb.get_market_trends()
        
        if trends_data['success']:
            print(f"  ✓ Success: Retrieved {trends_data.get('count', 0)} records")
            if trends_data['data']:
                print(f"  Data preview: {trends_data['data'][:2]}")
        else:
            print(f"  ✗ Failed: {trends_data.get('message', 'Unknown error')}")
        
        # Close driver
        kb._close_driver()
        
        return kb
        
    except Exception as e:
        print(f"  ✗ Selenium test failed: {e}")
        print("  Note: Selenium requires Chrome/Chromium to be installed")
        return None

def test_crawl_all():
    """Test crawling all categories"""
    print("\n" + "="*60)
    print("Crawling All KB Land Categories")
    print("="*60)
    
    kb = KBLandConnector(use_selenium=False)
    
    # Crawl all categories
    all_data = kb.crawl_all_categories(save_to_csv=True)
    
    # Summary
    print("\nCrawl Summary:")
    success_count = sum(1 for d in all_data.values() if d['success'])
    total_records = sum(d.get('count', 0) for d in all_data.values() if d['success'])
    
    print(f"  Categories crawled: {len(all_data)}")
    print(f"  Successful: {success_count}")
    print(f"  Total records: {total_records}")
    
    # Save summary
    summary_path = Path('data_exports') / 'kbland_summary.json'
    summary_path.parent.mkdir(exist_ok=True)
    
    summary = {
        'categories': len(all_data),
        'successful': success_count,
        'total_records': total_records,
        'details': {
            k: {
                'success': v['success'],
                'count': v.get('count', 0),
                'dataset': v.get('dataset', '')
            }
            for k, v in all_data.items()
        }
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n  Summary saved to: {summary_path}")
    
    return all_data

def main():
    """Main test function"""
    print("\n" + "="*80)
    print(" KB Land Web Scraper Test")
    print("="*80)
    
    # Test 1: Basic functionality
    kb_basic = test_kbland_basic()
    
    # Test 2: Selenium mode (optional)
    # Uncomment to test Selenium mode (requires Chrome)
    # kb_selenium = test_kbland_selenium()
    
    # Test 3: Crawl all categories
    # Uncomment to crawl all data
    # all_data = test_crawl_all()
    
    print("\n" + "="*60)
    print("Test Complete")
    print("="*60)
    print("\nKB Land connector is ready to use!")
    print("\nUsage example:")
    print("```python")
    print("from connectors import KBLandConnector")
    print("kb = KBLandConnector()")
    print("price_data = kb.get_apartment_price_index('seoul')")
    print("```")

if __name__ == "__main__":
    main()