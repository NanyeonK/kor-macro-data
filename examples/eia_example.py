#!/usr/bin/env python3
"""
Example: Using the EIA (Energy Information Administration) Connector

This example demonstrates how to fetch energy data including:
- WTI and Brent crude oil prices
- Natural gas prices
- US gasoline prices
- Korea energy consumption data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kor_macro.connectors import EIAConnector
import pandas as pd
from datetime import datetime

def main():
    """Main function demonstrating EIA connector usage."""
    
    print("=" * 60)
    print("EIA Energy Data Example")
    print("=" * 60)
    
    # Initialize EIA connector
    eia = EIAConnector()
    print("\n✅ EIA connector initialized")
    
    # 1. Get WTI crude oil prices
    print("\n📊 Fetching WTI Crude Oil Prices...")
    wti_data = eia.get_wti_crude_price(start_date='2023-01-01', end_date='2024-01-01')
    
    if not wti_data.empty:
        print(f"  ✓ Retrieved {len(wti_data)} daily WTI prices")
        print(f"  ✓ Latest price: ${wti_data.iloc[-1]['value']:.2f}")
        print(f"  ✓ Average 2023 price: ${wti_data['value'].mean():.2f}")
    else:
        print("  ⚠️ No WTI data retrieved (API key may be required)")
    
    # 2. Get Brent crude oil prices
    print("\n📊 Fetching Brent Crude Oil Prices...")
    brent_data = eia.get_brent_crude_price(start_date='2023-01-01', end_date='2024-01-01')
    
    if not brent_data.empty:
        print(f"  ✓ Retrieved {len(brent_data)} daily Brent prices")
        print(f"  ✓ Latest price: ${brent_data.iloc[-1]['value']:.2f}")
        
        # Calculate spread between WTI and Brent
        if not wti_data.empty:
            merged = pd.merge(wti_data, brent_data, on='date', suffixes=('_wti', '_brent'))
            merged['spread'] = merged['value_brent'] - merged['value_wti']
            print(f"  ✓ WTI-Brent spread: ${merged['spread'].mean():.2f}")
    
    # 3. Get US gasoline prices
    print("\n📊 Fetching US Gasoline Prices...")
    gas_data = eia.get_us_gasoline_price(start_date='2023-01-01')
    
    if not gas_data.empty:
        print(f"  ✓ Retrieved {len(gas_data)} weekly gasoline prices")
        print(f"  ✓ Latest price: ${gas_data.iloc[-1]['value']:.2f}/gallon")
    
    # 4. Get Korea energy consumption data
    print("\n📊 Fetching Korea Energy Data...")
    korea_petroleum = eia.get_korea_energy_data(
        data_type='petroleum_consumption',
        start_date='2015-01-01'
    )
    
    if not korea_petroleum.empty:
        print(f"  ✓ Retrieved {len(korea_petroleum)} annual Korea petroleum consumption records")
        print(f"  ✓ Latest consumption: {korea_petroleum.iloc[-1]['value']:.0f} thousand barrels/day")
    
    korea_electricity = eia.get_korea_energy_data(
        data_type='electricity_generation',
        start_date='2015-01-01'
    )
    
    if not korea_electricity.empty:
        print(f"  ✓ Retrieved {len(korea_electricity)} annual Korea electricity generation records")
        print(f"  ✓ Latest generation: {korea_electricity.iloc[-1]['value']:.0f} billion kWh")
    
    # 5. Get natural gas prices
    print("\n📊 Fetching Henry Hub Natural Gas Prices...")
    gas_data = eia.get_henry_hub_gas_price(start_date='2023-01-01')
    
    if not gas_data.empty:
        print(f"  ✓ Retrieved {len(gas_data)} daily natural gas prices")
        print(f"  ✓ Latest price: ${gas_data.iloc[-1]['value']:.2f}/MMBtu")
    
    # 6. Get US crude oil inventories
    print("\n📊 Fetching US Crude Oil Inventories...")
    inventory_data = eia.get_crude_oil_inventories(start_date='2023-01-01')
    
    if not inventory_data.empty:
        print(f"  ✓ Retrieved {len(inventory_data)} weekly inventory reports")
        print(f"  ✓ Latest inventory: {inventory_data.iloc[-1]['value']:.0f} thousand barrels")
    
    # 7. List all available datasets
    print("\n📋 Available EIA Datasets:")
    datasets = eia.list_datasets()
    
    # Group by category
    categories = {}
    for dataset in datasets:
        cat = dataset['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(dataset['name'])
    
    for category, items in categories.items():
        print(f"\n  {category}:")
        for item in items[:5]:  # Show first 5 items per category
            print(f"    • {item}")
        if len(items) > 5:
            print(f"    ... and {len(items)-5} more")
    
    # Save example data if available
    if not wti_data.empty:
        output_file = 'eia_wti_prices.csv'
        wti_data.to_csv(output_file, index=False)
        print(f"\n💾 Sample WTI data saved to {output_file}")
    
    print("\n" + "=" * 60)
    print("✅ EIA connector example completed!")
    print("\nNote: Some data may require an EIA API key.")
    print("Get your free key at: https://www.eia.gov/opendata/")

if __name__ == "__main__":
    main()