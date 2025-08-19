"""
Properly merge Korean macro data with correct date handling
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def parse_bok_date(date_str):
    """Parse BOK date format (YYYYMMDD or YYYY.MM)"""
    date_str = str(date_str)
    if '.' in date_str:
        # Format: 2024.01
        return pd.to_datetime(date_str, format='%Y.%m')
    elif len(date_str) == 8:
        # Format: 20240101
        return pd.to_datetime(date_str, format='%Y%m%d')
    elif len(date_str) == 6:
        # Format: 202401
        return pd.to_datetime(date_str, format='%Y%m')
    else:
        return pd.to_datetime(date_str, errors='coerce')

def load_and_prepare_bok_data(filepath, indicator_name):
    """Load BOK data and prepare for merging"""
    df = pd.read_csv(filepath, encoding='utf-8-sig')
    
    # Parse BOK date
    if 'TIME' in df.columns:
        df['date'] = df['TIME'].apply(parse_bok_date)
    elif 'time' in df.columns:
        df['date'] = df['time'].apply(parse_bok_date)
    
    # Get value column
    if 'DATA_VALUE' in df.columns:
        df['value'] = pd.to_numeric(df['DATA_VALUE'], errors='coerce')
    elif 'data_value' in df.columns:
        df['value'] = pd.to_numeric(df['data_value'], errors='coerce')
    
    # Keep only date and value
    result = df[['date', 'value']].copy()
    result = result.dropna(subset=['date'])
    result = result.rename(columns={'value': f'{indicator_name}_value'})
    
    return result

def load_and_prepare_fred_data(filepath, indicator_name):
    """Load FRED data and prepare for merging"""
    df = pd.read_csv(filepath)
    
    # Parse date
    df['date'] = pd.to_datetime(df['date'])
    
    # Get value column - handle the '.' values in FRED data
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # Keep only date and value
    result = df[['date', 'value']].copy()
    result = result.dropna(subset=['date'])
    result = result.rename(columns={'value': f'{indicator_name}_value'})
    
    return result

def aggregate_to_monthly(df, value_col, agg_func='mean'):
    """Aggregate daily data to monthly"""
    df = df.copy()
    df = df.set_index('date')
    
    # Resample to monthly
    if agg_func == 'mean':
        monthly = df.resample('M')[value_col].mean()
    elif agg_func == 'sum':
        monthly = df.resample('M')[value_col].sum()
    elif agg_func == 'last':
        monthly = df.resample('M')[value_col].last()
    else:
        monthly = df.resample('M')[value_col].mean()
    
    monthly = monthly.reset_index()
    monthly['date'] = monthly['date'].dt.to_period('M').dt.to_timestamp()
    
    return monthly

def main():
    print("="*80)
    print("PROPERLY MERGING KOREAN MACRO DATA")
    print("="*80)
    
    all_data = []
    
    # 1. Load BOK data
    print("\n1. Loading BOK Data...")
    print("-"*40)
    
    bok_files = {
        'base_rate': 'bok_data_final/bok_base_rate.csv',
        'usd_krw': 'bok_data_final/bok_usd_krw_exchange_rate.csv',
        'eur_krw': 'bok_data_final/bok_eur_krw_exchange_rate.csv',
        'cny_krw': 'bok_data_final/bok_cny_krw_exchange_rate.csv'
    }
    
    for name, filepath in bok_files.items():
        if Path(filepath).exists():
            try:
                df = load_and_prepare_bok_data(filepath, name)
                
                # Aggregate to monthly (BOK data is daily)
                monthly = aggregate_to_monthly(df, f'{name}_value', 'mean')
                all_data.append(monthly)
                
                print(f"✓ {name}: {len(df)} daily → {len(monthly)} monthly records")
            except Exception as e:
                print(f"✗ Error loading {name}: {e}")
    
    # 2. Load FRED data
    print("\n2. Loading FRED Data...")
    print("-"*40)
    
    fred_files = {
        'fed_rate': 'research_data_fixed/fred_us_federal_funds_rate.csv',
        'us_10y': 'research_data_fixed/fred_us_10-year_treasury.csv',
        'vix': 'research_data_fixed/fred_vix_index.csv',
        'us_gdp': 'research_data_fixed/fred_us_gdp_growth.csv',
        'wti_oil': 'research_data_fixed/fred_wti_oil_price.csv',
        'brent_oil': 'research_data_fixed/fred_brent_oil_price.csv'
    }
    
    for name, filepath in fred_files.items():
        if Path(filepath).exists():
            try:
                df = load_and_prepare_fred_data(filepath, name)
                
                # Check if aggregation needed
                if len(df) > 200:  # Likely daily data
                    monthly = aggregate_to_monthly(df, f'{name}_value', 'mean')
                    print(f"✓ {name}: {len(df)} daily → {len(monthly)} monthly records")
                else:
                    monthly = df.copy()
                    monthly['date'] = pd.to_datetime(monthly['date'])
                    # Convert to month start for consistency
                    monthly['date'] = monthly['date'].dt.to_period('M').dt.to_timestamp()
                    print(f"✓ {name}: {len(monthly)} monthly/quarterly records")
                
                all_data.append(monthly)
            except Exception as e:
                print(f"✗ Error loading {name}: {e}")
    
    # 3. Load KOSIS data
    print("\n3. Loading KOSIS Data...")
    print("-"*40)
    
    kosis_files = {
        'employment': 'research_data_fixed/kosis_DT_1DA7001.csv',
        'demographics': 'research_data_fixed/kosis_DT_1B8000F.csv'
    }
    
    for name, filepath in kosis_files.items():
        if Path(filepath).exists():
            try:
                df = pd.read_csv(filepath, encoding='utf-8-sig')
                
                # KOSIS date format
                if 'PRD_DE' in df.columns:
                    df['date'] = pd.to_datetime(df['PRD_DE'], format='%Y%m', errors='coerce')
                elif 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')
                
                # Get value
                if 'DT' in df.columns:
                    df['value'] = pd.to_numeric(df['DT'], errors='coerce')
                elif 'value' in df.columns:
                    df['value'] = pd.to_numeric(df['value'], errors='coerce')
                
                # Aggregate if multiple regions
                monthly = df.groupby('date')['value'].mean().reset_index()
                monthly = monthly.rename(columns={'value': f'{name}_value'})
                monthly['date'] = monthly['date'].dt.to_period('M').dt.to_timestamp()
                
                all_data.append(monthly)
                print(f"✓ {name}: {len(monthly)} monthly records")
            except Exception as e:
                print(f"✗ Error loading {name}: {e}")
    
    # 4. Merge all data
    print("\n4. Merging All Data...")
    print("-"*40)
    
    if all_data:
        # Start with the first dataset
        merged = all_data[0]
        
        # Merge remaining datasets
        for df in all_data[1:]:
            merged = pd.merge(merged, df, on='date', how='outer')
        
        # Sort by date
        merged = merged.sort_values('date')
        
        # Filter to 2010-2024
        merged = merged[(merged['date'] >= '2010-01-01') & (merged['date'] <= '2024-12-31')]
        
        # Add derived features
        merged['year'] = merged['date'].dt.year
        merged['month'] = merged['date'].dt.month
        merged['quarter'] = merged['date'].dt.quarter
        
        # Calculate percentage changes
        for col in merged.columns:
            if col.endswith('_value'):
                merged[f'{col}_pct_change'] = merged[col].pct_change() * 100
                merged[f'{col}_yoy'] = merged[col].pct_change(12) * 100
        
        # Save the properly merged data
        output_file = 'korean_macro_merged_properly.csv'
        merged.to_csv(output_file, index=False)
        
        print(f"\n✅ Successfully merged {len(all_data)} datasets")
        print(f"Output shape: {merged.shape}")
        print(f"Date range: {merged['date'].min()} to {merged['date'].max()}")
        print(f"Saved to: {output_file}")
        
        # Display summary statistics
        print("\n5. Data Summary")
        print("-"*40)
        value_cols = [col for col in merged.columns if col.endswith('_value')]
        
        print(f"Available indicators: {len(value_cols)}")
        for col in value_cols:
            non_null = merged[col].notna().sum()
            coverage = (non_null / len(merged)) * 100
            print(f"  - {col}: {non_null} observations ({coverage:.1f}% coverage)")
        
        # Sample of merged data
        print("\n6. Sample of Merged Data (first 5 rows)")
        print("-"*40)
        print(merged[['date'] + value_cols[:5]].head())
        
        return merged
    else:
        print("No data loaded successfully")
        return None

if __name__ == "__main__":
    merged_data = main()