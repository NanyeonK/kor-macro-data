"""Bank of Korea ECOS API Connector"""

import os
from typing import Dict, List, Optional
from .base import BaseConnector

class BOKConnector(BaseConnector):
    """Connector for Bank of Korea Economic Statistics System (ECOS)"""
    
    # Popular BOK statistics codes
    STAT_CODES = {
        'base_rate': '722Y001',  # Base rate
        'exchange_rate': '731Y001',  # Exchange rates
        'money_supply': '101Y004',  # Money supply (M2)
        'gdp': '200Y001',  # GDP
        'cpi': '901Y009',  # Consumer Price Index
        'housing_price': '901Y067',  # Housing price index
        'household_debt': '008Y002',  # Household debt
        'unemployment': '901Y016',  # Unemployment rate
    }
    
    def __init__(self):
        super().__init__('BOK_ECOS')
        self.api_key = self.get_api_key()
        self.base_url = self.get_base_url()
        self.lang = os.getenv('BOK_LANG', 'en')
        
    def get_api_key(self) -> str:
        key = os.getenv('BOK_API_KEY')
        if not key:
            raise ValueError("BOK_API_KEY not found in environment")
        return key
    
    def get_base_url(self) -> str:
        return os.getenv('BOK_API_URL', 'https://ecos.bok.or.kr/api/')
    
    def list_datasets(self) -> List[Dict]:
        """List available BOK datasets"""
        datasets = []
        for name, code in self.STAT_CODES.items():
            datasets.append({
                'id': code,
                'name': name.replace('_', ' ').title(),
                'description': f'BOK {name} statistics',
                'source': 'Bank of Korea'
            })
        return datasets
    
    def fetch_data(self, dataset_id: str, 
                  start_date: str = '20200101',
                  end_date: str = '20241231',
                  period: str = 'M',  # M: Monthly, Q: Quarterly, Y: Yearly
                  **params) -> Dict:
        """
        Fetch data from BOK ECOS API
        
        Args:
            dataset_id: Statistics code (e.g., '722Y001' for base rate)
            start_date: Start date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format) 
            period: Period type (M/Q/Y)
        """
        # BOK ECOS API endpoint format:
        # /StatisticSearch/{API_KEY}/{LANG}/{START}/{END}/{STAT_CODE}/{PERIOD}/{START_DATE}/{END_DATE}
        
        url = f"{self.base_url}StatisticSearch/{self.api_key}/json/{self.lang}/1/10000/{dataset_id}/{period}/{start_date}/{end_date}"
        
        result = self._make_request(url)
        
        # Parse BOK response
        if 'StatisticSearch' in result:
            data = result['StatisticSearch']
            if 'row' in data:
                return {
                    'success': True,
                    'dataset_id': dataset_id,
                    'period': period,
                    'data': data['row'],
                    'count': len(data['row'])
                }
        
        return {
            'success': False,
            'dataset_id': dataset_id,
            'message': 'No data found',
            'raw_response': result
        }
    
    def get_base_rate(self, start_date: str = '20200101', end_date: str = '20241231'):
        """Get Bank of Korea base rate"""
        return self.fetch_data(self.STAT_CODES['base_rate'], start_date, end_date, 'M')
    
    def get_exchange_rate(self, start_date: str = '20200101', end_date: str = '20241231'):
        """Get USD/KRW exchange rate"""
        return self.fetch_data(self.STAT_CODES['exchange_rate'], start_date, end_date, 'D')
    
    def get_housing_price_index(self, start_date: str = '20200101', end_date: str = '20241231'):
        """Get housing price index"""
        return self.fetch_data(self.STAT_CODES['housing_price'], start_date, end_date, 'M')