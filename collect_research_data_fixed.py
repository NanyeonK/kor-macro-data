"""
Fixed Data Collection for Korean Real Estate Market Research
Using correct BOK series codes and KOSIS table discovery
Data Period: January 2010 - December 2024
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import logging
from connectors import BOKConnector, KOSISConnector, SeoulDataConnector
from connectors.kbland_enhanced import KBLandEnhancedConnector
from connectors.global_data import FREDConnector, WorldBankConnector
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Create output directory
output_dir = Path('research_data_fixed')
output_dir.mkdir(exist_ok=True)

class FixedResearchDataCollector:
    def __init__(self):
        self.start_date = '20100101'
        self.end_date = '20241231'
        self.data_tracker = []
        
        # Initialize connectors
        try:
            self.bok = BOKConnector()
            logger.info("✓ BOK connector initialized")
        except:
            self.bok = None
            logger.error("✗ BOK connector failed")
            
        try:
            self.kosis = KOSISConnector()
            logger.info("✓ KOSIS connector initialized")
        except:
            self.kosis = None
            logger.error("✗ KOSIS connector failed")
            
        try:
            self.kb = KBLandEnhancedConnector()
            logger.info("✓ KB Land connector initialized")
        except:
            self.kb = None
            logger.error("✗ KB Land connector failed")
            
        try:
            self.fred = FREDConnector()
            logger.info("✓ FRED connector initialized")
        except:
            self.fred = None
            logger.error("✗ FRED connector failed")
    
    def track_data(self, category, indicator, source, frequency, status, filepath=None):
        """Track data collection status"""
        self.data_tracker.append({
            'Category': category,
            'Indicator': indicator,
            'Source': source,
            'Frequency': frequency,
            'Status': status,
            'Filepath': filepath if filepath else 'Not downloaded',
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    def collect_bok_data_fixed(self):
        """Collect BOK data with correct series codes"""
        logger.info("\n" + "="*60)
        logger.info("COLLECTING BOK DATA WITH CORRECT CODES")
        logger.info("="*60)
        
        # Correct BOK series codes from our discovery
        bok_correct_codes = {
            'Base Rate': ('722Y001', 'M', 'Financial'),
            'USD/KRW Exchange Rate': ('731Y001', 'D', 'Financial'),
            'Money Supply M2': ('101Y004', 'M', 'Monetary'),
            'GDP': ('200Y001', 'Q', 'Macroeconomic'),
            'Consumer Price Index': ('901Y009', 'M', 'Price'),
            'Housing Price Index': ('901Y067', 'M', 'Real Estate'),
            'Household Debt': ('008Y002', 'Q', 'Debt'),
            'Unemployment Rate': ('901Y016', 'M', 'Employment'),
        }
        
        for indicator_name, (series_id, freq, category) in bok_correct_codes.items():
            if self.bok:
                try:
                    logger.info(f"Fetching {indicator_name} ({series_id})...")
                    
                    # Try basic fetch first
                    data = self.bok.fetch_data(series_id, self.start_date, self.end_date, freq)
                    
                    if data['success'] and data['data']:
                        # Save to CSV
                        df = pd.DataFrame(data['data'])
                        filepath = output_dir / f"bok_{indicator_name.lower().replace(' ', '_').replace('/', '_')}.csv"
                        df.to_csv(filepath, index=False, encoding='utf-8-sig')
                        self.track_data(category, indicator_name, 'BOK', 
                                      'Daily' if freq == 'D' else 'Monthly' if freq == 'M' else 'Quarterly', 
                                      'Downloaded', str(filepath))
                        logger.info(f"✓ {indicator_name} downloaded")
                    else:
                        # Try alternative method for specific indicators
                        if 'base rate' in indicator_name.lower():
                            data = self.bok.get_base_rate(self.start_date, self.end_date)
                        elif 'housing' in indicator_name.lower():
                            data = self.bok.get_housing_price_index(self.start_date, self.end_date)
                        elif 'household debt' in indicator_name.lower():
                            data = self.bok.get_household_debt(self.start_date, self.end_date)
                        else:
                            data = {'success': False}
                        
                        if data.get('success') and data.get('data'):
                            df = pd.DataFrame(data['data'])
                            filepath = output_dir / f"bok_{indicator_name.lower().replace(' ', '_').replace('/', '_')}.csv"
                            df.to_csv(filepath, index=False, encoding='utf-8-sig')
                            self.track_data(category, indicator_name, 'BOK', 
                                          'Daily' if freq == 'D' else 'Monthly' if freq == 'M' else 'Quarterly', 
                                          'Downloaded', str(filepath))
                            logger.info(f"✓ {indicator_name} downloaded (alternative method)")
                        else:
                            self.track_data(category, indicator_name, 'BOK', 
                                          'Daily' if freq == 'D' else 'Monthly' if freq == 'M' else 'Quarterly', 
                                          'No data', None)
                            logger.warning(f"✗ {indicator_name}: No data available")
                        
                except Exception as e:
                    self.track_data(category, indicator_name, 'BOK', 
                                  'Daily' if freq == 'D' else 'Monthly' if freq == 'M' else 'Quarterly', 
                                  f'Error: {str(e)}', None)
                    logger.error(f"✗ {indicator_name} error: {e}")
            
            time.sleep(0.5)  # Rate limiting
    
    def discover_kosis_tables(self):
        """Try to discover KOSIS table IDs"""
        logger.info("\n" + "="*60)
        logger.info("DISCOVERING KOSIS TABLE IDS")
        logger.info("="*60)
        
        if self.kosis:
            try:
                # Try common KOSIS table patterns
                common_tables = [
                    ('DT_1B040M3', 'Population by Region', 'Population'),
                    ('DT_1DA7001', 'Employment Rate', 'Employment'),
                    ('DT_1YL2001', 'Apartment Price Index', 'Real Estate'),
                    ('DT_1YL2101', 'Real Estate Transactions', 'Real Estate'),
                    ('DT_1JC1501', 'Household Statistics', 'Household'),
                    ('DT_1IN1502', 'Population Movement', 'Population'),
                    ('DT_1B8000F', 'Birth and Death Statistics', 'Demographics'),
                ]
                
                for table_id, description, category in common_tables:
                    try:
                        logger.info(f"Testing {table_id}: {description}...")
                        data = self.kosis.fetch_data(table_id, '201001', '202412')
                        
                        if data['success'] and data['data']:
                            df = pd.DataFrame(data['data'])
                            filepath = output_dir / f"kosis_{table_id}.csv"
                            df.to_csv(filepath, index=False, encoding='utf-8-sig')
                            self.track_data(category, description, 'KOSIS', 'Monthly', 
                                          'Downloaded', str(filepath))
                            logger.info(f"✓ {description} downloaded")
                        else:
                            self.track_data(category, description, 'KOSIS', 'Monthly', 
                                          'No data', None)
                            logger.warning(f"✗ {description}: No data")
                    except Exception as e:
                        logger.error(f"✗ {description} error: {e}")
                    
                    time.sleep(0.5)
                    
            except Exception as e:
                logger.error(f"KOSIS discovery error: {e}")
    
    def collect_kb_and_global_data(self):
        """Collect KB Land and Global data (already working)"""
        logger.info("\n" + "="*60)
        logger.info("COLLECTING KB LAND DATA")
        logger.info("="*60)
        
        # KB Land datasets (already working)
        kb_datasets = {
            'KB Housing Price Index': 'price_index',
            'Jeonse Price Index': 'jeonse_index',
            'Monthly Rent Index': 'monthly_rent',
            'Transaction Volume': 'transaction_volume',
            'Market Sentiment': 'market_sentiment',
            'Regional Analysis': 'regional_analysis',
        }
        
        for name, dataset_id in kb_datasets.items():
            if self.kb:
                try:
                    success, filepath = self.kb.download_dataset(dataset_id)
                    if success:
                        self.track_data('Real Estate', name, 'KB Land', 'Monthly', 
                                      'Downloaded', filepath)
                        logger.info(f"✓ {name} downloaded")
                    else:
                        self.track_data('Real Estate', name, 'KB Land', 'Monthly', 
                                      'Failed', None)
                except Exception as e:
                    self.track_data('Real Estate', name, 'KB Land', 'Monthly', 
                                  f'Error: {str(e)}', None)
            
            time.sleep(0.5)
        
        logger.info("\n" + "="*60)
        logger.info("COLLECTING GLOBAL DATA (FRED)")
        logger.info("="*60)
        
        # FRED indicators (already working)
        global_indicators = {
            'US Federal Funds Rate': 'DFF',
            'US 10-Year Treasury': 'DGS10',
            'VIX Index': 'VIXCLS',
            'DXY Dollar Index': 'DTWEXBGS',
            'US GDP Growth': 'A191RL1Q225SBEA',
            'China GDP': 'NYGDPMKTPCDWLD',
            'WTI Oil Price': 'DCOILWTICO',
            'Brent Oil Price': 'DCOILBRENTEU',
        }
        
        for indicator_name, series_id in global_indicators.items():
            if self.fred:
                try:
                    data = self.fred.fetch_data(series_id, '2010-01-01', '2024-12-31')
                    if data['success']:
                        df = pd.DataFrame(data['data'])
                        filepath = output_dir / f"fred_{indicator_name.lower().replace(' ', '_')}.csv"
                        df.to_csv(filepath, index=False)
                        self.track_data('Global', indicator_name, 'FRED', 'Various', 
                                      'Downloaded', str(filepath))
                        logger.info(f"✓ {indicator_name} downloaded")
                    else:
                        self.track_data('Global', indicator_name, 'FRED', 'Various', 
                                      'No data', None)
                except Exception as e:
                    self.track_data('Global', indicator_name, 'FRED', 'Various', 
                                  f'Error: {str(e)}', None)
            
            time.sleep(0.5)
    
    def generate_report(self):
        """Generate final data collection report"""
        logger.info("\n" + "="*60)
        logger.info("GENERATING DATA COLLECTION REPORT")
        logger.info("="*60)
        
        # Create DataFrame from tracker
        df = pd.DataFrame(self.data_tracker)
        
        # Save main tracker CSV
        tracker_file = output_dir / 'data_collection_tracker_fixed.csv'
        df.to_csv(tracker_file, index=False, encoding='utf-8-sig')
        logger.info(f"✓ Data tracker saved to: {tracker_file}")
        
        # Generate summary statistics
        summary = df['Status'].value_counts()
        
        print("\n" + "="*60)
        print("DATA COLLECTION SUMMARY (FIXED)")
        print("="*60)
        print(f"Total indicators attempted: {len(df)}")
        print("\nStatus breakdown:")
        for status, count in summary.items():
            if 'Downloaded' in status:
                print(f"  ✓ {status}: {count}")
            else:
                print(f"  ✗ {status}: {count}")
        
        # Show successful downloads
        downloaded = df[df['Status'] == 'Downloaded']
        if len(downloaded) > 0:
            print("\n✓ Successfully Downloaded:")
            for _, row in downloaded.iterrows():
                print(f"  - {row['Indicator']} ({row['Source']})")
        
        return df

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("KOREAN REAL ESTATE MARKET RESEARCH DATA COLLECTION (FIXED)")
    print("Using Correct BOK Series Codes")
    print("Data Period: January 2010 - December 2024")
    print("="*80)
    
    collector = FixedResearchDataCollector()
    
    # Collect data with correct codes
    collector.collect_bok_data_fixed()
    collector.discover_kosis_tables()
    collector.collect_kb_and_global_data()
    
    # Generate final report
    tracker_df = collector.generate_report()
    
    print("\n✅ Data collection complete!")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print("📊 Files generated:")
    print("  - data_collection_tracker_fixed.csv (tracking file)")
    print("  - Individual data files in research_data_fixed/ folder")
    
    return tracker_df

if __name__ == "__main__":
    tracker = main()