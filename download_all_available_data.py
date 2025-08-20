#!/usr/bin/env python3
"""
Download all available data from BOK and KOSIS using verified working methods
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kor_macro.connectors.bok import BOKConnector
from kor_macro.connectors.kosis import KOSISConnector

# Set up API keys
os.environ['BOK_API_KEY'] = 'XJ9KI67DWCNIL35PBE9W'
os.environ['KOSIS_API_KEY'] = 'YzM0YThjZjUwYjliMTNiNmZhMWZiOTlhNTZkOGIzNTg'

# Date range
START_DATE = '2020-01-01'
END_DATE = '2024-12-31'

def download_bok_data():
    """Download all available BOK data"""
    print("\n" + "="*60)
    print("DOWNLOADING BOK DATA")
    print("="*60)
    
    bok = BOKConnector()
    data = {}
    
    # List of BOK methods to call
    bok_indicators = [
        # Interest Rates
        ('base_rate', lambda: bok.get_base_rate(START_DATE, END_DATE)),
        ('call_rate', lambda: bok.get_call_rate(START_DATE, END_DATE)),
        
        # Exchange Rates
        ('exchange_usd', lambda: bok.get_exchange_rate('USD', START_DATE, END_DATE)),
        ('exchange_eur', lambda: bok.get_exchange_rate('EUR', START_DATE, END_DATE)),
        ('exchange_jpy', lambda: bok.get_exchange_rate('JPY', START_DATE, END_DATE)),
        ('exchange_cny', lambda: bok.get_exchange_rate('CNY', START_DATE, END_DATE)),
        
        # Money Supply
        ('money_m1', lambda: bok.get_money_supply('M1', START_DATE, END_DATE)),
        ('money_m2', lambda: bok.get_money_supply('M2', START_DATE, END_DATE)),
        
        # GDP
        ('gdp_nominal', lambda: bok.get_gdp('nominal', START_DATE, END_DATE)),
        ('gdp_real', lambda: bok.get_gdp('real', START_DATE, END_DATE)),
        
        # Prices
        ('cpi', lambda: bok.get_cpi(START_DATE, END_DATE)),
        ('housing_price_index', lambda: bok.get_housing_price_index(START_DATE, END_DATE)),
        
        # Employment
        ('unemployment_rate', lambda: bok.get_unemployment_rate(START_DATE, END_DATE)),
        ('employment_rate', lambda: bok.get_employment_rate(START_DATE, END_DATE)),
        ('participation_rate', lambda: bok.get_participation_rate(START_DATE, END_DATE)),
        
        # Trade
        ('exports', lambda: bok.get_trade_data('exports', START_DATE, END_DATE)),
        ('imports', lambda: bok.get_trade_data('imports', START_DATE, END_DATE)),
        
        # Stock Market
        ('kospi', lambda: bok.get_kospi(START_DATE, END_DATE)),
        ('kosdaq', lambda: bok.get_kosdaq(START_DATE, END_DATE)),
        
        # Treasury Yields
        ('treasury_3y', lambda: bok.get_treasury_yield('3y', START_DATE, END_DATE)),
        ('treasury_5y', lambda: bok.get_treasury_yield('5y', START_DATE, END_DATE)),
        ('treasury_10y', lambda: bok.get_treasury_yield('10y', START_DATE, END_DATE)),
        
        # Household Debt
        ('household_debt', lambda: bok.get_household_debt(START_DATE, END_DATE)),
        
        # Balance of Payments
        ('current_account', lambda: bok.get_balance_of_payments('current', START_DATE, END_DATE)),
        
        # Foreign Reserves
        ('foreign_reserves', lambda: bok.get_foreign_reserves(START_DATE, END_DATE)),
    ]
    
    # Download each indicator
    for name, method in bok_indicators:
        try:
            print(f"  Downloading {name}...")
            df = method()
            if not df.empty:
                data[name] = df
                print(f"    ✅ {len(df)} rows")
            else:
                print(f"    ⚠️  Empty result")
        except Exception as e:
            print(f"    ❌ Error: {e}")
        time.sleep(0.5)  # Be nice to the API
    
    return data

def download_kosis_data():
    """Download all available KOSIS data"""
    print("\n" + "="*60)
    print("DOWNLOADING KOSIS DATA")
    print("="*60)
    
    kosis = KOSISConnector()
    data = {}
    
    # List of KOSIS methods to call
    kosis_indicators = [
        # Population
        ('population', lambda: kosis.get_population_data(START_DATE, END_DATE)),
        ('birth_statistics', lambda: kosis.get_birth_statistics(START_DATE, END_DATE)),
        ('death_statistics', lambda: kosis.get_death_statistics(START_DATE, END_DATE)),
        ('marriage_statistics', lambda: kosis.get_marriage_statistics(START_DATE, END_DATE)),
        ('migration_data', lambda: kosis.get_migration_data(START_DATE, END_DATE)),
        ('foreign_residents', lambda: kosis.get_foreign_residents(START_DATE, END_DATE)),
        
        # Employment
        ('employment_data', lambda: kosis.get_employment_data(START_DATE, END_DATE)),
        ('unemployment_data', lambda: kosis.get_unemployment_data(START_DATE, END_DATE)),
        ('wage_data', lambda: kosis.get_wage_data(START_DATE, END_DATE)),
        ('working_hours', lambda: kosis.get_working_hours(START_DATE, END_DATE)),
        ('labor_productivity', lambda: kosis.get_labor_productivity(START_DATE, END_DATE)),
        
        # Regional Economy
        ('regional_gdp', lambda: kosis.get_regional_gdp(START_DATE, END_DATE)),
        ('regional_cpi', lambda: kosis.get_regional_cpi(START_DATE, END_DATE)),
        ('regional_employment', lambda: kosis.get_regional_employment(START_DATE, END_DATE)),
        
        # Industry & Business
        ('manufacturing_production', lambda: kosis.get_manufacturing_production(START_DATE, END_DATE)),
        ('service_production', lambda: kosis.get_service_production(START_DATE, END_DATE)),
        ('retail_sales', lambda: kosis.get_retail_sales(START_DATE, END_DATE)),
        ('construction_orders', lambda: kosis.get_construction_orders(START_DATE, END_DATE)),
        ('business_survey', lambda: kosis.get_business_survey(START_DATE, END_DATE)),
        
        # Social Indicators
        ('housing_statistics', lambda: kosis.get_housing_statistics(START_DATE, END_DATE)),
        ('education_statistics', lambda: kosis.get_education_statistics(START_DATE, END_DATE)),
        ('healthcare_statistics', lambda: kosis.get_healthcare_statistics(START_DATE, END_DATE)),
        ('welfare_statistics', lambda: kosis.get_welfare_statistics(START_DATE, END_DATE)),
        ('crime_statistics', lambda: kosis.get_crime_statistics(START_DATE, END_DATE)),
        ('environment_statistics', lambda: kosis.get_environment_statistics(START_DATE, END_DATE)),
    ]
    
    # Download each indicator
    for name, method in kosis_indicators:
        try:
            print(f"  Downloading {name}...")
            df = method()
            if not df.empty:
                data[name] = df
                print(f"    ✅ {len(df)} rows")
            else:
                print(f"    ⚠️  Empty result")
        except Exception as e:
            print(f"    ❌ Error: {e}")
        time.sleep(0.5)  # Be nice to the API
    
    return data

def create_policy_dummy_variables(bok_data):
    """Create policy dummy variables from BOK data"""
    print("\n" + "="*60)
    print("CREATING POLICY VARIABLES")
    print("="*60)
    
    policy_data = {}
    
    # Base rate changes
    if 'base_rate' in bok_data and not bok_data['base_rate'].empty:
        print("  Creating base rate change dummies...")
        df = bok_data['base_rate'].copy()
        df['rate_change'] = df['value'].diff()
        df['rate_increase_dummy'] = (df['rate_change'] > 0).astype(int)
        df['rate_decrease_dummy'] = (df['rate_change'] < 0).astype(int)
        df['rate_change_dummy'] = (df['rate_change'] != 0).astype(int)
        
        # Monetary policy stance
        df['policy_stance'] = 'neutral'
        df.loc[df['rate_change'] > 0, 'policy_stance'] = 'tightening'
        df.loc[df['rate_change'] < 0, 'policy_stance'] = 'easing'
        
        policy_data['monetary_policy'] = df
        print(f"    ✅ Created policy variables")
    
    # Major policy announcement dates (manually coded)
    print("  Creating major policy announcement dummies...")
    announcements = pd.DataFrame({
        'date': pd.to_datetime([
            '2020-03-16',  # COVID emergency rate cut
            '2020-05-28',  # Additional rate cut
            '2020-06-17',  # 6.17 real estate measures
            '2020-07-10',  # 7.10 real estate measures
            '2020-12-16',  # 12.16 real estate measures
            '2021-02-04',  # 2.4 real estate measures
            '2021-08-26',  # 8.26 real estate measures
            '2021-08-26',  # First rate hike
            '2021-11-25',  # Second rate hike
            '2022-01-03',  # Real estate deregulation
            '2022-01-14',  # Rate hike
            '2022-04-14',  # Rate hike
            '2022-05-26',  # Rate hike
            '2022-07-13',  # Rate hike
            '2022-08-25',  # Rate hike
            '2022-10-12',  # Rate hike
            '2022-11-24',  # Rate hike
            '2023-01-13',  # Rate hike
        ]),
        'policy_type': [
            'monetary', 'monetary', 'real_estate', 'real_estate', 'real_estate',
            'real_estate', 'real_estate', 'monetary', 'monetary', 'real_estate',
            'monetary', 'monetary', 'monetary', 'monetary', 'monetary',
            'monetary', 'monetary', 'monetary'
        ],
        'description': [
            'COVID emergency cut', 'Additional cut', '6.17 measures', '7.10 measures',
            '12.16 measures', '2.4 measures', '8.26 measures', 'First hike', 'Second hike',
            'Deregulation', 'Rate hike', 'Rate hike', 'Rate hike', 'Rate hike',
            'Rate hike', 'Rate hike', 'Rate hike', 'Rate hike'
        ]
    })
    
    policy_data['policy_announcements'] = announcements
    print(f"    ✅ Added {len(announcements)} policy announcements")
    
    return policy_data

def save_all_data(all_data):
    """Save all data to CSV files"""
    print("\n" + "="*60)
    print("SAVING DATA TO CSV FILES")
    print("="*60)
    
    output_dir = 'data_downloads'
    os.makedirs(output_dir, exist_ok=True)
    
    saved_files = []
    
    # Save BOK data
    if 'bok' in all_data:
        for name, df in all_data['bok'].items():
            if not df.empty:
                filename = f"{output_dir}/bok_{name}.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                saved_files.append(filename)
                print(f"  ✅ Saved {filename} ({len(df)} rows)")
    
    # Save KOSIS data
    if 'kosis' in all_data:
        for name, df in all_data['kosis'].items():
            if not df.empty:
                filename = f"{output_dir}/kosis_{name}.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                saved_files.append(filename)
                print(f"  ✅ Saved {filename} ({len(df)} rows)")
    
    # Save policy data
    if 'policy' in all_data:
        for name, df in all_data['policy'].items():
            if not df.empty:
                filename = f"{output_dir}/policy_{name}.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                saved_files.append(filename)
                print(f"  ✅ Saved {filename} ({len(df)} rows)")
    
    # Create master file combining key indicators
    print("\n  Creating master file with key indicators...")
    master_data = {}
    
    # Add key BOK indicators
    if 'bok' in all_data:
        for key in ['base_rate', 'cpi', 'unemployment_rate', 'gdp_nominal', 'kospi', 
                   'exchange_usd', 'money_m2', 'household_debt', 'current_account']:
            if key in all_data['bok'] and not all_data['bok'][key].empty:
                df = all_data['bok'][key].copy()
                df = df.rename(columns={'value': key})
                if 'date' in df.columns:
                    df = df[['date', key]]
                    master_data[key] = df
    
    # Merge all data on date
    if master_data:
        master_df = None
        for key, df in master_data.items():
            if master_df is None:
                master_df = df
            else:
                master_df = pd.merge(master_df, df, on='date', how='outer')
        
        master_df = master_df.sort_values('date')
        master_file = f"{output_dir}/master_economic_indicators.csv"
        master_df.to_csv(master_file, index=False, encoding='utf-8-sig')
        print(f"  ✅ Saved {master_file} ({len(master_df)} rows)")
    
    return saved_files

def main():
    """Main function"""
    print("="*60)
    print("COMPREHENSIVE DATA DOWNLOAD FROM BOK & KOSIS")
    print("="*60)
    print(f"Date Range: {START_DATE} to {END_DATE}")
    
    all_data = {}
    
    # Download BOK data
    all_data['bok'] = download_bok_data()
    
    # Download KOSIS data
    all_data['kosis'] = download_kosis_data()
    
    # Create policy variables
    all_data['policy'] = create_policy_dummy_variables(all_data['bok'])
    
    # Save all data
    saved_files = save_all_data(all_data)
    
    # Summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    
    bok_success = sum(1 for df in all_data['bok'].values() if not df.empty)
    kosis_success = sum(1 for df in all_data['kosis'].values() if not df.empty)
    
    print(f"BOK indicators downloaded: {bok_success}/{len(all_data['bok'])}")
    print(f"KOSIS indicators downloaded: {kosis_success}/{len(all_data['kosis'])}")
    print(f"Total files saved: {len(saved_files)}")
    print(f"Output directory: data_downloads/")
    
    return all_data

if __name__ == '__main__':
    data = main()