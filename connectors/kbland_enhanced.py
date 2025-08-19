"""Enhanced KB Land Connector with Excel/CSV download support"""

import os
import time
import json
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

logger = logging.getLogger(__name__)

class KBLandEnhancedConnector:
    """Enhanced KB Land connector with file download capabilities"""
    
    # KB Land Data Catalog - Comprehensive list
    KB_DATA_CATALOG = {
        'price_index': {
            'name': 'KB Housing Price Index',
            'korean': 'KB주택가격지수',
            'url': 'https://data.kbland.kr/kbstats/wmh',
            'format': 'Excel',
            'frequency': 'Monthly',
            'data_types': [
                'Apartment price index (아파트)',
                'House price index (단독주택)',
                'Row house price index (연립주택)',
                'National composite index (전국종합)'
            ]
        },
        'jeonse_index': {
            'name': 'KB Jeonse Price Index',
            'korean': 'KB전세가격지수',
            'url': 'https://data.kbland.kr/kbstats/wjs',
            'format': 'Excel',
            'frequency': 'Monthly',
            'data_types': [
                'Jeonse price index (전세가격지수)',
                'Jeonse ratio (전세가율)',
                'Regional jeonse trends'
            ]
        },
        'monthly_rent': {
            'name': 'KB Monthly Rent Index',
            'korean': 'KB월세가격지수',
            'url': 'https://data.kbland.kr/kbstats/wmr',
            'format': 'Excel',
            'frequency': 'Monthly',
            'data_types': [
                'Monthly rent index',
                'Deposit conversion rate',
                'Regional rent trends'
            ]
        },
        'transaction_volume': {
            'name': 'Real Estate Transaction Volume',
            'korean': '부동산거래량',
            'url': 'https://data.kbland.kr/kbstats/wmt',
            'format': 'Excel/CSV',
            'frequency': 'Monthly',
            'data_types': [
                'Transaction count by region',
                'Transaction volume by type',
                'YoY comparison'
            ]
        },
        'market_sentiment': {
            'name': 'Market Sentiment Index',
            'korean': '시장심리지수',
            'url': 'https://data.kbland.kr/kbstats/wms',
            'format': 'Excel',
            'frequency': 'Monthly',
            'data_types': [
                'Consumer sentiment',
                'Expert outlook',
                'Price expectation'
            ]
        },
        'regional_analysis': {
            'name': 'Regional Market Analysis',
            'korean': '지역별 시장분석',
            'url': 'https://data.kbland.kr/kbstats/wra',
            'format': 'Excel',
            'frequency': 'Monthly',
            'data_types': [
                'Seoul 25 districts',
                'Gyeonggi 31 cities',
                'Metropolitan cities',
                'Price rankings'
            ]
        },
        'apartment_ranking': {
            'name': 'Apartment Complex Rankings',
            'korean': '아파트 단지 순위',
            'url': 'https://data.kbland.kr/kbstats/war',
            'format': 'CSV',
            'frequency': 'Weekly',
            'data_types': [
                'Top 100 by price',
                'Top gainers/losers',
                'Transaction leaders'
            ]
        },
        'office_retail': {
            'name': 'Office & Retail Market',
            'korean': '오피스/상가 시장',
            'url': 'https://data.kbland.kr/kbstats/wor',
            'format': 'Excel',
            'frequency': 'Quarterly',
            'data_types': [
                'Office rent index',
                'Retail space prices',
                'Vacancy rates'
            ]
        },
        'land_price': {
            'name': 'Land Price Index',
            'korean': '토지가격지수',
            'url': 'https://data.kbland.kr/kbstats/wlp',
            'format': 'Excel',
            'frequency': 'Quarterly',
            'data_types': [
                'Residential land',
                'Commercial land',
                'Industrial land'
            ]
        },
        'policy_impact': {
            'name': 'Policy Impact Analysis',
            'korean': '정책영향분석',
            'url': 'https://data.kbland.kr/kbstats/wpi',
            'format': 'PDF/Excel',
            'frequency': 'As needed',
            'data_types': [
                'Tax policy effects',
                'Regulation impacts',
                'Market interventions'
            ]
        }
    }
    
    def __init__(self, download_dir: str = None):
        self.download_dir = Path(download_dir) if download_dir else Path('data_exports/kb_land')
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.driver = None
        
    def init_driver(self, headless: bool = True):
        """Initialize Selenium driver with download capabilities"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Set download directory
        prefs = {
            'download.default_directory': str(self.download_dir.absolute()),
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        }
        chrome_options.add_experimental_option('prefs', prefs)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Selenium driver initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize driver: {e}")
            return False
    
    def close_driver(self):
        """Close Selenium driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def get_catalog(self) -> pd.DataFrame:
        """Return KB Land data catalog as DataFrame"""
        catalog_list = []
        
        for key, info in self.KB_DATA_CATALOG.items():
            catalog_list.append({
                'ID': key,
                'Name': info['name'],
                'Korean': info['korean'],
                'Format': info['format'],
                'Frequency': info['frequency'],
                'URL': info['url'],
                'Data Types': ', '.join(info['data_types'])
            })
        
        return pd.DataFrame(catalog_list)
    
    def download_dataset(self, dataset_id: str) -> Tuple[bool, str]:
        """
        Download a specific dataset from KB Land
        
        Returns:
            Tuple of (success, file_path or error_message)
        """
        if dataset_id not in self.KB_DATA_CATALOG:
            return False, f"Unknown dataset: {dataset_id}"
        
        dataset = self.KB_DATA_CATALOG[dataset_id]
        
        # Try direct download first (for Excel/CSV links)
        success, result = self._try_direct_download(dataset)
        if success:
            return True, result
        
        # Use Selenium for dynamic content
        if not self.driver:
            if not self.init_driver():
                return False, "Failed to initialize Selenium driver"
        
        try:
            logger.info(f"Downloading {dataset['name']} from {dataset['url']}")
            self.driver.get(dataset['url'])
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Look for download buttons/links
            download_selectors = [
                "//a[contains(@href, '.xlsx')]",
                "//a[contains(@href, '.xls')]",
                "//a[contains(@href, '.csv')]",
                "//button[contains(text(), '다운로드')]",
                "//button[contains(text(), 'Download')]",
                "//a[contains(text(), 'Excel')]",
                "//a[contains(@class, 'download')]"
            ]
            
            for selector in download_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        elements[0].click()
                        time.sleep(3)  # Wait for download
                        
                        # Check if file was downloaded
                        downloaded_file = self._get_latest_download()
                        if downloaded_file:
                            logger.info(f"Downloaded: {downloaded_file}")
                            return True, str(downloaded_file)
                except:
                    continue
            
            # If no download link found, extract table data
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            if tables:
                return self._extract_tables_to_csv(tables, dataset_id)
            
            return False, "No downloadable data found"
            
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return False, str(e)
    
    def _try_direct_download(self, dataset: Dict) -> Tuple[bool, str]:
        """Try to download file directly without Selenium"""
        try:
            # Common Excel/CSV download patterns for KB Land
            download_patterns = [
                f"{dataset['url']}/download",
                f"{dataset['url']}.xlsx",
                f"{dataset['url']}/export",
                dataset['url'].replace('/kbstats/', '/download/')
            ]
            
            for pattern in download_patterns:
                try:
                    response = requests.head(pattern, timeout=5)
                    if response.status_code == 200:
                        # Download file
                        response = requests.get(pattern)
                        
                        # Determine file extension
                        content_type = response.headers.get('content-type', '')
                        if 'excel' in content_type or 'spreadsheet' in content_type:
                            ext = '.xlsx'
                        elif 'csv' in content_type:
                            ext = '.csv'
                        else:
                            ext = '.xlsx'  # Default
                        
                        # Save file
                        filename = f"{dataset.get('korean', 'data')}_{datetime.now().strftime('%Y%m%d')}{ext}"
                        filepath = self.download_dir / filename
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        
                        logger.info(f"Direct download successful: {filepath}")
                        return True, str(filepath)
                except:
                    continue
                    
        except Exception as e:
            logger.debug(f"Direct download failed: {e}")
        
        return False, "Direct download not available"
    
    def _extract_tables_to_csv(self, tables, dataset_id: str) -> Tuple[bool, str]:
        """Extract HTML tables to CSV"""
        try:
            all_data = []
            
            for table in tables:
                # Convert table to pandas DataFrame
                table_html = table.get_attribute('outerHTML')
                df = pd.read_html(table_html)[0]
                all_data.append(df)
            
            if all_data:
                # Combine all tables
                combined_df = pd.concat(all_data, ignore_index=True)
                
                # Save to CSV
                filename = f"{dataset_id}_{datetime.now().strftime('%Y%m%d')}.csv"
                filepath = self.download_dir / filename
                combined_df.to_csv(filepath, index=False, encoding='utf-8-sig')
                
                logger.info(f"Extracted table data to: {filepath}")
                return True, str(filepath)
                
        except Exception as e:
            logger.error(f"Table extraction failed: {e}")
        
        return False, "Failed to extract table data"
    
    def _get_latest_download(self) -> Optional[Path]:
        """Get the most recently downloaded file"""
        try:
            files = list(self.download_dir.glob('*'))
            if not files:
                return None
            
            # Get most recent file
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            
            # Check if it was downloaded in the last 10 seconds
            if time.time() - latest_file.stat().st_mtime < 10:
                return latest_file
                
        except Exception as e:
            logger.error(f"Error checking downloads: {e}")
        
        return None
    
    def download_all_datasets(self) -> Dict[str, Any]:
        """Download all available KB Land datasets"""
        results = {}
        
        if not self.driver:
            self.init_driver()
        
        for dataset_id in self.KB_DATA_CATALOG:
            logger.info(f"Downloading {dataset_id}...")
            success, result = self.download_dataset(dataset_id)
            
            results[dataset_id] = {
                'success': success,
                'result': result,
                'dataset': self.KB_DATA_CATALOG[dataset_id]['name']
            }
            
            # Pause between downloads
            time.sleep(2)
        
        self.close_driver()
        
        # Generate summary
        summary = {
            'total': len(results),
            'successful': sum(1 for r in results.values() if r['success']),
            'failed': sum(1 for r in results.values() if not r['success']),
            'results': results
        }
        
        # Save summary
        summary_path = self.download_dir / 'download_summary.json'
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Download summary saved to: {summary_path}")
        
        return summary