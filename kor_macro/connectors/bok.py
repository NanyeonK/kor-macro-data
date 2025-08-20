"""Bank of Korea ECOS API Connector - Fixed Version"""

import os
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
try:
    from .base import BaseConnector
except ImportError:
    from connectors.base import BaseConnector

class BOKConnector(BaseConnector):
    """Connector for Bank of Korea Economic Statistics System (ECOS)"""
    
    # Popular BOK statistics codes
    STAT_CODES = {
        'base_rate': '722Y001',  # Base rate
        'call_rate': '721Y001',  # Call rate (overnight)
        'exchange_rate_usd': '731Y003/1070000',  # USD/KRW
        'exchange_rate_eur': '731Y003/1070001',  # EUR/KRW
        'exchange_rate_jpy': '731Y003/1070002',  # JPY/KRW (100 yen)
        'money_supply_m1': '901Y014/AI1AA',  # M1 Money Supply
        'money_supply_m2': '901Y014/AI2AA',  # M2 Money Supply
        'gdp_nominal': '200Y001/I16A',  # GDP (Nominal)
        'gdp_real': '200Y001/I16B',  # GDP (Real)
        'cpi': '901Y009/0',  # Consumer Price Index
        'housing_price': '901Y066/KB01',  # KB Housing Price Index
        'unemployment': '901Y016/1',  # Unemployment rate
        'exports': '301Y013/1',  # Exports
        'imports': '301Y013/2',  # Imports
        'kospi': '817Y002/KOSPI',  # KOSPI Index
    }
    
    def __init__(self):
        super().__init__('BOK_ECOS')
        self.api_key = self.get_api_key()
        self.base_url = self.get_base_url()
        self.lang = os.getenv('BOK_LANG', 'kr')
        
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
                  start_date: str = '2020-01-01',
                  end_date: str = None,
                  period: str = 'M',  # D: Daily, M: Monthly, Q: Quarterly, Y: Yearly
                  **params) -> pd.DataFrame:
        """
        Fetch data from BOK ECOS API
        
        Args:
            dataset_id: Statistics code (e.g., '722Y001' for base rate)
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format) 
            period: Period type (D/M/Q/Y)
            
        Returns:
            pd.DataFrame: DataFrame with date and value columns
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Convert dates to BOK format (YYYYMMDD)
        bok_start = start_date.replace('-', '')
        bok_end = end_date.replace('-', '')
        
        # BOK ECOS API endpoint format
        url = f"{self.base_url}StatisticSearch/{self.api_key}/json/{self.lang}/1/10000/{dataset_id}/{period}/{bok_start}/{bok_end}"
        
        try:
            result = self._make_request(url)
            
            # Parse BOK response
            if 'StatisticSearch' in result and 'row' in result['StatisticSearch']:
                rows = result['StatisticSearch']['row']
                
                # Convert to DataFrame
                df = pd.DataFrame(rows)
                
                # Standardize column names
                if 'TIME' in df.columns and 'DATA_VALUE' in df.columns:
                    df['date'] = pd.to_datetime(df['TIME'])
                    df['value'] = pd.to_numeric(df['DATA_VALUE'], errors='coerce')
                    
                    # Keep relevant columns
                    columns_to_keep = ['date', 'value']
                    if 'UNIT_NAME' in df.columns:
                        df['unit'] = df['UNIT_NAME']
                        columns_to_keep.append('unit')
                    if 'ITEM_NAME1' in df.columns:
                        df['item'] = df['ITEM_NAME1']
                        columns_to_keep.append('item')
                    
                    df = df[columns_to_keep].copy()
                    df = df.sort_values('date').reset_index(drop=True)
                    
                    return df
            
            # Return empty DataFrame if no data
            return pd.DataFrame(columns=['date', 'value'])
            
        except Exception as e:
            print(f"Error fetching BOK data: {e}")
            return pd.DataFrame(columns=['date', 'value'])
    
    def get_base_rate(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get Bank of Korea base rate"""
        return self.fetch_data(self.STAT_CODES['base_rate'], start_date, end_date, 'M')
    
    def get_call_rate(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get call rate (overnight)"""
        return self.fetch_data(self.STAT_CODES['call_rate'], start_date, end_date, 'D')
    
    def get_exchange_rate(self, currency: str = 'USD', start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get exchange rate for specified currency"""
        currency_map = {
            'USD': 'exchange_rate_usd',
            'EUR': 'exchange_rate_eur', 
            'JPY': 'exchange_rate_jpy'
        }
        
        if currency not in currency_map:
            raise ValueError(f"Currency {currency} not supported. Use: {list(currency_map.keys())}")
        
        return self.fetch_data(self.STAT_CODES[currency_map[currency]], start_date, end_date, 'D')
    
    def get_money_supply(self, supply_type: str = 'M2', start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get money supply (M1 or M2)"""
        if supply_type == 'M1':
            return self.fetch_data(self.STAT_CODES['money_supply_m1'], start_date, end_date, 'M')
        elif supply_type == 'M2':
            return self.fetch_data(self.STAT_CODES['money_supply_m2'], start_date, end_date, 'M')
        else:
            raise ValueError("supply_type must be 'M1' or 'M2'")
    
    def get_gdp(self, gdp_type: str = 'nominal', start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get GDP data (nominal or real)"""
        if gdp_type == 'nominal':
            return self.fetch_data(self.STAT_CODES['gdp_nominal'], start_date, end_date, 'Q')
        elif gdp_type == 'real':
            return self.fetch_data(self.STAT_CODES['gdp_real'], start_date, end_date, 'Q')
        else:
            raise ValueError("gdp_type must be 'nominal' or 'real'")
    
    def get_cpi(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get Consumer Price Index"""
        return self.fetch_data(self.STAT_CODES['cpi'], start_date, end_date, 'M')
    
    def get_housing_price_index(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get housing price index"""
        return self.fetch_data(self.STAT_CODES['housing_price'], start_date, end_date, 'M')
    
    def get_unemployment_rate(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get unemployment rate"""
        return self.fetch_data(self.STAT_CODES['unemployment'], start_date, end_date, 'M')
    
    def get_trade_data(self, trade_type: str = 'exports', start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get trade data (exports or imports)"""
        if trade_type == 'exports':
            return self.fetch_data(self.STAT_CODES['exports'], start_date, end_date, 'M')
        elif trade_type == 'imports':
            return self.fetch_data(self.STAT_CODES['imports'], start_date, end_date, 'M')
        else:
            raise ValueError("trade_type must be 'exports' or 'imports'")
    
    def get_kospi(self, start_date: str = '2020-01-01', end_date: str = None) -> pd.DataFrame:
        """Get KOSPI index"""
        return self.fetch_data(self.STAT_CODES['kospi'], start_date, end_date, 'D')
    
    def get_economic_indicators(self, indicators: List[str] = None, start_date: str = '2020-01-01', end_date: str = None) -> Dict[str, pd.DataFrame]:
        """Get multiple economic indicators"""
        if indicators is None:
            indicators = ['base_rate', 'exchange_rate_usd', 'cpi', 'unemployment']
        
        results = {}
        for indicator in indicators:
            if indicator in self.STAT_CODES:
                try:
                    if indicator == 'base_rate':
                        results[indicator] = self.get_base_rate(start_date, end_date)
                    elif indicator == 'exchange_rate_usd':
                        results[indicator] = self.get_exchange_rate('USD', start_date, end_date)
                    elif indicator == 'cpi':
                        results[indicator] = self.get_cpi(start_date, end_date)
                    elif indicator == 'unemployment':
                        results[indicator] = self.get_unemployment_rate(start_date, end_date)
                    else:
                        results[indicator] = self.fetch_data(self.STAT_CODES[indicator], start_date, end_date)
                except Exception as e:
                    print(f"Failed to fetch {indicator}: {e}")
                    results[indicator] = pd.DataFrame(columns=['date', 'value'])
        
        return results
