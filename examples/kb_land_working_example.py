#!/usr/bin/env python3
"""
Working Example: KB Land Real Estate Data

This example demonstrates how to fetch and analyze Korean real estate data
from KB Land, including housing prices, Jeonse rates, and market trends.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use the fixed KB Land connector
import importlib.util
spec = importlib.util.spec_from_file_location("kbland_fixed", 
                                              "kor_macro/connectors/kbland_fixed.py")
kbland_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kbland_module)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def main():
    """Main function demonstrating KB Land data retrieval"""
    
    print("=" * 70)
    print("KB Land Real Estate Data Example")
    print("=" * 70)
    
    # Initialize KB Land connector
    kb = kbland_module.KBLandConnector()
    print("\n✅ KB Land connector initialized")
    
    # 1. Get Seoul apartment price index
    print("\n" + "=" * 70)
    print("1. Seoul Apartment Price Index (서울 아파트 매매가격지수)")
    print("-" * 70)
    
    seoul_apt = kb.get_housing_index(
        house_type='apartment',
        region='서울',
        start_date='2022-01-01',
        end_date='2024-12-31'
    )
    
    if not seoul_apt.empty:
        print(f"✓ Retrieved {len(seoul_apt)} months of data")
        print(f"✓ Latest index: {seoul_apt.iloc[-1]['price_index']:.2f}")
        print(f"✓ YoY change: {seoul_apt.iloc[-1]['yoy_change']:.2f}%")
        print(f"✓ MoM change: {seoul_apt.iloc[-1]['mom_change']:.2f}%")
        
        # Show recent trends
        print("\nRecent 6 months trend:")
        recent = seoul_apt.tail(6)[['date', 'price_index', 'mom_change', 'yoy_change']]
        recent['date'] = recent['date'].dt.strftime('%Y-%m')
        print(recent.to_string(index=False))
    
    # 2. Get Jeonse price index
    print("\n" + "=" * 70)
    print("2. Seoul Jeonse Price Index (서울 전세가격지수)")
    print("-" * 70)
    
    jeonse = kb.get_jeonse_index(
        region='서울',
        start_date='2022-01-01',
        end_date='2024-12-31'
    )
    
    if not jeonse.empty:
        print(f"✓ Retrieved {len(jeonse)} months of Jeonse data")
        print(f"✓ Latest index: {jeonse.iloc[-1]['price_index']:.2f}")
        print(f"✓ YoY change: {jeonse.iloc[-1]['yoy_change']:.2f}%")
        
    # 3. Compare sale vs Jeonse trends
    print("\n" + "=" * 70)
    print("3. Sale vs Jeonse Comparison")
    print("-" * 70)
    
    if not seoul_apt.empty and not jeonse.empty:
        # Merge data
        comparison = pd.merge(
            seoul_apt[['date', 'price_index', 'yoy_change']],
            jeonse[['date', 'price_index', 'yoy_change']],
            on='date',
            suffixes=('_sale', '_jeonse')
        )
        
        # Calculate Jeonse ratio (전세가율)
        comparison['jeonse_ratio'] = (comparison['price_index_jeonse'] / 
                                      comparison['price_index_sale'] * 100)
        
        print(f"✓ Average Jeonse ratio: {comparison['jeonse_ratio'].mean():.1f}%")
        print(f"✓ Current Jeonse ratio: {comparison.iloc[-1]['jeonse_ratio']:.1f}%")
        
        # Correlation
        corr = comparison['yoy_change_sale'].corr(comparison['yoy_change_jeonse'])
        print(f"✓ Sale-Jeonse correlation: {corr:.3f}")
    
    # 4. Get monthly rent index
    print("\n" + "=" * 70)
    print("4. Monthly Rent Index (월세가격지수)")
    print("-" * 70)
    
    rent = kb.get_rent_index(
        region='서울',
        start_date='2023-01-01',
        end_date='2024-12-31'
    )
    
    if not rent.empty:
        print(f"✓ Retrieved {len(rent)} months of rent data")
        print(f"✓ Latest index: {rent.iloc[-1]['price_index']:.2f}")
        print(f"✓ YoY change: {rent.iloc[-1]['yoy_change']:.2f}%")
    
    # 5. Market sentiment and trends
    print("\n" + "=" * 70)
    print("5. Market Trends and Sentiment")
    print("-" * 70)
    
    market_trend = kb.get_market_trend(region='서울')
    
    if not market_trend.empty:
        latest_trend = market_trend.iloc[-1]
        print(f"✓ Supply-Demand Balance: {latest_trend.get('supply_demand', 'N/A')}")
        print(f"✓ Transaction Volume: {latest_trend.get('transaction_volume', 0):,}")
        
        # Count trend distribution
        if 'supply_demand' in market_trend.columns:
            trend_counts = market_trend['supply_demand'].value_counts()
            print("\nMarket sentiment (last 3 months):")
            for trend, count in trend_counts.items():
                print(f"  • {trend}: {count} weeks")
    
    # 6. Price outlook
    print("\n" + "=" * 70)
    print("6. Price Outlook Index (가격전망지수)")
    print("-" * 70)
    
    outlook = kb.get_price_outlook(region='서울')
    
    if not outlook.empty:
        latest_outlook = outlook.iloc[-1]
        print(f"✓ Outlook Index: {latest_outlook.get('outlook_index', 0):.1f}")
        print(f"✓ Sentiment: {latest_outlook.get('sentiment', 'N/A')}")
        
        # Sentiment distribution
        if 'sentiment' in outlook.columns:
            sentiment_counts = outlook['sentiment'].value_counts()
            print("\nSentiment distribution (last 6 months):")
            for sentiment, count in sentiment_counts.items():
                print(f"  • {sentiment}: {count} months")
    
    # 7. Regional comparison
    print("\n" + "=" * 70)
    print("7. Regional Comparison")
    print("-" * 70)
    
    regions = ['서울', '부산', '대구', '인천', '경기']
    regional_data = kb.get_regional_comparison(
        house_type='apartment',
        regions=regions,
        date=datetime.now().strftime('%Y-%m-%d')
    )
    
    if not regional_data.empty:
        print("\nRegional Price Indices (Latest):")
        summary = regional_data.groupby('region').agg({
            'price_index': 'last',
            'yoy_change': 'last'
        }).round(2)
        print(summary.to_string())
    
    # 8. Create visualizations
    print("\n" + "=" * 70)
    print("8. Creating Visualizations")
    print("-" * 70)
    
    if not seoul_apt.empty and not jeonse.empty:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Price indices
        axes[0, 0].plot(seoul_apt['date'], seoul_apt['price_index'], 
                       label='Sale Price', color='blue', linewidth=2)
        axes[0, 0].plot(jeonse['date'], jeonse['price_index'], 
                       label='Jeonse Price', color='orange', linewidth=2)
        axes[0, 0].set_title('Seoul Apartment Price Indices')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Index (Base=100)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Year-over-year changes
        axes[0, 1].plot(seoul_apt['date'], seoul_apt['yoy_change'], 
                       label='Sale YoY', color='blue', linewidth=2)
        axes[0, 1].plot(jeonse['date'], jeonse['yoy_change'], 
                       label='Jeonse YoY', color='orange', linewidth=2)
        axes[0, 1].axhline(y=0, color='red', linestyle='--', alpha=0.5)
        axes[0, 1].set_title('Year-over-Year Price Changes')
        axes[0, 1].set_xlabel('Date')
        axes[0, 1].set_ylabel('YoY Change (%)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Jeonse ratio
        if not comparison.empty:
            axes[1, 0].plot(comparison['date'], comparison['jeonse_ratio'], 
                           color='green', linewidth=2)
            axes[1, 0].axhline(y=comparison['jeonse_ratio'].mean(), 
                              color='red', linestyle='--', alpha=0.5, 
                              label=f"Average: {comparison['jeonse_ratio'].mean():.1f}%")
            axes[1, 0].set_title('Jeonse-to-Sale Ratio (전세가율)')
            axes[1, 0].set_xlabel('Date')
            axes[1, 0].set_ylabel('Ratio (%)')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Regional comparison
        if not regional_data.empty:
            regional_summary = regional_data.groupby('region')['price_index'].last().sort_values()
            bars = axes[1, 1].bar(range(len(regional_summary)), 
                                 regional_summary.values,
                                 color=['red' if x == '서울' else 'skyblue' 
                                       for x in regional_summary.index])
            axes[1, 1].set_xticks(range(len(regional_summary)))
            axes[1, 1].set_xticklabels(regional_summary.index, rotation=45)
            axes[1, 1].set_title('Regional Price Index Comparison')
            axes[1, 1].set_ylabel('Price Index')
            axes[1, 1].grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for i, (idx, val) in enumerate(regional_summary.items()):
                axes[1, 1].text(i, val + 1, f'{val:.1f}', 
                              ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('kb_land_analysis.png', dpi=100, bbox_inches='tight')
        print("✅ Saved visualization to kb_land_analysis.png")
    
    # 9. Export data
    print("\n" + "=" * 70)
    print("9. Exporting Data")
    print("-" * 70)
    
    # Combine all data for export
    export_data = {
        'seoul_apartment': seoul_apt,
        'seoul_jeonse': jeonse,
        'seoul_rent': rent,
        'market_trend': market_trend,
        'price_outlook': outlook
    }
    
    # Save to Excel with multiple sheets
    with pd.ExcelWriter('kb_land_data.xlsx') as writer:
        for sheet_name, df in export_data.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"✓ Exported {sheet_name}: {len(df)} records")
    
    print("\n✅ All data exported to kb_land_data.xlsx")
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("Summary Statistics")
    print("=" * 70)
    
    if not seoul_apt.empty:
        print("\nSeoul Apartment Sale Prices:")
        print(f"  • Total growth (period): {(seoul_apt.iloc[-1]['price_index'] / seoul_apt.iloc[0]['price_index'] - 1) * 100:.2f}%")
        print(f"  • Average monthly change: {seoul_apt['mom_change'].mean():.3f}%")
        print(f"  • Volatility (std): {seoul_apt['mom_change'].std():.3f}%")
        print(f"  • Max monthly change: {seoul_apt['mom_change'].max():.2f}%")
        print(f"  • Min monthly change: {seoul_apt['mom_change'].min():.2f}%")
    
    if not jeonse.empty:
        print("\nSeoul Jeonse Prices:")
        print(f"  • Total growth (period): {(jeonse.iloc[-1]['price_index'] / jeonse.iloc[0]['price_index'] - 1) * 100:.2f}%")
        print(f"  • Average monthly change: {jeonse['mom_change'].mean():.3f}%")
        print(f"  • Volatility (std): {jeonse['mom_change'].std():.3f}%")
    
    print("\n" + "=" * 70)
    print("✅ KB Land data analysis complete!")
    print("\nNote: This uses sample data for demonstration.")
    print("For real data, implement actual KB Land API calls.")

if __name__ == "__main__":
    main()