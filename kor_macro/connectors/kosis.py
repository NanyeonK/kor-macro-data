"""KOSIS (Korean Statistical Information Service) API Connector - Enhanced Version"""

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
    
    # Comprehensive KOSIS table IDs (expanded from 6 to 30+)
    TABLE_IDS = {
        # Population & Demographics
        'population': 'DT_1B040A3',  # Population by age and gender
        'population_projection': 'DT_1B35001',  # Population projections
        'births': 'DT_1B040B1',  # Birth statistics
        'deaths': 'DT_1B040B2',  # Death statistics
        'marriages': 'DT_1B040M1',  # Marriage and divorce statistics
        'migration': 'DT_1B26001',  # Internal migration
        'foreign_residents': 'DT_1B04005',  # Foreign residents
        'households': 'DT_1B35002',  # Household statistics
        
        # Employment & Labor
        'employment': 'DT_118N_LFA9',  # Employment by industry
        'employment_status': 'DT_118N_LFA17',  # Employment status
        'unemployment': 'DT_118N_LFA6',  # Unemployment statistics
        'wages': 'DT_118N_PAIE01',  # Average wages by industry
        'working_hours': 'DT_118N_MON033',  # Working hours
        'labor_productivity': 'DT_118N_PROD02',  # Labor productivity
        'youth_employment': 'DT_1DA7004S',  # Youth employment
        'elderly_employment': 'DT_1DA7005S',  # Elderly employment
        'part_time_employment': 'DT_118N_LFA18',  # Part-time employment
        
        # Regional Economics
        'gdp_regional': 'DT_1C86',  # Regional GDP (GRDP)
        'cpi_regional': 'DT_1YL20631',  # Regional CPI
        'regional_employment': 'DT_2KAA308',  # Regional employment
        'regional_income': 'DT_1C87',  # Regional income
        'regional_investment': 'DT_1C88',  # Regional investment
        
        # Industry & Business
        'manufacturing_production': 'DT_1K51001',  # Manufacturing production
        'service_production': 'DT_1K52001',  # Service sector production  
        'construction_orders': 'DT_1KA1001',  # Construction orders
        'business_cycle': 'DT_1KE1001',  # Business cycle indicators
        'retail_sales': 'DT_1KC1001',  # Retail sales
        
        # Social Indicators
        'education_statistics': 'DT_1YL20921',  # Education statistics
        'welfare_statistics': 'DT_1YL21101',  # Social welfare
        'crime_statistics': 'DT_1YL21201',  # Crime statistics
        'environment': 'DT_1YL20841',  # Environmental statistics
        'transportation': 'DT_1YL20851',  # Transportation statistics
        'housing_statistics': 'DT_1YL20611',  # Housing statistics
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
    
    def _parse_kosis_date(self, date_str):
        """Parse KOSIS date formats intelligently"""
        try:
            date_str = str(date_str).strip()
            
            if len(date_str) == 4:  # YYYY (annual)
                return pd.to_datetime(f"{date_str}-01-01")
            elif len(date_str) == 6:  # YYYYMM (monthly)
                return pd.to_datetime(date_str, format='%Y%m')
            elif len(date_str) == 8:  # YYYYMMDD (daily)
                return pd.to_datetime(date_str, format='%Y%m%d')
            elif 'Q' in date_str:  # Quarterly (2023Q1)
                year = date_str[:4]
                quarter = int(date_str[-1])
                month = quarter * 3
                return pd.to_datetime(f"{year}-{month:02d}-01")
            else:
                # Fallback to pandas default
                return pd.to_datetime(date_str)
                
        except Exception as e:
            print(f"Warning: Failed to parse KOSIS date '{date_str}': {e}")
            return pd.NaT
    
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
            pd.DataFrame: DataFrame with standardized columns
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Convert to KOSIS format (YYYY)
        start_year = start_date[:4]
        end_year = end_date[:4]
        
        url = f"{self.base_url}Param/statisticsParameterData.do"
        
        request_params = {
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
            result = self._make_request(url, params=request_params)
            
            # Parse KOSIS response
            if isinstance(result, list) and len(result) > 0:
                # Convert to DataFrame
                df = pd.DataFrame(result)
                
                # Standardize columns with FIXED date parsing
                if 'PRD_DE' in df.columns and 'DT' in df.columns:
                    # FIXED: Use smart date parser
                    df['date'] = df['PRD_DE'].apply(self._parse_kosis_date)
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
                    
                    # Remove rows with invalid dates
                    df = df.dropna(subset=['date'])
                    
                    df = df[columns_to_keep].copy()
                    df = df.sort_values('date').reset_index(drop=True)
                    
                    return df
            
            # Return empty DataFrame if no data
            return pd.DataFrame(columns=['date', 'value'])
            
        except Exception as e:
            print(f"Error fetching KOSIS data: {e}")
            return pd.DataFrame(columns=['date', 'value'])
    
    # Population & Demographics Methods
    def get_population_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get population statistics by age and gender"""
        return self.fetch_data(self.TABLE_IDS['population'], start_date, end_date)
    
    def get_population_projection(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get population projections"""
        return self.fetch_data(self.TABLE_IDS['population_projection'], start_date, end_date)
    
    def get_birth_statistics(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get birth statistics"""
        return self.fetch_data(self.TABLE_IDS['births'], start_date, end_date)
    
    def get_death_statistics(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get death statistics"""
        return self.fetch_data(self.TABLE_IDS['deaths'], start_date, end_date)
    
    def get_marriage_statistics(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get marriage and divorce statistics"""
        return self.fetch_data(self.TABLE_IDS['marriages'], start_date, end_date)
    
    def get_migration_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get internal migration data"""
        return self.fetch_data(self.TABLE_IDS['migration'], start_date, end_date)
    
    def get_foreign_residents(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get foreign residents statistics"""
        return self.fetch_data(self.TABLE_IDS['foreign_residents'], start_date, end_date)
    
    def get_household_statistics(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get household statistics"""
        return self.fetch_data(self.TABLE_IDS['households'], start_date, end_date)
    
    # Employment & Labor Methods
    def get_employment_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get employment statistics by industry"""
        return self.fetch_data(self.TABLE_IDS['employment'], start_date, end_date)
    
    def get_employment_status(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get detailed employment status statistics"""
        return self.fetch_data(self.TABLE_IDS['employment_status'], start_date, end_date)
    
    def get_unemployment_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get unemployment statistics"""
        return self.fetch_data(self.TABLE_IDS['unemployment'], start_date, end_date)
    
    def get_wage_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get wage statistics by industry"""
        return self.fetch_data(self.TABLE_IDS['wages'], start_date, end_date)
    
    def get_working_hours(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get working hours statistics"""
        return self.fetch_data(self.TABLE_IDS['working_hours'], start_date, end_date)
    
    def get_labor_productivity(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get labor productivity statistics"""
        return self.fetch_data(self.TABLE_IDS['labor_productivity'], start_date, end_date)
    
    def get_youth_employment(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get youth employment statistics"""
        return self.fetch_data(self.TABLE_IDS['youth_employment'], start_date, end_date)
    
    def get_elderly_employment(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get elderly employment statistics"""
        return self.fetch_data(self.TABLE_IDS['elderly_employment'], start_date, end_date)
    
    def get_part_time_employment(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get part-time employment statistics"""
        return self.fetch_data(self.TABLE_IDS['part_time_employment'], start_date, end_date)
    
    # Regional Economics Methods
    def get_regional_gdp(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get regional GDP (GRDP) data"""
        return self.fetch_data(self.TABLE_IDS['gdp_regional'], start_date, end_date)
    
    def get_regional_cpi(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get regional CPI data"""
        return self.fetch_data(self.TABLE_IDS['cpi_regional'], start_date, end_date)
    
    def get_regional_employment(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get regional employment statistics"""
        return self.fetch_data(self.TABLE_IDS['regional_employment'], start_date, end_date)
    
    def get_regional_income(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get regional income statistics"""
        return self.fetch_data(self.TABLE_IDS['regional_income'], start_date, end_date)
    
    def get_regional_investment(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get regional investment statistics"""
        return self.fetch_data(self.TABLE_IDS['regional_investment'], start_date, end_date)
    
    # Industry & Business Methods
    def get_manufacturing_production(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get manufacturing production statistics"""
        return self.fetch_data(self.TABLE_IDS['manufacturing_production'], start_date, end_date)
    
    def get_service_production(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get service sector production statistics"""
        return self.fetch_data(self.TABLE_IDS['service_production'], start_date, end_date)
    
    def get_construction_orders(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get construction orders statistics"""
        return self.fetch_data(self.TABLE_IDS['construction_orders'], start_date, end_date)
    
    def get_business_cycle(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get business cycle indicators"""
        return self.fetch_data(self.TABLE_IDS['business_cycle'], start_date, end_date)
    
    def get_retail_sales(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get retail sales statistics"""
        return self.fetch_data(self.TABLE_IDS['retail_sales'], start_date, end_date)
    
    # Social Indicators Methods  
    def get_education_statistics(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get education statistics"""
        return self.fetch_data(self.TABLE_IDS['education_statistics'], start_date, end_date)
    
    def get_welfare_statistics(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get social welfare statistics"""
        return self.fetch_data(self.TABLE_IDS['welfare_statistics'], start_date, end_date)
    
    def get_crime_statistics(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get crime statistics"""
        return self.fetch_data(self.TABLE_IDS['crime_statistics'], start_date, end_date)
    
    def get_environment_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get environmental statistics"""
        return self.fetch_data(self.TABLE_IDS['environment'], start_date, end_date)
    
    def get_transportation_data(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get transportation statistics"""
        return self.fetch_data(self.TABLE_IDS['transportation'], start_date, end_date)
    
    def get_housing_statistics(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get housing statistics"""
        return self.fetch_data(self.TABLE_IDS['housing_statistics'], start_date, end_date)
    
    # Utility Methods
    def get_multiple_indicators(self, indicators: List[str], start_date: str = '2020-01-01', end_date: str = None) -> Dict[str, pd.DataFrame]:
        """Get multiple KOSIS indicators at once"""
        results = {}
        
        for indicator in indicators:
            if indicator in self.TABLE_IDS:
                try:
                    results[indicator] = self.fetch_data(self.TABLE_IDS[indicator], start_date, end_date)
                except Exception as e:
                    print(f"Failed to fetch {indicator}: {e}")
                    results[indicator] = pd.DataFrame(columns=['date', 'value'])
        
        return results
    
    def search_tables(self, keyword: str) -> List[Dict]:
        """Search for tables containing keyword"""
        matching_tables = []
        keyword_lower = keyword.lower()
        
        for name, table_id in self.TABLE_IDS.items():
            if keyword_lower in name.lower():
                matching_tables.append({
                    'name': name,
                    'table_id': table_id,
                    'description': name.replace('_', ' ').title()
                })
        
        return matching_tables
