"""
Example: Merge Korean Macro Data for Real Estate Research
Demonstrates merging BOK, KB Land, FRED, and KOSIS data with English columns
"""

import pandas as pd
from pathlib import Path
from kor_macro.data_merger import KoreanMacroDataMerger
import warnings
warnings.filterwarnings('ignore')

def main():
    print("Korean Real Estate Market Research - Data Merging Example")
    print("="*80)
    
    # Initialize merger
    merger = KoreanMacroDataMerger()
    
    # 1. Load BOK data (interest rates and exchange rates)
    print("\n1. Loading BOK Data...")
    print("-"*40)
    
    bok_files = [
        'bok_data_final/bok_base_rate.csv',
        'bok_data_final/bok_usd_krw_exchange_rate.csv',
        'bok_data_final/bok_eur_krw_exchange_rate.csv',
        'bok_data_final/bok_cny_krw_exchange_rate.csv'
    ]
    
    for file in bok_files:
        if Path(file).exists():
            name = Path(file).stem.replace('bok_', '')
            try:
                df = merger.load_data(file, name, source='bok')
                print(f"✓ Loaded {name}: {len(df)} records")
            except Exception as e:
                print(f"✗ Error loading {name}: {e}")
    
    # 2. Load KB Land real estate data
    print("\n2. Loading KB Land Data...")
    print("-"*40)
    
    kb_files = [
        'data_exports/kb_land/KB주택가격지수_20250819.xlsx',
        'data_exports/kb_land/KB전세가격지수_20250819.xlsx',
        'data_exports/kb_land/KB월세가격지수_20250819.xlsx',
        'data_exports/kb_land/부동산거래량_20250819.xlsx',
        'data_exports/kb_land/시장심리지수_20250819.xlsx'
    ]
    
    kb_names = ['housing_price', 'jeonse_price', 'monthly_rent', 'transaction_volume', 'market_sentiment']
    
    for file, name in zip(kb_files, kb_names):
        if Path(file).exists():
            try:
                df = merger.load_data(file, name, source='kb')
                print(f"✓ Loaded {name}: {len(df)} records")
            except Exception as e:
                print(f"✗ Error loading {name}: {e}")
    
    # 3. Load FRED global economic data
    print("\n3. Loading FRED Data...")
    print("-"*40)
    
    fred_files = [
        'research_data_fixed/fred_us_federal_funds_rate.csv',
        'research_data_fixed/fred_us_10-year_treasury.csv',
        'research_data_fixed/fred_vix_index.csv',
        'research_data_fixed/fred_us_gdp_growth.csv',
        'research_data_fixed/fred_wti_oil_price.csv'
    ]
    
    fred_names = ['fed_rate', 'us_10y_treasury', 'vix', 'us_gdp', 'oil_price']
    
    for file, name in zip(fred_files, fred_names):
        if Path(file).exists():
            try:
                df = merger.load_data(file, name, source='fred')
                print(f"✓ Loaded {name}: {len(df)} records")
            except Exception as e:
                print(f"✗ Error loading {name}: {e}")
    
    # 4. Get data summary
    print("\n4. Data Summary")
    print("-"*40)
    summary = merger.get_data_summary()
    print(summary.to_string())
    
    # 5. Create merged datasets with different frequencies
    print("\n5. Creating Merged Datasets...")
    print("-"*40)
    
    # Monthly aggregation (most common for economic analysis)
    print("\nCreating MONTHLY aggregated dataset...")
    try:
        monthly_data = merger.create_research_dataset(
            freq='M',
            start_date='2010-01-01',
            end_date='2024-12-31'
        )
        merger.save_merged_data('merged_data_monthly.csv', format='csv')
        print(f"✓ Monthly data: {monthly_data.shape[0]} rows, {monthly_data.shape[1]} columns")
        print(f"  Date range: {monthly_data['date'].min()} to {monthly_data['date'].max()}")
        
        # Show sample columns
        print("\n  Sample columns (first 20):")
        for col in monthly_data.columns[:20]:
            print(f"    - {col}")
    except Exception as e:
        print(f"✗ Error creating monthly dataset: {e}")
    
    # Quarterly aggregation (for GDP and other quarterly indicators)
    print("\nCreating QUARTERLY aggregated dataset...")
    try:
        quarterly_data = merger.create_research_dataset(
            freq='Q',
            start_date='2010-01-01',
            end_date='2024-12-31'
        )
        merger.save_merged_data('merged_data_quarterly.csv', format='csv')
        print(f"✓ Quarterly data: {quarterly_data.shape[0]} rows, {quarterly_data.shape[1]} columns")
    except Exception as e:
        print(f"✗ Error creating quarterly dataset: {e}")
    
    # Yearly aggregation (for long-term trends)
    print("\nCreating YEARLY aggregated dataset...")
    try:
        yearly_data = merger.create_research_dataset(
            freq='Y',
            start_date='2010-01-01',
            end_date='2024-12-31'
        )
        merger.save_merged_data('merged_data_yearly.csv', format='csv')
        print(f"✓ Yearly data: {yearly_data.shape[0]} rows, {yearly_data.shape[1]} columns")
    except Exception as e:
        print(f"✗ Error creating yearly dataset: {e}")
    
    # 6. Example: Correlation analysis
    print("\n6. Sample Analysis - Correlations")
    print("-"*40)
    
    if 'monthly_data' in locals():
        # Select numeric columns for correlation
        numeric_cols = monthly_data.select_dtypes(include=['float64', 'int64']).columns
        value_cols = [col for col in numeric_cols if 'value' in col or 'index' in col]
        
        if len(value_cols) > 1:
            correlations = monthly_data[value_cols].corr()
            print("\nTop correlations with housing prices:")
            if 'value_housing_price' in correlations.columns:
                housing_corr = correlations['value_housing_price'].sort_values(ascending=False)
                for idx, (col, corr) in enumerate(housing_corr.items()):
                    if idx < 10 and col != 'value_housing_price':
                        print(f"  {col}: {corr:.3f}")
    
    print("\n" + "="*80)
    print("✅ Data merging complete!")
    print("\nOutput files created:")
    print("  - merged_data_monthly.csv")
    print("  - merged_data_quarterly.csv") 
    print("  - merged_data_yearly.csv")
    
    return merger

if __name__ == "__main__":
    merger = main()