"""List and document all KB Land available datasets"""

import pandas as pd
from pathlib import Path
from connectors.kbland_enhanced import KBLandEnhancedConnector
import json

def generate_kb_land_documentation():
    """Generate comprehensive KB Land data documentation"""
    
    print("="*80)
    print("KB Land Data Catalog")
    print("="*80)
    
    # Initialize connector
    kb = KBLandEnhancedConnector()
    
    # Get catalog as DataFrame
    catalog_df = kb.get_catalog()
    
    # Display catalog
    print("\nAvailable KB Land Datasets:")
    print("-"*80)
    
    for idx, row in catalog_df.iterrows():
        print(f"\n{idx+1}. {row['Name']} ({row['Korean']})")
        print(f"   ID: {row['ID']}")
        print(f"   Format: {row['Format']}")
        print(f"   Update Frequency: {row['Frequency']}")
        print(f"   URL: {row['URL']}")
        print(f"   Data Types:")
        for dtype in row['Data Types'].split(', '):
            print(f"     - {dtype}")
    
    # Save to CSV
    output_dir = Path('dataset_lists')
    output_dir.mkdir(exist_ok=True)
    
    csv_path = output_dir / 'kb_land_complete_catalog.csv'
    catalog_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\n✓ Catalog saved to: {csv_path}")
    
    # Create detailed JSON catalog
    detailed_catalog = {}
    for key, info in kb.KB_DATA_CATALOG.items():
        detailed_catalog[key] = {
            'name_en': info['name'],
            'name_kr': info['korean'],
            'url': info['url'],
            'format': info['format'],
            'frequency': info['frequency'],
            'data_types': info['data_types']
        }
    
    json_path = output_dir / 'kb_land_detailed_catalog.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(detailed_catalog, f, ensure_ascii=False, indent=2)
    print(f"✓ Detailed catalog saved to: {json_path}")
    
    # Generate markdown documentation
    generate_markdown_doc(catalog_df, detailed_catalog)
    
    return catalog_df, detailed_catalog

def generate_markdown_doc(catalog_df, detailed_catalog):
    """Generate markdown documentation for KB Land data"""
    
    md_content = """# KB Land Complete Data Catalog

## Overview
KB Land (KB부동산) provides comprehensive Korean real estate market data through their data portal.

## Data Access Information
- **Main Portal**: https://data.kbland.kr
- **Format**: Excel (.xlsx), CSV, PDF
- **Update Schedule**: Monthly (last Monday), Quarterly, Weekly (varies by dataset)
- **Language**: Korean (some English headers available)

## Complete Dataset List

"""
    
    # Add summary table
    md_content += "### Summary Table\n\n"
    md_content += "| No | Dataset | Korean Name | Format | Frequency |\n"
    md_content += "|----|---------|-------------|--------|----------|\n"
    
    for idx, row in catalog_df.iterrows():
        md_content += f"| {idx+1} | {row['Name']} | {row['Korean']} | {row['Format']} | {row['Frequency']} |\n"
    
    md_content += "\n## Detailed Dataset Descriptions\n\n"
    
    # Add detailed descriptions
    for idx, (key, info) in enumerate(detailed_catalog.items(), 1):
        md_content += f"### {idx}. {info['name_en']} ({info['name_kr']})\n\n"
        md_content += f"- **Dataset ID**: `{key}`\n"
        md_content += f"- **URL**: {info['url']}\n"
        md_content += f"- **Format**: {info['format']}\n"
        md_content += f"- **Update Frequency**: {info['frequency']}\n"
        md_content += f"- **Data Contents**:\n"
        for dtype in info['data_types']:
            md_content += f"  - {dtype}\n"
        md_content += "\n"
    
    # Add usage section
    md_content += """## Usage with Python Package

### Basic Usage
```python
from connectors.kbland_enhanced import KBLandEnhancedConnector

# Initialize connector
kb = KBLandEnhancedConnector()

# Get catalog
catalog = kb.get_catalog()

# Download specific dataset
success, filepath = kb.download_dataset('price_index')

# Download all datasets
results = kb.download_all_datasets()
```

### Available Dataset IDs
- `price_index` - KB Housing Price Index
- `jeonse_index` - KB Jeonse Price Index
- `monthly_rent` - KB Monthly Rent Index
- `transaction_volume` - Real Estate Transaction Volume
- `market_sentiment` - Market Sentiment Index
- `regional_analysis` - Regional Market Analysis
- `apartment_ranking` - Apartment Complex Rankings
- `office_retail` - Office & Retail Market
- `land_price` - Land Price Index
- `policy_impact` - Policy Impact Analysis

## Data Update Schedule
- **Monthly Data**: Released on the last Monday of each month
- **Quarterly Data**: Released in January, April, July, October
- **Weekly Rankings**: Updated every Monday
- **Special Reports**: Released as needed for policy changes

## Notes
- Data lag: Approximately 1 month (e.g., January data released end of February)
- Historical data: Available from 1986 for major indices
- Regional coverage: Nationwide with special focus on Seoul metropolitan area
- Excel files typically contain multiple sheets with different regional breakdowns
"""
    
    # Save markdown
    output_path = Path('dataset_lists') / 'KB_LAND_COMPLETE_CATALOG.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✓ Markdown documentation saved to: {output_path}")

def main():
    """Main function"""
    print("\n📊 Generating KB Land Data Documentation\n")
    
    catalog_df, detailed_catalog = generate_kb_land_documentation()
    
    print("\n" + "="*80)
    print("Summary")
    print("="*80)
    print(f"Total Datasets: {len(catalog_df)}")
    print(f"Data Formats: Excel, CSV, PDF")
    print(f"Coverage: National, Regional, District-level")
    print(f"Time Period: 1986 - Present (varies by dataset)")
    
    print("\n✅ KB Land data catalog generation complete!")
    print("\nFiles created:")
    print("  - dataset_lists/kb_land_complete_catalog.csv")
    print("  - dataset_lists/kb_land_detailed_catalog.json")
    print("  - dataset_lists/KB_LAND_COMPLETE_CATALOG.md")

if __name__ == "__main__":
    main()