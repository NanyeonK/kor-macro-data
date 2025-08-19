"""
BOK Data Collection with Correct Statistical Codes and Item Codes
Data Period: January 2010 - December 2024
"""

import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Create output directory
output_dir = Path('bok_data_final')
output_dir.mkdir(exist_ok=True)

class BOKDataCollector:
    def __init__(self):
        self.api_key = 'XJ9KI67DWCNIL35PBE9W'
        self.base_url = 'https://ecos.bok.or.kr/api'
        self.start_date = '20100101'
        self.end_date = '20241231'
        self.data_tracker = []
        
    def fetch_bok_data(self, stat_code, item_code, cycle, start_date, end_date):
        """Fetch data from BOK API with proper parameters"""
        # Construct URL based on whether item_code is provided
        if item_code:
            url = f"{self.base_url}/StatisticSearch/{self.api_key}/xml/kr/1/100000/{stat_code}/{cycle}/{start_date}/{end_date}/{item_code}"
        else:
            url = f"{self.base_url}/StatisticSearch/{self.api_key}/xml/kr/1/100000/{stat_code}/{cycle}/{start_date}/{end_date}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.text)
            
            # Check for errors
            result = root.find('.//RESULT')
            if result is not None:
                code = result.find('CODE').text if result.find('CODE') is not None else ''
                message = result.find('MESSAGE').text if result.find('MESSAGE') is not None else ''
                if code != '000':
                    logger.warning(f"API Error {code}: {message}")
                    return None
            
            # Extract data
            data = []
            for row in root.findall('.//row'):
                record = {}
                for child in row:
                    record[child.tag] = child.text
                if record:
                    data.append(record)
            
            return data if data else None
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def track_data(self, indicator, stat_code, item_code, status, filepath=None):
        """Track data collection status"""
        self.data_tracker.append({
            'Indicator': indicator,
            'STAT_CODE': stat_code,
            'ITEM_CODE': item_code,
            'Status': status,
            'Filepath': filepath if filepath else 'Not downloaded',
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    def collect_all_data(self):
        """Collect all BOK data with correct codes"""
        logger.info("="*60)
        logger.info("COLLECTING BOK DATA WITH CORRECT CODES")
        logger.info("="*60)
        
        # Define statistics with correct codes
        bok_statistics = [
            # Basic economic indicators
            {'name': 'Base Rate', 'stat_code': '722Y001', 'item_code': '0101000', 'cycle': 'D'},
            {'name': 'USD/KRW Exchange Rate', 'stat_code': '731Y001', 'item_code': '0000001', 'cycle': 'D'},
            {'name': 'CNY/KRW Exchange Rate', 'stat_code': '731Y001', 'item_code': '0000053', 'cycle': 'D'},
            {'name': 'EUR/KRW Exchange Rate', 'stat_code': '731Y001', 'item_code': '0000003', 'cycle': 'D'},
            
            # Money supply
            {'name': 'M2 Money Supply', 'stat_code': '101Y003', 'item_code': 'BBHS00', 'cycle': 'M'},
            
            # Price indices
            {'name': 'CPI Total', 'stat_code': '901Y009', 'item_code': '0', 'cycle': 'M'},
            
            # Housing prices - National
            {'name': 'Housing Price Index Total', 'stat_code': '901Y062', 'item_code': 'P63A', 'cycle': 'M'},
            {'name': 'Housing Price Index Apartments', 'stat_code': '901Y062', 'item_code': 'P63AC', 'cycle': 'M'},
            {'name': 'Housing Price Index Seoul Apartments', 'stat_code': '901Y062', 'item_code': 'P63ACA', 'cycle': 'M'},
            
            # Jeonse prices
            {'name': 'Jeonse Price Index Total', 'stat_code': '901Y063', 'item_code': 'P64A', 'cycle': 'M'},
            {'name': 'Jeonse Price Index Apartments', 'stat_code': '901Y063', 'item_code': 'P64AC', 'cycle': 'M'},
            {'name': 'Jeonse Price Index Seoul Apartments', 'stat_code': '901Y063', 'item_code': 'P64ACA', 'cycle': 'M'},
            
            # Household debt
            {'name': 'Household Credit Total', 'stat_code': '151Y001', 'item_code': '1000000', 'cycle': 'Q'},
            {'name': 'Household Loans', 'stat_code': '151Y001', 'item_code': '1100000', 'cycle': 'Q'},
            
            # Bank loans
            {'name': 'Bank Total Loans', 'stat_code': '104Y016', 'item_code': 'BDCA1', 'cycle': 'M'},
        ]
        
        # Collect each statistic
        for stat in bok_statistics:
            logger.info(f"\nFetching {stat['name']} ({stat['stat_code']}/{stat['item_code']})...")
            
            # Determine date range based on cycle
            if stat['cycle'] == 'D':
                # Daily data - fetch in yearly chunks to avoid too much data
                all_data = []
                for year in range(2010, 2025):
                    start = f"{year}0101"
                    end = f"{year}1231" if year < 2024 else self.end_date
                    
                    data = self.fetch_bok_data(
                        stat['stat_code'], 
                        stat['item_code'], 
                        stat['cycle'],
                        start,
                        end
                    )
                    
                    if data:
                        all_data.extend(data)
                    time.sleep(0.5)  # Rate limiting
                
                data = all_data if all_data else None
                
            else:
                # Monthly/Quarterly data - fetch all at once
                data = self.fetch_bok_data(
                    stat['stat_code'], 
                    stat['item_code'], 
                    stat['cycle'],
                    self.start_date,
                    self.end_date
                )
            
            if data:
                # Save to CSV
                df = pd.DataFrame(data)
                filename = stat['name'].lower().replace(' ', '_').replace('/', '_')
                filepath = output_dir / f"bok_{filename}.csv"
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                
                self.track_data(
                    stat['name'],
                    stat['stat_code'],
                    stat['item_code'],
                    'Downloaded',
                    str(filepath)
                )
                logger.info(f"✓ {stat['name']} downloaded - {len(df)} records")
            else:
                self.track_data(
                    stat['name'],
                    stat['stat_code'],
                    stat['item_code'],
                    'No data',
                    None
                )
                logger.warning(f"✗ {stat['name']} - No data available")
            
            time.sleep(1)  # Rate limiting between requests
    
    def generate_report(self):
        """Generate data collection report"""
        logger.info("\n" + "="*60)
        logger.info("GENERATING REPORT")
        logger.info("="*60)
        
        # Create DataFrame from tracker
        df = pd.DataFrame(self.data_tracker)
        
        # Save tracker
        tracker_file = output_dir / 'bok_collection_tracker.csv'
        df.to_csv(tracker_file, index=False, encoding='utf-8-sig')
        logger.info(f"✓ Tracker saved to: {tracker_file}")
        
        # Summary
        summary = df['Status'].value_counts()
        
        print("\n" + "="*60)
        print("BOK DATA COLLECTION SUMMARY")
        print("="*60)
        print(f"Total indicators: {len(df)}")
        print("\nStatus breakdown:")
        for status, count in summary.items():
            if status == 'Downloaded':
                print(f"  ✓ {status}: {count}")
            else:
                print(f"  ✗ {status}: {count}")
        
        # List successful downloads
        downloaded = df[df['Status'] == 'Downloaded']
        if len(downloaded) > 0:
            print("\n✓ Successfully Downloaded:")
            for _, row in downloaded.iterrows():
                print(f"  - {row['Indicator']} ({row['STAT_CODE']}/{row['ITEM_CODE']})")
        
        return df

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("BOK DATA COLLECTION WITH CORRECT CODES")
    print("Data Period: January 2010 - December 2024")
    print("="*80)
    
    collector = BOKDataCollector()
    collector.collect_all_data()
    tracker_df = collector.generate_report()
    
    print(f"\n✅ Collection complete!")
    print(f"📁 Output directory: {output_dir.absolute()}")
    
    return tracker_df

if __name__ == "__main__":
    tracker = main()