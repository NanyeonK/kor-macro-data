"""KB Land (KB부동산) Web Scraper Connector"""

import os
import time
import json
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # BeautifulSoup is optional for web scraping
# Selenium imports - optional for dynamic content
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
from .base import BaseConnector
import logging

logger = logging.getLogger(__name__)

class KBLandConnector(BaseConnector):
    """Connector for KB Land real estate data"""
    
    # KB Land main data categories
    DATA_CATEGORIES = {
        'apartment_price': {
            'name': 'Apartment Price Trends',
            'url': 'https://data.kbland.kr/kbstats/wmh',
            'description': 'KB apartment price index and trends'
        },
        'jeonse_rate': {
            'name': 'Jeonse Rate Trends', 
            'url': 'https://data.kbland.kr/kbstats/wjs',
            'description': 'Jeonse (key money deposit) rate trends'
        },
        'transaction_volume': {
            'name': 'Transaction Volume',
            'url': 'https://data.kbland.kr/kbstats/wmt',
            'description': 'Real estate transaction volume statistics'
        },
        'regional_price': {
            'name': 'Regional Price Data',
            'url': 'https://data.kbland.kr/kbstats/wsr',
            'description': 'Regional real estate price comparisons'
        },
        'market_trends': {
            'name': 'Market Trends',
            'url': 'https://data.kbland.kr/kbstats/wmi',
            'description': 'Overall real estate market indicators'
        },
        'rental_trends': {
            'name': 'Rental Market Trends',
            'url': 'https://data.kbland.kr/kbstats/wrt',
            'description': 'Monthly rent and jeonse trends'
        }
    }
    
    def __init__(self, use_selenium=False):
        super().__init__('KBLand')
        self.base_url = 'https://data.kbland.kr'
        self.use_selenium = use_selenium and SELENIUM_AVAILABLE
        self.driver = None
        
        if use_selenium and not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available. Install with: pip install selenium webdriver-manager")
        
    def get_api_key(self) -> str:
        """KB Land doesn't require API key for public data"""
        return ""
    
    def get_base_url(self) -> str:
        return self.base_url
    
    def _init_selenium_driver(self):
        """Initialize Selenium WebDriver for dynamic content"""
        if not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available")
            return
            
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("Selenium WebDriver initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Selenium: {e}")
                self.use_selenium = False
    
    def _close_driver(self):
        """Close Selenium driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def list_datasets(self) -> List[Dict]:
        """List available KB Land datasets"""
        datasets = []
        for key, info in self.DATA_CATEGORIES.items():
            datasets.append({
                'id': key,
                'name': info['name'],
                'description': info['description'],
                'url': info['url'],
                'source': 'KB Land'
            })
        return datasets
    
    def fetch_data(self, dataset_id: str, **params) -> Dict:
        """
        Fetch data from KB Land website
        
        Args:
            dataset_id: Category ID from DATA_CATEGORIES
            params: Additional parameters like region, period, etc.
        """
        if dataset_id not in self.DATA_CATEGORIES:
            return {
                'success': False,
                'message': f'Unknown dataset: {dataset_id}'
            }
        
        category = self.DATA_CATEGORIES[dataset_id]
        
        if self.use_selenium:
            return self._fetch_with_selenium(category, **params)
        else:
            return self._fetch_with_requests(category, **params)
    
    def _fetch_with_requests(self, category: Dict, **params) -> Dict:
        """Fetch data using requests and BeautifulSoup"""
        try:
            # Make request to KB Land
            response = requests.get(
                category['url'],
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                timeout=30
            )
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data based on category
            data = self._extract_data_from_html(soup, category['name'])
            
            return {
                'success': True,
                'dataset': category['name'],
                'data': data,
                'count': len(data) if isinstance(data, list) else 1,
                'source': 'KB Land',
                'url': category['url']
            }
            
        except Exception as e:
            logger.error(f"Error fetching KB Land data: {e}")
            return {
                'success': False,
                'dataset': category['name'],
                'message': str(e)
            }
    
    def _fetch_with_selenium(self, category: Dict, **params) -> Dict:
        """Fetch data using Selenium for dynamic content"""
        try:
            self._init_selenium_driver()
            if not self.driver:
                return self._fetch_with_requests(category, **params)
            
            # Navigate to page
            self.driver.get(category['url'])
            
            # Wait for content to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "data-content"))
            )
            
            # Extract data
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            data = self._extract_data_from_html(soup, category['name'])
            
            return {
                'success': True,
                'dataset': category['name'],
                'data': data,
                'count': len(data) if isinstance(data, list) else 1,
                'source': 'KB Land',
                'url': category['url']
            }
            
        except Exception as e:
            logger.error(f"Error with Selenium: {e}")
            return {
                'success': False,
                'dataset': category['name'],
                'message': str(e)
            }
    
    def _extract_data_from_html(self, soup: BeautifulSoup, category_name: str) -> List[Dict]:
        """Extract structured data from HTML"""
        data = []
        
        # Look for data tables
        tables = soup.find_all('table', class_=['data-table', 'stats-table', 'table'])
        
        for table in tables:
            # Extract headers
            headers = []
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            
            # Extract rows
            tbody = table.find('tbody')
            if tbody:
                for row in tbody.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        row_data = {}
                        for i, cell in enumerate(cells):
                            key = headers[i] if i < len(headers) else f'col_{i}'
                            row_data[key] = cell.get_text(strip=True)
                        
                        if row_data:
                            data.append(row_data)
        
        # If no tables found, look for other data structures
        if not data:
            # Look for chart data in scripts
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'chartData' in script.string:
                    # Try to extract JSON data from script
                    try:
                        import re
                        json_pattern = r'chartData\s*=\s*({.*?});'
                        match = re.search(json_pattern, script.string, re.DOTALL)
                        if match:
                            chart_data = json.loads(match.group(1))
                            if isinstance(chart_data, list):
                                data.extend(chart_data)
                            else:
                                data.append(chart_data)
                    except:
                        pass
        
        return data
    
    def get_apartment_price_index(self, region: str = 'seoul', period: str = 'monthly'):
        """Get KB apartment price index data"""
        return self.fetch_data('apartment_price', region=region, period=period)
    
    def get_jeonse_rate(self, region: str = 'seoul'):
        """Get jeonse rate trends"""
        return self.fetch_data('jeonse_rate', region=region)
    
    def get_transaction_volume(self, region: str = 'seoul', year: int = 2024):
        """Get real estate transaction volume"""
        return self.fetch_data('transaction_volume', region=region, year=year)
    
    def get_market_trends(self):
        """Get overall market trend indicators"""
        return self.fetch_data('market_trends')
    
    def crawl_all_categories(self, save_to_csv: bool = True) -> Dict[str, Any]:
        """
        Crawl all available KB Land data categories
        
        Returns:
            Dictionary with all crawled data
        """
        all_data = {}
        
        for category_id, category_info in self.DATA_CATEGORIES.items():
            logger.info(f"Crawling {category_info['name']}...")
            
            result = self.fetch_data(category_id)
            
            if result['success']:
                all_data[category_id] = result
                
                # Save to CSV if requested
                if save_to_csv and result['data']:
                    df = pd.DataFrame(result['data'])
                    csv_path = Path('data_exports/csv') / f'kbland_{category_id}.csv'
                    csv_path.parent.mkdir(parents=True, exist_ok=True)
                    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                    logger.info(f"  Saved to {csv_path}")
            else:
                logger.warning(f"  Failed to crawl {category_info['name']}: {result.get('message')}")
        
        # Close Selenium driver if used
        self._close_driver()
        
        return all_data
    
    def search_by_region(self, region: str) -> List[Dict]:
        """
        Search all datasets for specific region data
        
        Args:
            region: Region name (e.g., 'seoul', 'gangnam', 'busan')
        """
        results = []
        
        for category_id in self.DATA_CATEGORIES:
            data = self.fetch_data(category_id, region=region)
            if data['success']:
                results.append({
                    'category': category_id,
                    'name': self.DATA_CATEGORIES[category_id]['name'],
                    'data_count': data['count'],
                    'data': data['data']
                })
        
        return results