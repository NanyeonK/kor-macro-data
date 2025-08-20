"""KOSIS (Korean Statistical Information Service) API Connector - Fixed Version"""

import os
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
try:
    from .base import BaseConnector
except ImportError:
    from connectors.base import BaseConnector

class KOSISConnector(BaseConnector):
    """Connector for Korean Statistical Information Service (KOSIS)"""
    
    # Popular KOSIS table IDs
    TABLE_IDS = {
        'population': 'DT_1B040A3',  # Population by age and gender
        'employment': 'DT_118N_LFA9',  # Employment by industry
        'wages': 'DT_118N_PAIE01',  # Average wages by industry
        'gdp_regional': 'DT_1C86',  # Regional GDP (GRDP)
        'cpi_regional': 'DT_1YL20631',  # Regional CPI
        'births': 'DT_1B040B1',  # Birth statistics
        'deaths': 'DT_1B040B2',  # Death statistics
        'marriages': 'DT_1B040M1',  # Marriage and divorce
        'households': 'DT_1B35001',  # Household projections
        'working_hours': 'DT_118N_MON033',  # Working hours
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
        for name, table_id in self.TABLE_IDS.items():
            datasets.append({
                'id': table_id,
                'name': name.replace('_', ' ').title(),
                'description': f'KOSIS {name} statistics',
                'source': 'KOSIS'
            })
        return datasets
    
    def fetch_data(self, table_id: str, 
                  start_date: str = '2020-01-01',
                  end_date: str = None,
                  **params) -> pd.DataFrame:
        """
        Fetch data from KOSIS API
        
        Args:
            table_id: KOSIS table ID (e.g., 'DT_1B040A3')
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            
        Returns:
            pd.DataFrame: DataFrame with data
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Convert to KOSIS format (YYYY)
        start_year = start_date[:4]
        end_year = end_date[:4]
        
        url = f"{self.base_url}Param/statisticsParameterData.do"
        
        params = {
            'method': 'getList',
            'apiKey': self.api_key,
            'itmId': 'ALL',  # All items
            'objL1': 'ALL',  # All level 1 objects
            'objL2': '',     # Level 2 objects
            'objL3': '',     # Level 3 objects
            'objL4': '',     # Level 4 objects
            'objL5': '',     # Level 5 objects
            'objL6': '',     # Level 6 objects
            'objL7': '',     # Level 7 objects
            'objL8': '',     # Level 8 objects
            'format': 'json',
            'jsonVD': 'Y',
            'prdSe': 'Y',    # Year period
            'startPrdDe': start_year,
            'endPrdDe': end_year,
            'tblId': table_id
        }
        
        try:
            result = self._make_request(url, params=params)
            
            # Parse KOSIS response
            if isinstance(result, list) and len(result) > 0:
                # Convert to DataFrame
                df = pd.DataFrame(result)
                
                # Standardize columns
                if 'PRD_DE' in df.columns and 'DT' in df.columns:
                    df['date'] = pd.to_datetime(df['PRD_DE'], format='%Y')
                    df['value'] = pd.to_numeric(df['DT'], errors='coerce')
                    
                    # Keep relevant columns
                    columns_to_keep = ['date', 'value']
                    if 'ITM_NM' in df.columns:
                        df['item'] = df['ITM_NM']
                        columns_to_keep.append('item')
                    if 'C1_NM' in df.columns:
                        df['category'] = df['C1_NM']
                        columns_to_keep.append('category')
                    if 'UNIT_NM' in df.columns:
                        df['unit'] = df['UNIT_NM']
                        columns_to_keep.append('unit')
                    
                    df = df[columns_to_keep].copy()
                    df = df.sort_values('date').reset_index(drop=True)
                    
                    return df
            
            # Return empty DataFrame if no data
            return pd.DataFrame(columns=['date', 'value'])
            
        except Exception as e:
            print(f"Error fetching KOSIS data: {e}")
            return pd.DataFrame(columns=['date', 'value'])
    
    def get_population_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get population statistics"""
        return self.fetch_data(self.TABLE_IDS['population'], start_date, end_date)
    
    def get_employment_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get employment statistics"""
        return self.fetch_data(self.TABLE_IDS['employment'], start_date, end_date)
    
    def get_wage_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get wage statistics"""
        return self.fetch_data(self.TABLE_IDS['wages'], start_date, end_date)
    
    def get_regional_gdp(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get regional GDP data"""
        return self.fetch_data(self.TABLE_IDS['gdp_regional'], start_date, end_date)
