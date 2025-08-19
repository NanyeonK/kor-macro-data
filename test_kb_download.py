"""Test KB Land data download functionality"""

from connectors.kbland_enhanced import KBLandEnhancedConnector
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_download():
    """Test downloading KB Land data"""
    
    print("="*80)
    print("Testing KB Land Data Download")
    print("="*80)
    
    # Initialize connector
    kb = KBLandEnhancedConnector()
    
    # Test downloading a single dataset (without Selenium first)
    print("\n1. Testing direct download (without Selenium):")
    print("-"*40)
    
    test_dataset = 'price_index'
    print(f"Attempting to download: {kb.KB_DATA_CATALOG[test_dataset]['name']}")
    
    success, result = kb.download_dataset(test_dataset)
    
    if success:
        print(f"✓ Success! Downloaded to: {result}")
    else:
        print(f"✗ Failed: {result}")
        print("Note: Direct download may not work - KB Land may require browser access")
    
    # Display catalog info
    print("\n2. Available datasets for download:")
    print("-"*40)
    
    catalog = kb.get_catalog()
    print(catalog[['ID', 'Name', 'Format', 'Frequency']].to_string())
    
    print("\n" + "="*80)
    print("Summary")
    print("="*80)
    print(f"Total datasets available: {len(kb.KB_DATA_CATALOG)}")
    print("Formats: Excel, CSV, PDF")
    print("Download directory: data_exports/kb_land/")
    
    print("\nTo download all datasets with Selenium:")
    print("```python")
    print("kb = KBLandEnhancedConnector()")
    print("kb.init_driver()  # Initialize Selenium")
    print("results = kb.download_all_datasets()")
    print("```")
    
    # Close driver if initialized
    kb.close_driver()

if __name__ == "__main__":
    test_download()