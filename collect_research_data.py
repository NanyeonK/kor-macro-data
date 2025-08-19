"""
Comprehensive Data Collection for Korean Real Estate Market Research
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
output_dir = Path('research_data')
output_dir.mkdir(exist_ok=True)

class ResearchDataCollector:
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
    
    def collect_kb_housing_prices(self):
        """1. Dependent Variable - KB Housing Price Index"""
        logger.info("\n" + "="*60)
        logger.info("1. COLLECTING KB HOUSING PRICE INDEX")
        logger.info("="*60)
        
        if self.kb:
            try:
                # Download KB housing price index
                success, filepath = self.kb.download_dataset('price_index')
                if success:
                    self.track_data('Dependent Variable', 'KB Housing Price Index', 
                                  'KB Land', 'Monthly', 'Downloaded', filepath)
                    logger.info(f"✓ KB Housing Price Index downloaded: {filepath}")
                else:
                    self.track_data('Dependent Variable', 'KB Housing Price Index', 
                                  'KB Land', 'Monthly', 'Failed', None)
            except Exception as e:
                logger.error(f"✗ KB Housing Price Index failed: {e}")
                self.track_data('Dependent Variable', 'KB Housing Price Index', 
                              'KB Land', 'Monthly', 'Error', None)
        else:
            self.track_data('Dependent Variable', 'KB Housing Price Index', 
                          'KB Land', 'Monthly', 'Not available', None)
    
    def collect_macroeconomic_indicators(self):
        """2. Macroeconomic Variables from BOK"""
        logger.info("\n" + "="*60)
        logger.info("2. COLLECTING MACROECONOMIC INDICATORS")
        logger.info("="*60)
        
        # BOK indicators mapping
        bok_indicators = {
            # Economic Growth
            'GDP Growth Rate': ('200Y001', 'Q'),
            'Industrial Production Index': ('901Y002', 'M'),
            'Leading Index': ('901Y030', 'M'),
            'Coincident Index': ('901Y031', 'M'),
            
            # Price Indicators
            'Consumer Price Index': ('901Y009', 'M'),
            'Producer Price Index': ('404Y014', 'M'),
            'GDP Deflator': ('200Y004', 'Q'),
            
            # Employment (from KOSIS instead)
            'Unemployment Rate': ('901Y016', 'M'),
            'Employment Rate': ('901Y033', 'M'),
            
            # External Indicators
            'Current Account Balance': ('301Y001', 'M'),
            'Export Growth Rate': ('301Y013', 'M'),
            'Import Growth Rate': ('301Y014', 'M'),
            'Foreign Exchange Reserves': ('732Y001', 'M'),
        }
        
        for indicator_name, (series_id, frequency) in bok_indicators.items():
            if self.bok:
                try:
                    data = self.bok.fetch_data(series_id, self.start_date, self.end_date, frequency)
                    if data['success']:
                        # Save to CSV
                        df = pd.DataFrame(data['data'])
                        filepath = output_dir / f"bok_{indicator_name.lower().replace(' ', '_')}.csv"
                        df.to_csv(filepath, index=False)
                        self.track_data('Macroeconomic', indicator_name, 'BOK', 
                                      'Monthly' if frequency == 'M' else 'Quarterly', 
                                      'Downloaded', str(filepath))
                        logger.info(f"✓ {indicator_name} downloaded")
                    else:
                        self.track_data('Macroeconomic', indicator_name, 'BOK', 
                                      'Monthly' if frequency == 'M' else 'Quarterly', 
                                      'No data', None)
                        logger.warning(f"✗ {indicator_name}: No data available")
                except Exception as e:
                    self.track_data('Macroeconomic', indicator_name, 'BOK', 
                                  'Monthly' if frequency == 'M' else 'Quarterly', 
                                  'Error', None)
                    logger.error(f"✗ {indicator_name} error: {e}")
            else:
                self.track_data('Macroeconomic', indicator_name, 'BOK', 
                              'Monthly' if frequency == 'M' else 'Quarterly', 
                              'Not available', None)
            
            time.sleep(0.5)  # Rate limiting
    
    def collect_financial_market_variables(self):
        """3. Financial Market Variables"""
        logger.info("\n" + "="*60)
        logger.info("3. COLLECTING FINANCIAL MARKET VARIABLES")
        logger.info("="*60)
        
        # Interest rates from BOK
        interest_rates = {
            'Base Rate': ('722Y001', 'M'),
            '3-Year Treasury Bond': ('721Y001', 'M'),
            '5-Year Treasury Bond': ('721Y002', 'M'),
            '10-Year Treasury Bond': ('721Y003', 'M'),
            'CD Rate (91-day)': ('721Y017', 'M'),
            'Call Rate': ('721Y016', 'M'),
            'Housing Mortgage Rate': ('723Y001', 'M'),
            'Household Loan Rate': ('723Y003', 'M'),
        }
        
        for rate_name, (series_id, frequency) in interest_rates.items():
            if self.bok:
                try:
                    data = self.bok.fetch_data(series_id, self.start_date, self.end_date, frequency)
                    if data['success']:
                        df = pd.DataFrame(data['data'])
                        filepath = output_dir / f"bok_{rate_name.lower().replace(' ', '_')}.csv"
                        df.to_csv(filepath, index=False)
                        self.track_data('Financial Market', rate_name, 'BOK', 'Monthly', 
                                      'Downloaded', str(filepath))
                        logger.info(f"✓ {rate_name} downloaded")
                    else:
                        self.track_data('Financial Market', rate_name, 'BOK', 'Monthly', 
                                      'No data', None)
                except Exception as e:
                    self.track_data('Financial Market', rate_name, 'BOK', 'Monthly', 
                                  'Error', None)
                    logger.error(f"✗ {rate_name} error: {e}")
            
            time.sleep(0.5)
        
        # Stock market indices - These would need a different source
        stock_indices = ['KOSPI Index', 'KOSDAQ Index', 'Construction Index', 'Financial Index']
        for index in stock_indices:
            self.track_data('Financial Market', index, 'KRX', 'Monthly', 
                          'Not downloaded - KRX API needed', None)
        
        # Exchange rates from BOK
        exchange_rates = {
            'KRW/USD Exchange Rate': ('731Y001', 'M'),
            'KRW/JPY Exchange Rate': ('731Y002', 'M'),
            'KRW/CNY Exchange Rate': ('731Y003', 'M'),
            'Real Effective Exchange Rate': ('731Y004', 'M'),
        }
        
        for rate_name, (series_id, frequency) in exchange_rates.items():
            if self.bok:
                try:
                    data = self.bok.fetch_data(series_id, self.start_date, self.end_date, frequency)
                    if data['success']:
                        df = pd.DataFrame(data['data'])
                        filepath = output_dir / f"bok_{rate_name.lower().replace(' ', '_').replace('/', '_')}.csv"
                        df.to_csv(filepath, index=False)
                        self.track_data('Financial Market', rate_name, 'BOK', 'Monthly', 
                                      'Downloaded', str(filepath))
                        logger.info(f"✓ {rate_name} downloaded")
                    else:
                        self.track_data('Financial Market', rate_name, 'BOK', 'Monthly', 
                                      'No data', None)
                except Exception as e:
                    self.track_data('Financial Market', rate_name, 'BOK', 'Monthly', 
                                  'Error', None)
            
            time.sleep(0.5)
    
    def collect_real_estate_market_variables(self):
        """4. Real Estate Market Variables"""
        logger.info("\n" + "="*60)
        logger.info("4. COLLECTING REAL ESTATE MARKET VARIABLES")
        logger.info("="*60)
        
        # KB Land data
        kb_datasets = {
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
                        self.track_data('Real Estate Market', name, 'KB Land', 'Monthly', 
                                      'Downloaded', filepath)
                        logger.info(f"✓ {name} downloaded")
                    else:
                        self.track_data('Real Estate Market', name, 'KB Land', 'Monthly', 
                                      'Failed', None)
                except Exception as e:
                    self.track_data('Real Estate Market', name, 'KB Land', 'Monthly', 
                                  'Error', None)
            else:
                self.track_data('Real Estate Market', name, 'KB Land', 'Monthly', 
                              'Not available', None)
        
        # MOLIT data (would need separate API)
        molit_indicators = [
            'Housing Transaction Volume',
            'Apartment Transaction Volume',
            'Jeonse Transaction Volume',
            'Housing Permits',
            'Housing Starts',
            'Housing Completions',
            'Unsold Housing'
        ]
        
        for indicator in molit_indicators:
            self.track_data('Real Estate Market', indicator, 'MOLIT', 'Monthly', 
                          'Not downloaded - MOLIT API needed', None)
    
    def collect_household_debt_variables(self):
        """5. Household Debt and Financial Soundness"""
        logger.info("\n" + "="*60)
        logger.info("5. COLLECTING HOUSEHOLD DEBT VARIABLES")
        logger.info("="*60)
        
        # BOK household debt indicators
        debt_indicators = {
            'Household Credit Balance': ('451Y056', 'Q'),
            'Household Debt Growth Rate': ('451Y057', 'Q'),
            'Mortgage Balance': ('451Y058', 'M'),
            'Jeonse Loan Balance': ('451Y059', 'M'),
            'Household Debt-to-GDP Ratio': ('451Y060', 'Q'),
        }
        
        for indicator_name, (series_id, frequency) in debt_indicators.items():
            if self.bok:
                try:
                    data = self.bok.fetch_data(series_id, self.start_date, self.end_date, frequency)
                    if data['success']:
                        df = pd.DataFrame(data['data'])
                        filepath = output_dir / f"bok_{indicator_name.lower().replace(' ', '_')}.csv"
                        df.to_csv(filepath, index=False)
                        self.track_data('Household Debt', indicator_name, 'BOK', 
                                      'Quarterly' if frequency == 'Q' else 'Monthly', 
                                      'Downloaded', str(filepath))
                        logger.info(f"✓ {indicator_name} downloaded")
                    else:
                        self.track_data('Household Debt', indicator_name, 'BOK', 
                                      'Quarterly' if frequency == 'Q' else 'Monthly', 
                                      'No data', None)
                except Exception as e:
                    self.track_data('Household Debt', indicator_name, 'BOK', 
                                  'Quarterly' if frequency == 'Q' else 'Monthly', 
                                  'Error', None)
            
            time.sleep(0.5)
    
    def collect_sentiment_variables(self):
        """7. Sentiment and Expectation Variables"""
        logger.info("\n" + "="*60)
        logger.info("7. COLLECTING SENTIMENT VARIABLES")
        logger.info("="*60)
        
        # Consumer sentiment from BOK
        sentiment_indicators = {
            'Consumer Sentiment Index': ('511Y001', 'M'),
            'Housing Price Outlook CSI': ('511Y002', 'M'),
            'Housing Purchase Attitude': ('511Y003', 'M'),
        }
        
        for indicator_name, (series_id, frequency) in sentiment_indicators.items():
            if self.bok:
                try:
                    data = self.bok.fetch_data(series_id, self.start_date, self.end_date, frequency)
                    if data['success']:
                        df = pd.DataFrame(data['data'])
                        filepath = output_dir / f"bok_{indicator_name.lower().replace(' ', '_')}.csv"
                        df.to_csv(filepath, index=False)
                        self.track_data('Sentiment', indicator_name, 'BOK', 'Monthly', 
                                      'Downloaded', str(filepath))
                        logger.info(f"✓ {indicator_name} downloaded")
                    else:
                        self.track_data('Sentiment', indicator_name, 'BOK', 'Monthly', 
                                      'No data', None)
                except Exception as e:
                    self.track_data('Sentiment', indicator_name, 'BOK', 'Monthly', 
                                  'Error', None)
            
            time.sleep(0.5)
        
        # Google Trends and EPU Index would need separate APIs
        self.track_data('Sentiment', 'Google Search Trends', 'Google Trends', 'Monthly', 
                      'Not downloaded - Google Trends API needed', None)
        self.track_data('Sentiment', 'Economic Policy Uncertainty Index', 'EPU', 'Monthly', 
                      'Not downloaded - EPU API needed', None)
    
    def collect_population_variables(self):
        """8. Population and Social Variables from KOSIS"""
        logger.info("\n" + "="*60)
        logger.info("8. COLLECTING POPULATION VARIABLES")
        logger.info("="*60)
        
        # KOSIS population indicators
        population_indicators = {
            'Population Growth Rate': 'DT_1B040A3',
            'Working Age Population': 'DT_1B040A4',
            'Household Growth Rate': 'DT_1JC1501',
            'Single-Person Households': 'DT_1JC1502',
        }
        
        for indicator_name, table_id in population_indicators.items():
            if self.kosis:
                try:
                    data = self.kosis.fetch_data(table_id, '201001', '202412')
                    if data['success']:
                        df = pd.DataFrame(data['data'])
                        filepath = output_dir / f"kosis_{indicator_name.lower().replace(' ', '_')}.csv"
                        df.to_csv(filepath, index=False)
                        self.track_data('Population', indicator_name, 'KOSIS', 'Monthly', 
                                      'Downloaded', str(filepath))
                        logger.info(f"✓ {indicator_name} downloaded")
                    else:
                        self.track_data('Population', indicator_name, 'KOSIS', 'Monthly', 
                                      'No data', None)
                except Exception as e:
                    self.track_data('Population', indicator_name, 'KOSIS', 'Monthly', 
                                  'Error', None)
            else:
                self.track_data('Population', indicator_name, 'KOSIS', 'Monthly', 
                              'Not available', None)
            
            time.sleep(0.5)
    
    def collect_global_variables(self):
        """9. Global Variables from FRED"""
        logger.info("\n" + "="*60)
        logger.info("9. COLLECTING GLOBAL VARIABLES")
        logger.info("="*60)
        
        # FRED global indicators
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
                        self.track_data('Global', indicator_name, 'FRED', 'Monthly', 
                                      'Downloaded', str(filepath))
                        logger.info(f"✓ {indicator_name} downloaded")
                    else:
                        self.track_data('Global', indicator_name, 'FRED', 'Monthly', 
                                      'No data', None)
                except Exception as e:
                    self.track_data('Global', indicator_name, 'FRED', 'Monthly', 
                                  'Error', None)
            else:
                self.track_data('Global', indicator_name, 'FRED', 'Monthly', 
                              'Not available', None)
            
            time.sleep(0.5)
    
    def collect_policy_variables(self):
        """6. Policy Variables"""
        logger.info("\n" + "="*60)
        logger.info("6. COLLECTING POLICY VARIABLES")
        logger.info("="*60)
        
        # Policy variables need manual coding or specific government APIs
        policy_vars = [
            'Base Rate Change Dummy',
            'LTV Regulation Change',
            'DTI/DSR Regulation Change',
            'Speculative Area Designation',
            'Acquisition Tax Rate Change',
            'Property Tax Rate Change',
            'Comprehensive Real Estate Tax Change',
            'Capital Gains Tax Change',
            'Real Estate Policy Announcements',
            'Household Debt Management Plans',
        ]
        
        for policy in policy_vars:
            self.track_data('Policy', policy, 'Manual/Government', 'Event-based', 
                          'Not downloaded - Manual coding required', None)
    
    def generate_report(self):
        """Generate final data collection report"""
        logger.info("\n" + "="*60)
        logger.info("GENERATING DATA COLLECTION REPORT")
        logger.info("="*60)
        
        # Create DataFrame from tracker
        df = pd.DataFrame(self.data_tracker)
        
        # Save main tracker CSV
        tracker_file = output_dir / 'data_collection_tracker.csv'
        df.to_csv(tracker_file, index=False)
        logger.info(f"✓ Data tracker saved to: {tracker_file}")
        
        # Generate summary statistics
        summary = df['Status'].value_counts()
        
        print("\n" + "="*60)
        print("DATA COLLECTION SUMMARY")
        print("="*60)
        print(f"Total indicators requested: {len(df)}")
        print("\nStatus breakdown:")
        for status, count in summary.items():
            print(f"  {status}: {count}")
        
        # Create detailed report
        report = []
        report.append("KOREAN REAL ESTATE MARKET RESEARCH DATA COLLECTION REPORT")
        report.append("="*60)
        report.append(f"Collection Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Data Period: January 2010 - December 2024")
        report.append("")
        
        # Group by category
        for category in df['Category'].unique():
            cat_data = df[df['Category'] == category]
            report.append(f"\n{category.upper()}")
            report.append("-"*40)
            
            downloaded = cat_data[cat_data['Status'] == 'Downloaded']
            not_downloaded = cat_data[cat_data['Status'] != 'Downloaded']
            
            if len(downloaded) > 0:
                report.append(f"✓ Downloaded ({len(downloaded)} indicators):")
                for _, row in downloaded.iterrows():
                    report.append(f"  - {row['Indicator']} ({row['Source']})")
            
            if len(not_downloaded) > 0:
                report.append(f"✗ Not Downloaded ({len(not_downloaded)} indicators):")
                for _, row in not_downloaded.iterrows():
                    report.append(f"  - {row['Indicator']} ({row['Source']}) - {row['Status']}")
        
        # Save detailed report
        report_file = output_dir / 'data_collection_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        logger.info(f"✓ Detailed report saved to: {report_file}")
        
        return df

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("KOREAN REAL ESTATE MARKET RESEARCH DATA COLLECTION")
    print("Data Period: January 2010 - December 2024")
    print("="*80)
    
    collector = ResearchDataCollector()
    
    # Collect all data categories
    collector.collect_kb_housing_prices()
    collector.collect_macroeconomic_indicators()
    collector.collect_financial_market_variables()
    collector.collect_real_estate_market_variables()
    collector.collect_household_debt_variables()
    collector.collect_policy_variables()
    collector.collect_sentiment_variables()
    collector.collect_population_variables()
    collector.collect_global_variables()
    
    # Generate final report
    tracker_df = collector.generate_report()
    
    print("\n✅ Data collection complete!")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print("📊 Files generated:")
    print("  - data_collection_tracker.csv (main tracking file)")
    print("  - data_collection_report.txt (detailed report)")
    print("  - Individual data files in research_data/ folder")
    
    return tracker_df

if __name__ == "__main__":
    tracker = main()