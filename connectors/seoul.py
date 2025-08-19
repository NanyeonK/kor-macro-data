"""Seoul Open Data Plaza API Connector"""

import os
from typing import Dict, List, Optional
from .base import BaseConnector

class SeoulDataConnector(BaseConnector):
    """Connector for Seoul Open Data Plaza"""
    
    # Popular Seoul datasets
    DATASETS = {
        'real_estate_prices': 'tbLnOpendataRtmsV',  # Real estate transaction prices
        'population': 'PopulationDensityOfSeoul',  # Population density
        'public_parking': 'GetParkInfo',  # Public parking information
        'air_quality': 'RealtimeCityAir',  # Real-time air quality
        'subway_passenger': 'CardSubwayStatsNew',  # Subway passenger statistics
        'apartment_rent': 'tbLnOpendataRentV',  # Apartment rent prices
        'commercial_rent': 'landBizInfo',  # Commercial property information
        'bus_route': 'busRouteInfo',  # Bus route information
    }
    
    def __init__(self):
        super().__init__('Seoul_OpenData')
        self.api_key = self.get_api_key()
        self.base_url = self.get_base_url()
        
    def get_api_key(self) -> str:
        key = os.getenv('SEOUL_API_KEY')
        if not key:
            raise ValueError("SEOUL_API_KEY not found in environment")
        return key
    
    def get_base_url(self) -> str:
        return os.getenv('SEOUL_API_URL', 'http://openapi.seoul.go.kr:8088/')
    
    def list_datasets(self) -> List[Dict]:
        """List available Seoul datasets"""
        datasets = []
        for name, service_name in self.DATASETS.items():
            datasets.append({
                'id': service_name,
                'name': name.replace('_', ' ').title(),
                'description': f'Seoul {name} data',
                'source': 'Seoul Metropolitan Government'
            })
        return datasets
    
    def fetch_data(self, dataset_id: str,
                  start_index: int = 1,
                  end_index: int = 100,
                  **params) -> Dict:
        """
        Fetch data from Seoul Open Data API
        
        Args:
            dataset_id: Service name (e.g., 'tbLnOpendataRtmsV')
            start_index: Starting index for results
            end_index: Ending index for results
        """
        
        # Seoul API URL format:
        # /{API_KEY}/{TYPE}/{SERVICE}/{START_INDEX}/{END_INDEX}/
        
        data_type = params.get('data_type', 'json')
        url = f"{self.base_url}{self.api_key}/{data_type}/{dataset_id}/{start_index}/{end_index}/"
        
        # Add additional parameters to URL if provided
        if 'year' in params:
            url += f"{params['year']}/"
        if 'month' in params:
            url += f"{params['month']}/"
        if 'district' in params:
            url += f"{params['district']}/"
            
        result = self._make_request(url)
        
        # Parse Seoul API response
        if dataset_id in result:
            data = result[dataset_id]
            if 'row' in data:
                return {
                    'success': True,
                    'dataset_id': dataset_id,
                    'data': data['row'],
                    'count': len(data['row']),
                    'total_count': data.get('list_total_count', len(data['row']))
                }
        
        return {
            'success': False,
            'dataset_id': dataset_id,
            'message': 'No data found',
            'raw_response': result
        }
    
    def get_real_estate_prices(self, year: str = '2024', month: str = '01', 
                               district: str = '', start_index: int = 1, end_index: int = 100):
        """Get Seoul real estate transaction prices"""
        return self.fetch_data(
            self.DATASETS['real_estate_prices'],
            start_index=start_index,
            end_index=end_index,
            year=year,
            month=month,
            district=district
        )
    
    def get_apartment_rent(self, year: str = '2024', month: str = '01',
                           start_index: int = 1, end_index: int = 100):
        """Get Seoul apartment rent prices"""
        return self.fetch_data(
            self.DATASETS['apartment_rent'],
            start_index=start_index,
            end_index=end_index,
            year=year,
            month=month
        )
    
    def get_air_quality(self, start_index: int = 1, end_index: int = 25):
        """Get Seoul real-time air quality (for 25 districts)"""
        return self.fetch_data(
            self.DATASETS['air_quality'],
            start_index=start_index,
            end_index=end_index
        )