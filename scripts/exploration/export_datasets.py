"""Export all available Korean datasets to CSV files and generate documentation"""

import os
import csv
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging
from connectors import BOKConnector, KOSISConnector, SeoulDataConnector

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create directories for output
OUTPUT_DIR = Path("data_exports")
OUTPUT_DIR.mkdir(exist_ok=True)
CSV_DIR = OUTPUT_DIR / "csv"
CSV_DIR.mkdir(exist_ok=True)

class DatasetExporter:
    """Export Korean datasets to CSV and generate documentation"""
    
    def __init__(self):
        self.bok = BOKConnector()
        self.kosis = KOSISConnector()
        self.seoul = SeoulDataConnector()
        self.catalog = []
        self.export_results = []
        
    def export_bok_datasets(self):
        """Export Bank of Korea datasets"""
        logger.info("Exporting BOK datasets...")
        
        # Define BOK datasets to export
        bok_exports = [
            ('base_rate', '722Y001', 'M', 'Bank of Korea Base Rate'),
            ('exchange_rate', '731Y001', 'M', 'USD/KRW Exchange Rate'),
            ('money_supply', '101Y004', 'M', 'Money Supply (M2)'),
            ('gdp', '200Y001', 'Q', 'Gross Domestic Product'),
            ('cpi', '901Y009', 'M', 'Consumer Price Index'),
            ('housing_price', '901Y067', 'M', 'Housing Price Index'),
        ]
        
        for name, code, period, description in bok_exports:
            try:
                # Fetch data
                data = self.bok.fetch_data(code, '20200101', '20241231', period)
                
                if data['success'] and data['data']:
                    # Convert to DataFrame
                    df = pd.DataFrame(data['data'])
                    
                    # Select relevant columns if they exist
                    columns_to_keep = ['TIME', 'ITEM_NAME1', 'DATA_VALUE', 'UNIT_NAME']
                    available_cols = [col for col in columns_to_keep if col in df.columns]
                    if available_cols:
                        df = df[available_cols]
                    
                    # Save to CSV
                    csv_path = CSV_DIR / f"bok_{name}.csv"
                    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                    
                    # Add to catalog
                    self.catalog.append({
                        'source': 'Bank of Korea',
                        'dataset': description,
                        'code': code,
                        'period': period,
                        'records': len(df),
                        'file': f"bok_{name}.csv",
                        'status': 'Success'
                    })
                    
                    logger.info(f"  ✓ Exported {name}: {len(df)} records")
                else:
                    self.catalog.append({
                        'source': 'Bank of Korea',
                        'dataset': description,
                        'code': code,
                        'period': period,
                        'records': 0,
                        'file': f"bok_{name}.csv",
                        'status': 'No data available'
                    })
                    logger.warning(f"  ⚠ No data for {name}")
                    
            except Exception as e:
                logger.error(f"  ✗ Error exporting {name}: {e}")
                self.catalog.append({
                    'source': 'Bank of Korea',
                    'dataset': description,
                    'code': code,
                    'period': period,
                    'records': 0,
                    'file': f"bok_{name}.csv",
                    'status': f'Error: {str(e)}'
                })
    
    def export_kosis_datasets(self):
        """Export KOSIS datasets"""
        logger.info("Exporting KOSIS datasets...")
        
        # Define KOSIS datasets to export
        kosis_exports = [
            ('population', 'DT_1B040A3', 'Population Statistics'),
            ('household', 'DT_1JC1501', 'Household Statistics'),
            ('employment', 'DT_1DA7001S', 'Employment Rate'),
            ('real_estate_trans', 'DT_1YL2101', 'Real Estate Transactions'),
            ('apartment_prices', 'DT_1YL2001', 'Apartment Prices'),
        ]
        
        for name, table_id, description in kosis_exports:
            try:
                # Fetch data
                data = self.kosis.fetch_data(table_id, '202001', '202412')
                
                if data['success'] and data['data']:
                    # Convert to DataFrame
                    df = pd.DataFrame(data['data'])
                    
                    # Select relevant columns if they exist
                    columns_to_keep = ['PRD_DE', 'C1_NM', 'C2_NM', 'DT', 'UNIT_NM']
                    available_cols = [col for col in columns_to_keep if col in df.columns]
                    if available_cols:
                        df = df[available_cols]
                    
                    # Save to CSV
                    csv_path = CSV_DIR / f"kosis_{name}.csv"
                    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                    
                    # Add to catalog
                    self.catalog.append({
                        'source': 'KOSIS',
                        'dataset': description,
                        'code': table_id,
                        'period': 'Monthly',
                        'records': len(df),
                        'file': f"kosis_{name}.csv",
                        'status': 'Success'
                    })
                    
                    logger.info(f"  ✓ Exported {name}: {len(df)} records")
                else:
                    self.catalog.append({
                        'source': 'KOSIS',
                        'dataset': description,
                        'code': table_id,
                        'period': 'Monthly',
                        'records': 0,
                        'file': f"kosis_{name}.csv",
                        'status': 'No data available'
                    })
                    logger.warning(f"  ⚠ No data for {name}")
                    
            except Exception as e:
                logger.error(f"  ✗ Error exporting {name}: {e}")
                self.catalog.append({
                    'source': 'KOSIS',
                    'dataset': description,
                    'code': table_id,
                    'period': 'Monthly',
                    'records': 0,
                    'file': f"kosis_{name}.csv",
                    'status': f'Error: {str(e)}'
                })
    
    def export_seoul_datasets(self):
        """Export Seoul Open Data datasets"""
        logger.info("Exporting Seoul datasets...")
        
        # Export air quality data
        try:
            data = self.seoul.get_air_quality(1, 25)  # All 25 districts
            
            if data['success'] and data['data']:
                df = pd.DataFrame(data['data'])
                
                # Select relevant columns
                columns_to_keep = ['MSRSTE_NM', 'PM10', 'PM25', 'O3', 'NO2', 'CO', 'SO2', 'MSRDT']
                available_cols = [col for col in columns_to_keep if col in df.columns]
                if available_cols:
                    df = df[available_cols]
                
                csv_path = CSV_DIR / "seoul_air_quality.csv"
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                
                self.catalog.append({
                    'source': 'Seoul Open Data',
                    'dataset': 'Real-time Air Quality',
                    'code': 'RealtimeCityAir',
                    'period': 'Real-time',
                    'records': len(df),
                    'file': 'seoul_air_quality.csv',
                    'status': 'Success'
                })
                
                logger.info(f"  ✓ Exported air quality: {len(df)} records")
        except Exception as e:
            logger.error(f"  ✗ Error exporting air quality: {e}")
            self.catalog.append({
                'source': 'Seoul Open Data',
                'dataset': 'Real-time Air Quality',
                'code': 'RealtimeCityAir',
                'period': 'Real-time',
                'records': 0,
                'file': 'seoul_air_quality.csv',
                'status': f'Error: {str(e)}'
            })
    
    def create_catalog_csv(self):
        """Create a master catalog CSV of all datasets"""
        catalog_df = pd.DataFrame(self.catalog)
        catalog_path = OUTPUT_DIR / "dataset_catalog.csv"
        catalog_df.to_csv(catalog_path, index=False, encoding='utf-8-sig')
        logger.info(f"Created catalog: {catalog_path}")
        return catalog_df
    
    def create_documentation(self):
        """Create markdown documentation"""
        doc_path = OUTPUT_DIR / "DATASET_DOCUMENTATION.md"
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write("# Korean Economic & Real Estate Data Catalog\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary statistics
            f.write("## Summary\n\n")
            total_datasets = len(self.catalog)
            successful = sum(1 for c in self.catalog if c['status'] == 'Success')
            total_records = sum(c['records'] for c in self.catalog)
            
            f.write(f"- **Total Datasets**: {total_datasets}\n")
            f.write(f"- **Successfully Exported**: {successful}\n")
            f.write(f"- **Total Records**: {total_records:,}\n\n")
            
            # Datasets by source
            f.write("## Available Datasets\n\n")
            
            # Group by source
            sources = {}
            for item in self.catalog:
                source = item['source']
                if source not in sources:
                    sources[source] = []
                sources[source].append(item)
            
            for source, datasets in sources.items():
                f.write(f"### {source}\n\n")
                f.write("| Dataset | Code | Period | Records | File | Status |\n")
                f.write("|---------|------|--------|---------|------|--------|\n")
                
                for ds in datasets:
                    f.write(f"| {ds['dataset']} | {ds['code']} | {ds['period']} | ")
                    f.write(f"{ds['records']:,} | {ds['file']} | {ds['status']} |\n")
                
                f.write("\n")
            
            # Data dictionary
            f.write("## Data Sources\n\n")
            
            f.write("### Bank of Korea (한국은행)\n")
            f.write("- **API**: ECOS (Economic Statistics System)\n")
            f.write("- **Coverage**: Macroeconomic indicators, monetary policy, financial statistics\n")
            f.write("- **Update Frequency**: Daily to Quarterly\n\n")
            
            f.write("### KOSIS (통계청)\n")
            f.write("- **API**: Korean Statistical Information Service\n")
            f.write("- **Coverage**: Population, employment, real estate, regional statistics\n")
            f.write("- **Update Frequency**: Monthly to Yearly\n\n")
            
            f.write("### Seoul Open Data (서울 열린데이터 광장)\n")
            f.write("- **API**: Seoul Metropolitan Government Open Data\n")
            f.write("- **Coverage**: Seoul-specific data including real estate, air quality, transportation\n")
            f.write("- **Update Frequency**: Real-time to Monthly\n\n")
            
            # Usage instructions
            f.write("## Usage Instructions\n\n")
            f.write("### CSV Files\n")
            f.write("All data files are exported in CSV format with UTF-8 encoding (BOM for Excel compatibility).\n\n")
            f.write("```python\n")
            f.write("import pandas as pd\n\n")
            f.write("# Load a dataset\n")
            f.write("df = pd.read_csv('data_exports/csv/kosis_population.csv')\n")
            f.write("```\n\n")
            
            f.write("### Python Package Usage\n")
            f.write("```python\n")
            f.write("from connectors import BOKConnector, KOSISConnector, SeoulDataConnector\n\n")
            f.write("# Bank of Korea\n")
            f.write("bok = BOKConnector()\n")
            f.write("base_rate = bok.get_base_rate('20230101', '20241231')\n\n")
            f.write("# KOSIS\n")
            f.write("kosis = KOSISConnector()\n")
            f.write("population = kosis.get_population_stats('202301', '202412')\n\n")
            f.write("# Seoul Data\n")
            f.write("seoul = SeoulDataConnector()\n")
            f.write("air_quality = seoul.get_air_quality()\n")
            f.write("```\n\n")
            
            f.write("## Files Generated\n\n")
            f.write("- `dataset_catalog.csv` - Master list of all datasets\n")
            f.write("- `csv/` - Directory containing all exported data files\n")
            f.write("- `DATASET_DOCUMENTATION.md` - This documentation file\n")
        
        logger.info(f"Created documentation: {doc_path}")
    
    def run(self):
        """Run the complete export process"""
        logger.info("Starting dataset export process...")
        
        # Export from each source
        self.export_bok_datasets()
        self.export_kosis_datasets()
        self.export_seoul_datasets()
        
        # Create catalog and documentation
        catalog_df = self.create_catalog_csv()
        self.create_documentation()
        
        logger.info("Export process completed!")
        
        # Print summary
        print("\n" + "="*60)
        print("EXPORT SUMMARY")
        print("="*60)
        print(f"Total datasets processed: {len(self.catalog)}")
        print(f"Successful exports: {sum(1 for c in self.catalog if c['status'] == 'Success')}")
        print(f"Total records exported: {sum(c['records'] for c in self.catalog):,}")
        print(f"\nFiles created in: {OUTPUT_DIR.absolute()}")
        print("  - dataset_catalog.csv")
        print("  - DATASET_DOCUMENTATION.md")
        print(f"  - {len(list(CSV_DIR.glob('*.csv')))} CSV data files")

if __name__ == "__main__":
    exporter = DatasetExporter()
    exporter.run()