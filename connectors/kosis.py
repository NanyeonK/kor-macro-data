"""KOSIS (Korean Statistical Information Service) API Connector"""

import os
import json
from typing import Dict, List, Optional
from .base import BaseConnector

class KOSISConnector(BaseConnector):
    """Connector for Korean Statistical Information Service"""
    
    # Popular KOSIS statistics
    STAT_TABLES = {
        'population': 'DT_1B040A3',  # Population statistics
        'household': 'DT_1JC1501',  # Household statistics  
        'employment': 'DT_1DA7001S',  # Employment rate
        'wages': 'DT_1J17001',  # Average wages
        'real_estate_transactions': 'DT_1YL2101',  # Real estate transactions
        'construction_permits': 'DT_1YL1601',  # Construction permits
        'apartment_prices': 'DT_1YL2001',  # Apartment prices
        'regional_gdp': 'DT_1C61',  # Regional GDP
    }
    
    def __init__(self):
        super().__init__('KOSIS')
        self.api_key = self.get_api_key()
        self.base_url = self.get_base_url()
        
    def get_api_key(self) -> str:
        key = os.getenv('KOSIS_API_KEY')
        if not key:
            raise ValueError("KOSIS_API_KEY not found in environment")
        return key
    
    def get_base_url(self) -> str:
        return os.getenv('KOSIS_API_URL', 'https://kosis.kr/openapi/')
    
    def list_datasets(self) -> List[Dict]:
        """List available KOSIS datasets"""
        datasets = []
        for name, table_id in self.STAT_TABLES.items():
            datasets.append({
                'id': table_id,
                'name': name.replace('_', ' ').title(),
                'description': f'KOSIS {name} statistics',
                'source': 'Korean Statistical Information Service'
            })
        return datasets
    
    def fetch_data(self, dataset_id: str,
                  start_period: str = '2020',
                  end_period: str = '2024',
                  **params) -> Dict:
        """
        Fetch data from KOSIS API
        
        Args:
            dataset_id: Table ID (e.g., 'DT_1B040A3')
            start_period: Start period (YYYY or YYYYMM)
            end_period: End period
        """
        
        # KOSIS API parameters
        api_params = {
            'method': 'getList',
            'apiKey': self.api_key,
            'itmId': 'ALL',
            'objL1': 'ALL',
            'objL2': '',
            'objL3': '',
            'objL4': '',
            'objL5': '',
            'objL6': '',
            'objL7': '',
            'objL8': '',
            'format': 'json',
            'jsonVD': 'Y',
            'prdSe': 'M',  # Period type
            'startPrdDe': start_period,
            'endPrdDe': end_period,
            'orgId': params.get('org_id', '101'),
            'tblId': dataset_id,
        }
        
        url = f"{self.base_url}Param/statisticsParameterData.do"
        
        result = self._make_request(url, params=api_params)
        
        # Parse KOSIS response
        if isinstance(result, list) and len(result) > 0:
            return {
                'success': True,
                'dataset_id': dataset_id,
                'data': result,
                'count': len(result)
            }
        
        return {
            'success': False,
            'dataset_id': dataset_id,
            'message': 'No data found',
            'raw_response': result
        }
    
    def get_population_stats(self, start_period: str = '202001', end_period: str = '202412'):
        """Get population statistics"""
        return self.fetch_data(self.STAT_TABLES['population'], start_period, end_period)
    
    def get_real_estate_transactions(self, start_period: str = '202001', end_period: str = '202412'):
        """Get real estate transaction statistics"""
        return self.fetch_data(self.STAT_TABLES['real_estate_transactions'], start_period, end_period)
    
    def get_apartment_prices(self, start_period: str = '202001', end_period: str = '202412'):
        """Get apartment price statistics"""
        return self.fetch_data(self.STAT_TABLES['apartment_prices'], start_period, end_period)