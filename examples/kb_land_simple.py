#!/usr/bin/env python3
"""
Simple KB Land Real Estate Data Example

Quick example showing how to get Korean real estate data.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the fixed KB Land connector
import importlib.util
spec = importlib.util.spec_from_file_location("kbland_fixed", 
                                              "kor_macro/connectors/kbland_fixed.py")
kb_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb_module)

def main():
    print("\n" + "="*60)
    print("KB Land Real Estate Data - Simple Example")
    print("="*60)
    
    # Initialize connector
    kb = kb_module.KBLandConnector()
    
    # 1. Get Seoul apartment prices
    print("\n📊 Seoul Apartment Prices (Last 12 months)")
    print("-"*40)
    
    apt_prices = kb.get_housing_index(
        house_type='apartment',
        region='서울',
        start_date='2024-01-01',
        end_date='2024-12-31'
    )
    
    if not apt_prices.empty:
        # Show summary
        latest = apt_prices.iloc[-1]
        print(f"Latest Index: {latest['price_index']:.2f}")
        print(f"YoY Change: {latest['yoy_change']:.2f}%")
        print(f"MoM Change: {latest['mom_change']:.2f}%")
        
        # Show trend
        print("\nMonthly Trend:")
        for _, row in apt_prices.iterrows():
            date_str = row['date'].strftime('%Y-%m')
            bar = '█' * int(abs(row['mom_change']) * 10)
            sign = '+' if row['mom_change'] > 0 else ''
            print(f"{date_str}: {sign}{row['mom_change']:5.2f}% {bar}")
    
    # 2. Get Jeonse prices
    print("\n📊 Seoul Jeonse Prices (Last 12 months)")
    print("-"*40)
    
    jeonse = kb.get_jeonse_index(
        region='서울',
        start_date='2024-01-01',
        end_date='2024-12-31'
    )
    
    if not jeonse.empty:
        latest = jeonse.iloc[-1]
        print(f"Latest Index: {latest['price_index']:.2f}")
        print(f"YoY Change: {latest['yoy_change']:.2f}%")
        
        # Calculate Jeonse ratio
        if not apt_prices.empty:
            jeonse_ratio = (latest['price_index'] / apt_prices.iloc[-1]['price_index']) * 100
            print(f"Jeonse/Sale Ratio: {jeonse_ratio:.1f}%")
    
    # 3. Market sentiment
    print("\n📊 Market Sentiment")
    print("-"*40)
    
    market = kb.get_market_trend(region='서울')
    if not market.empty:
        # Count sentiment
        sentiment_counts = market['supply_demand'].value_counts()
        total = len(market)
        
        for sentiment, count in sentiment_counts.items():
            pct = (count / total) * 100
            bar = '█' * int(pct / 5)
            print(f"{sentiment}: {pct:5.1f}% {bar}")
    
    # 4. Regional comparison
    print("\n📊 Regional Price Comparison (Latest)")
    print("-"*40)
    
    regions = ['서울', '경기', '부산', '대구', '인천']
    
    print("Region     Index    YoY Change")
    print("-"*35)
    
    for region in regions:
        data = kb.get_housing_index(
            house_type='apartment',
            region=region,
            period='2024-12'
        )
        if not data.empty:
            latest = data.iloc[-1]
            change_symbol = '↑' if latest['yoy_change'] > 0 else '↓'
            print(f"{region:8} {latest['price_index']:7.2f}  {latest['yoy_change']:+6.2f}% {change_symbol}")
    
    print("\n" + "="*60)
    print("✅ Analysis Complete!")
    print("\nNote: This uses sample data for demonstration.")
    print("For production use, implement actual KB Land API.")
    print("="*60)

if __name__ == "__main__":
    main()