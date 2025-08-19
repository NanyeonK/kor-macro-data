#!/usr/bin/env python3
"""
Quick Start Guide for Korean Macro Data Package

This script demonstrates the basic usage of the package.
"""

from kor_macro import KoreanMacroDataMerger
import os

def main():
    """Main function demonstrating package usage."""
    
    print("=" * 60)
    print("Korean Macro Data Package - Quick Start")
    print("=" * 60)
    
    # Check for API keys
    if not os.getenv('BOK_API_KEY'):
        print("\n⚠️ Warning: BOK_API_KEY not found in environment.")
        print("Please set your API keys in .env file")
        print("See .env.example for template")
    
    # Initialize the merger
    merger = KoreanMacroDataMerger()
    print("\n✅ Data merger initialized")
    
    # Example: Load some data files if they exist
    data_files = {
        'base_rate': 'bok_data_final/bok_base_rate.csv',
        'usd_krw': 'bok_data_final/bok_usd_krw_exchange_rate.csv',
    }
    
    loaded_count = 0
    for name, filepath in data_files.items():
        if os.path.exists(filepath):
            try:
                merger.load_data(filepath, name, source='bok')
                print(f"  ✓ Loaded {name}")
                loaded_count += 1
            except Exception as e:
                print(f"  ✗ Error loading {name}: {e}")
    
    if loaded_count > 0:
        print(f"\n✅ Successfully loaded {loaded_count} datasets")
        
        # Create merged dataset
        print("\nCreating merged dataset...")
        try:
            merged = merger.create_research_dataset(freq='M')
            print(f"✅ Created merged dataset: {merged.shape[0]} rows × {merged.shape[1]} columns")
            
            # Save with integrity check
            print("\nSaving with integrity validation...")
            result = merger.save_merged_data('quick_start_output.csv')
            
            if result:
                print("✅ Data saved and validated successfully!")
            else:
                print("⚠️ Data saved but validation found issues")
                
        except Exception as e:
            print(f"❌ Error creating dataset: {e}")
    else:
        print("\n📝 To get started:")
        print("1. Set your API keys in .env file")
        print("2. Run data collection scripts from scripts/data_collection/")
        print("3. Use the merger to combine and analyze data")
        print("\nSee examples/ directory for more usage examples")

if __name__ == "__main__":
    main()