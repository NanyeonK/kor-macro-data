"""
Example script demonstrating automatic integrity checking during data merging
"""

from kor_macro.data_merger import KoreanMacroDataMerger
import pandas as pd

def main():
    """
    Demonstrate the automatic integrity checking feature
    """
    print("=" * 80)
    print("KOREAN MACRO DATA MERGER WITH AUTOMATIC INTEGRITY CHECKING")
    print("=" * 80)
    
    # Initialize the merger
    merger = KoreanMacroDataMerger()
    
    # Load some sample data
    print("\n1. Loading data sources...")
    print("-" * 40)
    
    # Load BOK data
    merger.load_data('bok_data_final/bok_base_rate.csv', 'base_rate', source='bok')
    merger.load_data('bok_data_final/bok_usd_krw_exchange_rate.csv', 'usd_krw', source='bok')
    
    # Load FRED data
    merger.load_data('research_data_fixed/fred_us_federal_funds_rate.csv', 'fed_rate', source='fred')
    merger.load_data('research_data_fixed/fred_vix_index.csv', 'vix', source='fred')
    
    print(f"✅ Loaded {len(merger.datasets)} datasets")
    
    # Create merged dataset
    print("\n2. Creating merged dataset...")
    print("-" * 40)
    
    merged_data = merger.create_research_dataset(
        freq='M',  # Monthly aggregation
        start_date='2020-01-01',
        end_date='2024-12-31'
    )
    
    print(f"✅ Created merged dataset: {merged_data.shape[0]} rows × {merged_data.shape[1]} columns")
    
    # Save with automatic integrity check (default behavior)
    print("\n3. Saving data with automatic integrity check...")
    print("-" * 40)
    
    integrity_result = merger.save_merged_data(
        'example_merged_with_check.csv',
        format='csv',
        run_integrity_check=True  # This is True by default
    )
    
    # Report results
    print("\n" + "=" * 80)
    print("FINAL STATUS")
    print("=" * 80)
    
    if integrity_result is True:
        print("✅ SUCCESS: Data merged and validated successfully!")
        print("   - All dates properly aligned")
        print("   - No temporal shifts detected")
        print("   - Values correctly mapped")
        print("   - Ready for econometric analysis")
    elif integrity_result is False:
        print("⚠️ WARNING: Data merged but integrity issues detected!")
        print("   Please review data_integrity_report.txt for details")
    else:
        print("ℹ️ INFO: Data merged successfully (integrity check not performed)")
    
    # Demonstrate disabling integrity check
    print("\n4. Example: Saving without integrity check...")
    print("-" * 40)
    
    merger.save_merged_data(
        'example_merged_no_check.csv',
        format='csv',
        run_integrity_check=False  # Explicitly disable check
    )
    print("✅ Saved without integrity check (faster for large datasets)")
    
    # Show data preview
    print("\n5. Data Preview (First 5 rows):")
    print("-" * 40)
    print(merged_data.head())
    
    return merged_data

if __name__ == "__main__":
    merged_data = main()
    
    print("\n" + "=" * 80)
    print("EXAMPLE COMPLETE")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("  1. Integrity checking is enabled by default when saving CSV files")
    print("  2. Use run_integrity_check=False to skip validation (e.g., for performance)")
    print("  3. Check returns True (passed), False (issues), or None (skipped)")
    print("  4. Detailed report saved to data_integrity_report.txt")
    print("\nFiles created:")
    print("  - example_merged_with_check.csv (validated)")
    print("  - example_merged_no_check.csv (not validated)")
    print("  - data_integrity_report.txt (validation details)")