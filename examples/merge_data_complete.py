"""
Complete and proper merge of Korean macro data
Fixes all data availability and coverage issues
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
        return pd.to_datetime(date_str, format='%Y.%m')
    elif len(date_str) == 8:
        return pd.to_datetime(date_str, format='%Y%m%d')
    elif len(date_str) == 6:
        return pd.to_datetime(date_str, format='%Y%m')
    else:
        return pd.to_datetime(date_str, errors='coerce')

def load_kb_land_data():
    """Load KB Land Excel data if available"""
    kb_data = {}
    kb_files = {
        'housing_price': 'data_exports/kb_land/KB주택가격지수_20250819.xlsx',
        'jeonse_price': 'data_exports/kb_land/KB전세가격지수_20250819.xlsx',
        'monthly_rent': 'data_exports/kb_land/KB월세가격지수_20250819.xlsx',
        'transaction_volume': 'data_exports/kb_land/부동산거래량_20250819.xlsx',
        'market_sentiment': 'data_exports/kb_land/시장심리지수_20250819.xlsx'
    }
    
    for name, filepath in kb_files.items():
        if Path(filepath).exists():
            try:
                # Try different Excel engines
                try:
                    df = pd.read_excel(filepath, engine='openpyxl')
                except:
                    try:
                        df = pd.read_excel(filepath, engine='xlrd')
                    except:
                        print(f"  ✗ Cannot read {name} Excel file")
                        continue
                
                # Find date column
                date_cols = [col for col in df.columns if '날짜' in str(col) or '시점' in str(col) or 'date' in col.lower()]
                if date_cols:
                    df['date'] = pd.to_datetime(df[date_cols[0]], errors='coerce')
                else:
                    # Try first column as date
                    df['date'] = pd.to_datetime(df.iloc[:, 0], errors='coerce')
                
                # Find value columns - look for numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    # Use the first numeric column as value
                    df['value'] = df[numeric_cols[0]]
                    
                    # Keep only valid data
                    result = df[['date', 'value']].dropna()
                    result = result.rename(columns={'value': f'kb_{name}_value'})
                    
                    # Convert to monthly if needed
                    result = result.set_index('date')
                    result = result.resample('M').mean().reset_index()
                    result['date'] = result['date'].dt.to_period('M').dt.to_timestamp()
                    
                    kb_data[name] = result
                    print(f"  ✓ KB {name}: {len(result)} monthly records")
                else:
                    print(f"  ✗ KB {name}: No numeric data found")
                    
            except Exception as e:
                print(f"  ✗ KB {name} error: {e}")
    
    return kb_data

def main():
    print("="*80)
    print("COMPLETE KOREAN MACRO DATA MERGE")
    print("Fixing all data availability and coverage issues")
    print("="*80)
    
    all_data = {}
    
    # 1. Load BOK data (all available from 2010)
    print("\n1. Loading BOK Data...")
    print("-"*40)
    
    bok_files = {
        'base_rate': 'bok_data_final/bok_base_rate.csv',
        'usd_krw': 'bok_data_final/bok_usd_krw_exchange_rate.csv',
        'eur_krw': 'bok_data_final/bok_eur_krw_exchange_rate.csv',
        'cny_krw': 'bok_data_final/bok_cny_krw_exchange_rate.csv'  # Note: starts 2016
    }
    
    for name, filepath in bok_files.items():
        if Path(filepath).exists():
            try:
                df = pd.read_csv(filepath, encoding='utf-8-sig')
                
                # Parse date
                if 'TIME' in df.columns:
                    df['date'] = df['TIME'].apply(parse_bok_date)
                
                # Get value
                if 'DATA_VALUE' in df.columns:
                    df['value'] = pd.to_numeric(df['DATA_VALUE'], errors='coerce')
                
                # Keep only date and value
                result = df[['date', 'value']].dropna()
                
                # Aggregate to monthly
                result = result.set_index('date')
                monthly = result.resample('M').mean().reset_index()
                monthly['date'] = monthly['date'].dt.to_period('M').dt.to_timestamp()
                monthly = monthly.rename(columns={'value': f'{name}_value'})
                
                all_data[name] = monthly
                
                # Check actual date range
                date_range = f"{monthly['date'].min().strftime('%Y-%m')} to {monthly['date'].max().strftime('%Y-%m')}"
                print(f"  ✓ {name}: {len(monthly)} months ({date_range})")
                
            except Exception as e:
                print(f"  ✗ Error loading {name}: {e}")
    
    # 2. Load FRED data
    print("\n2. Loading FRED Data...")
    print("-"*40)
    
    fred_files = {
        'fed_rate': 'research_data_fixed/fred_us_federal_funds_rate.csv',
        'us_10y': 'research_data_fixed/fred_us_10-year_treasury.csv',
        'vix': 'research_data_fixed/fred_vix_index.csv',
        'us_gdp': 'research_data_fixed/fred_us_gdp_growth.csv',  # Quarterly
        'wti_oil': 'research_data_fixed/fred_wti_oil_price.csv',
        'brent_oil': 'research_data_fixed/fred_brent_oil_price.csv',
        'dxy': 'research_data_fixed/fred_dxy_dollar_index.csv',
        'china_gdp': 'research_data_fixed/fred_china_gdp.csv'  # Annual
    }
    
    for name, filepath in fred_files.items():
        if Path(filepath).exists():
            try:
                df = pd.read_csv(filepath)
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                
                # Handle different frequencies
                result = df[['date', 'value']].dropna()
                
                # Check frequency
                date_diff = (result['date'].iloc[-1] - result['date'].iloc[0]).days / len(result)
                
                if date_diff > 60:  # Quarterly or annual data
                    # For quarterly/annual, forward fill to monthly
                    result = result.set_index('date')
                    # Resample to monthly start first
                    monthly = result.resample('MS').first()
                    # Forward fill the missing months
                    monthly = monthly.fillna(method='ffill')
                    monthly = monthly.reset_index()
                    monthly['date'] = monthly['date'].dt.to_period('M').dt.to_timestamp()
                    freq_note = "quarterly/annual → monthly (forward filled)"
                else:
                    # Daily data - aggregate to monthly
                    result = result.set_index('date')
                    monthly = result.resample('M').mean().reset_index()
                    monthly['date'] = monthly['date'].dt.to_period('M').dt.to_timestamp()
                    freq_note = "daily → monthly average"
                
                monthly = monthly.rename(columns={'value': f'{name}_value'})
                all_data[name] = monthly
                
                date_range = f"{monthly['date'].min().strftime('%Y-%m')} to {monthly['date'].max().strftime('%Y-%m')}"
                print(f"  ✓ {name}: {len(monthly)} months ({date_range}) [{freq_note}]")
                
            except Exception as e:
                print(f"  ✗ Error loading {name}: {e}")
    
    # 3. Load KOSIS data
    print("\n3. Loading KOSIS Data...")
    print("-"*40)
    
    # Employment data (monthly)
    if Path('research_data_fixed/kosis_DT_1DA7001.csv').exists():
        try:
            df = pd.read_csv('research_data_fixed/kosis_DT_1DA7001.csv', encoding='utf-8-sig')
            
            # Parse KOSIS date (YYYYMM format)
            df['date'] = pd.to_datetime(df['PRD_DE'].astype(str), format='%Y%m')
            df['value'] = pd.to_numeric(df['DT'], errors='coerce')
            
            # Group by date (in case of multiple categories)
            monthly = df.groupby('date')['value'].mean().reset_index()
            monthly['date'] = monthly['date'].dt.to_period('M').dt.to_timestamp()
            monthly = monthly.rename(columns={'value': 'employment_value'})
            
            all_data['employment'] = monthly
            
            date_range = f"{monthly['date'].min().strftime('%Y-%m')} to {monthly['date'].max().strftime('%Y-%m')}"
            print(f"  ✓ employment: {len(monthly)} months ({date_range})")
        except Exception as e:
            print(f"  ✗ Error loading employment: {e}")
    
    # Demographics data (annual)
    if Path('research_data_fixed/kosis_DT_1B8000F.csv').exists():
        try:
            df = pd.read_csv('research_data_fixed/kosis_DT_1B8000F.csv', encoding='utf-8-sig')
            
            # This is annual data - PRD_DE is just year
            df['year'] = pd.to_numeric(df['PRD_DE'], errors='coerce')
            df['date'] = pd.to_datetime(df['year'].astype(str) + '-01-01')
            df['value'] = pd.to_numeric(df['DT'], errors='coerce')
            
            # Group by date
            annual = df.groupby('date')['value'].mean().reset_index()
            
            # Forward fill to monthly
            annual = annual.set_index('date')
            monthly = annual.resample('MS').first().fillna(method='ffill').reset_index()
            monthly['date'] = monthly['date'].dt.to_period('M').dt.to_timestamp()
            monthly = monthly.rename(columns={'value': 'demographics_value'})
            
            all_data['demographics'] = monthly
            
            date_range = f"{monthly['date'].min().strftime('%Y-%m')} to {monthly['date'].max().strftime('%Y-%m')}"
            print(f"  ✓ demographics: {len(monthly)} months ({date_range}) [annual → monthly]")
        except Exception as e:
            print(f"  ✗ Error loading demographics: {e}")
    
    # 4. Try to load KB Land data
    print("\n4. Loading KB Land Data...")
    print("-"*40)
    kb_data = load_kb_land_data()
    all_data.update(kb_data)
    
    # 5. Merge all data
    print("\n5. Merging All Data...")
    print("-"*40)
    
    if all_data:
        # Find the common date range
        min_dates = []
        max_dates = []
        for name, df in all_data.items():
            min_dates.append(df['date'].min())
            max_dates.append(df['date'].max())
        
        # Use 2010-01 to 2024-12 as our target range
        start_date = pd.Timestamp('2010-01-01')
        end_date = pd.Timestamp('2024-12-01')
        
        # Create a complete date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        merged = pd.DataFrame({'date': date_range})
        
        # Merge each dataset
        for name, df in all_data.items():
            merged = pd.merge(merged, df, on='date', how='left')
        
        # Add time features
        merged['year'] = merged['date'].dt.year
        merged['month'] = merged['date'].dt.month
        merged['quarter'] = merged['date'].dt.quarter
        
        # Calculate percentage changes for all value columns
        value_cols = [col for col in merged.columns if col.endswith('_value')]
        for col in value_cols:
            if merged[col].notna().sum() > 12:  # Only if we have enough data
                merged[f'{col}_pct_change'] = merged[col].pct_change() * 100
                merged[f'{col}_yoy'] = merged[col].pct_change(12) * 100
        
        # Save the complete merged data
        output_file = 'korean_macro_complete.csv'
        merged.to_csv(output_file, index=False)
        
        print(f"\n✅ Successfully merged {len(all_data)} datasets")
        print(f"Output shape: {merged.shape}")
        print(f"Date range: {merged['date'].min()} to {merged['date'].max()}")
        print(f"Saved to: {output_file}")
        
        # Display comprehensive coverage summary
        print("\n6. Data Coverage Summary")
        print("-"*40)
        print(f"{'Indicator':<25} {'Start':<10} {'End':<10} {'Coverage':<10} {'Missing'}")
        print("-"*70)
        
        for col in value_cols:
            non_null = merged[col].notna()
            if non_null.sum() > 0:
                first_valid = merged.loc[non_null.idxmax(), 'date'].strftime('%Y-%m')
                last_valid = merged.loc[non_null[::-1].idxmax(), 'date'].strftime('%Y-%m')
                coverage = (non_null.sum() / len(merged)) * 100
                missing = len(merged) - non_null.sum()
                
                indicator_name = col.replace('_value', '').replace('_', ' ').title()
                print(f"{indicator_name:<25} {first_valid:<10} {last_valid:<10} {coverage:>6.1f}%    {missing:>3}")
        
        # Show sample of complete data
        print("\n7. Sample of Complete Data (2020-01)")
        print("-"*40)
        sample_date = pd.Timestamp('2020-01-01')
        sample_row = merged[merged['date'] == sample_date]
        
        if not sample_row.empty:
            print(f"Date: {sample_date.strftime('%Y-%m')}")
            for col in value_cols[:10]:  # Show first 10 indicators
                val = sample_row[col].values[0]
                indicator_name = col.replace('_value', '').replace('_', ' ').title()
                if pd.notna(val):
                    print(f"  {indicator_name:<20}: {val:>10.2f}")
                else:
                    print(f"  {indicator_name:<20}: {'N/A':>10}")
        
        return merged
    else:
        print("No data loaded successfully")
        return None

if __name__ == "__main__":
    merged_data = main()
    
    # Automatically run integrity check after merging
    if merged_data is not None:
        print("\n" + "="*80)
        print("RUNNING AUTOMATIC INTEGRITY CHECK")
        print("="*80)
        
        from data_integrity_checker import DataIntegrityChecker
        checker = DataIntegrityChecker()
        checker.check_merge_integrity('korean_macro_complete.csv')
        
        # Check if any critical issues were found
        if checker.issues:
            print("\n⚠️ WARNING: Integrity issues detected in merged data!")
            print("Please review the data_integrity_report.txt for details.")
        else:
            print("\n✅ SUCCESS: All integrity checks passed!")
            print("The merged data is ready for analysis.")