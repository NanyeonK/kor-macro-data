"""Global Economic Data Connectors - Fed, World Bank, IMF, OECD, ECB"""

import os
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from .base import BaseConnector
import logging

logger = logging.getLogger(__name__)

class FREDConnector(BaseConnector):
    """Federal Reserve Economic Data (FRED) API Connector"""
    
    # Popular FRED series for major economies
    GDP_SERIES = {
        'us_gdp': 'GDP',                    # US GDP
        'us_real_gdp': 'GDPC1',            # US Real GDP
        'us_gdp_growth': 'A191RL1Q225SBEA', # US GDP Growth Rate
        'china_gdp': 'NYGDPMKTPCDWLD',     # China GDP (World Bank via FRED)
        'japan_gdp': 'JPNNGDP',            # Japan GDP
        'eurozone_gdp': 'EUNGDP',          # Eurozone GDP
        'uk_gdp': 'UKNGDP',                # UK GDP
        'germany_gdp': 'CLVMNACSCAB1GQDE',  # Germany GDP (Real)
        'france_gdp': 'CPMNACSCAB1GQFR',   # France GDP
        'korea_gdp': 'KORNGDP',            # South Korea GDP
    }
    
    INTEREST_RATES = {
        'fed_funds': 'DFF',                # Federal Funds Rate
        'us_10y': 'DGS10',                 # US 10-Year Treasury
        'ecb_rate': 'ECBDFR',              # ECB Deposit Rate
        'boj_rate': 'IRSTCB01JPM156N',     # Bank of Japan Rate
    }
    
    INFLATION = {
        'us_cpi': 'CPIAUCSL',              # US CPI
        'us_pce': 'PCEPI',                 # US PCE
        'eurozone_cpi': 'CP0000EZ19M086NEST', # Eurozone CPI
    }
    
    def __init__(self):
        super().__init__('FRED')
        self.api_key = self.get_api_key()
        self.base_url = os.getenv('FRED_API_URL', 'https://api.stlouisfed.org/fred/')
        
    def get_api_key(self) -> str:
        key = os.getenv('FRED_API_KEY')
        if not key:
            raise ValueError("FRED_API_KEY not found in environment")
        return key
    
    def get_base_url(self) -> str:
        return self.base_url
    
    def list_datasets(self) -> List[Dict]:
        """List available FRED datasets"""
        datasets = []
        
        # GDP datasets
        for key, series_id in self.GDP_SERIES.items():
            datasets.append({
                'id': series_id,
                'name': key.replace('_', ' ').upper(),
                'category': 'GDP',
                'source': 'FRED'
            })
        
        # Interest rates
        for key, series_id in self.INTEREST_RATES.items():
            datasets.append({
                'id': series_id,
                'name': key.replace('_', ' ').title(),
                'category': 'Interest Rates',
                'source': 'FRED'
            })
        
        # Inflation
        for key, series_id in self.INFLATION.items():
            datasets.append({
                'id': series_id,
                'name': key.replace('_', ' ').upper(),
                'category': 'Inflation',
                'source': 'FRED'
            })
        
        return datasets
    
    def fetch_data(self, series_id: str, 
                  start_date: str = '2010-01-01',
                  end_date: str = None,
                  **params) -> Dict:
        """
        Fetch data from FRED API
        
        Args:
            series_id: FRED series ID (e.g., 'GDP' for US GDP)
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
        """
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        url = f"{self.base_url}series/observations"
        
        api_params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json',
            'observation_start': start_date,
            'observation_end': end_date,
        }
        
        result = self._make_request(url, params=api_params)
        
        if 'observations' in result:
            return {
                'success': True,
                'series_id': series_id,
                'data': result['observations'],
                'count': len(result['observations']),
                'units': result.get('units', ''),
                'title': result.get('title', series_id)
            }
        
        return {
            'success': False,
            'series_id': series_id,
            'message': 'No data found'
        }
    
    def get_gdp_data(self, countries: List[str] = ['us', 'china', 'japan', 'eurozone'],
                     start_date: str = '2010-01-01') -> pd.DataFrame:
        """Get GDP data for multiple countries"""
        all_data = []
        
        for country in countries:
            series_key = f"{country}_gdp"
            if series_key in self.GDP_SERIES:
                series_id = self.GDP_SERIES[series_key]
                data = self.fetch_data(series_id, start_date)
                
                if data['success']:
                    df = pd.DataFrame(data['data'])
                    df['country'] = country.upper()
                    df['series'] = 'GDP'
                    all_data.append(df)
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()


class WorldBankConnector(BaseConnector):
    """World Bank API Connector"""
    
    # Common indicators
    INDICATORS = {
        'gdp': 'NY.GDP.MKTP.CD',           # GDP (current US$)
        'gdp_growth': 'NY.GDP.MKTP.KD.ZG',  # GDP growth (annual %)
        'gdp_per_capita': 'NY.GDP.PCAP.CD', # GDP per capita
        'inflation': 'FP.CPI.TOTL.ZG',      # Inflation (CPI)
        'unemployment': 'SL.UEM.TOTL.ZS',   # Unemployment rate
        'population': 'SP.POP.TOTL',        # Total population
        'exports': 'NE.EXP.GNFS.CD',        # Exports of goods and services
        'imports': 'NE.IMP.GNFS.CD',        # Imports of goods and services
    }
    
    # Country codes
    COUNTRIES = {
        'us': 'USA',
        'china': 'CHN',
        'japan': 'JPN',
        'germany': 'DEU',
        'uk': 'GBR',
        'france': 'FRA',
        'india': 'IND',
        'korea': 'KOR',
        'eurozone': 'EMU',
    }
    
    def __init__(self):
        super().__init__('WorldBank')
        self.base_url = os.getenv('WORLD_BANK_API_URL', 'https://api.worldbank.org/v2/')
    
    def get_api_key(self) -> str:
        return ""  # World Bank API doesn't require a key
    
    def get_base_url(self) -> str:
        return self.base_url
    
    def list_datasets(self) -> List[Dict]:
        """List available World Bank indicators"""
        datasets = []
        for key, indicator_id in self.INDICATORS.items():
            datasets.append({
                'id': indicator_id,
                'name': key.replace('_', ' ').title(),
                'description': f'World Bank {key} indicator',
                'source': 'World Bank'
            })
        return datasets
    
    def fetch_data(self, indicator: str, 
                  countries: List[str] = ['USA', 'CHN', 'JPN', 'EMU'],
                  start_year: int = 2010,
                  end_year: int = None,
                  **params) -> Dict:
        """
        Fetch data from World Bank API
        
        Args:
            indicator: Indicator ID (e.g., 'NY.GDP.MKTP.CD' for GDP)
            countries: List of country codes
            start_year: Start year
            end_year: End year
        """
        if not end_year:
            end_year = datetime.now().year
        
        # Convert country list to semicolon-separated string
        country_str = ';'.join(countries)
        
        url = f"{self.base_url}country/{country_str}/indicator/{indicator}"
        
        api_params = {
            'format': 'json',
            'date': f"{start_year}:{end_year}",
            'per_page': 1000
        }
        
        result = self._make_request(url, params=api_params)
        
        # World Bank returns array with metadata and data
        if isinstance(result, list) and len(result) > 1:
            data = result[1] if result[1] else []
            return {
                'success': True,
                'indicator': indicator,
                'data': data,
                'count': len(data),
                'metadata': result[0] if result[0] else {}
            }
        
        return {
            'success': False,
            'indicator': indicator,
            'message': 'No data found'
        }


class IMFConnector(BaseConnector):
    """International Monetary Fund (IMF) Data Connector"""
    
    # IMF datasets
    DATASETS = {
        'weo': 'WEO',  # World Economic Outlook
        'ifs': 'IFS',  # International Financial Statistics
        'bop': 'BOP',  # Balance of Payments
        'gfs': 'GFS',  # Government Finance Statistics
    }
    
    def __init__(self):
        super().__init__('IMF')
        self.base_url = 'https://www.imf.org/external/datamapper/api/v1/'
    
    def get_api_key(self) -> str:
        return ""  # IMF API doesn't require a key
    
    def get_base_url(self) -> str:
        return self.base_url
    
    def list_datasets(self) -> List[Dict]:
        """List available IMF datasets"""
        datasets = []
        for key, dataset_id in self.DATASETS.items():
            datasets.append({
                'id': dataset_id,
                'name': key.upper(),
                'description': f'IMF {dataset_id} dataset',
                'source': 'IMF'
            })
        return datasets
    
    def fetch_data(self, indicator: str, countries: List[str] = None, **params) -> Dict:
        """Fetch data from IMF API"""
        url = f"{self.base_url}{indicator}"
        
        result = self._make_request(url)
        
        if result:
            # Filter by countries if specified
            if countries and 'values' in result:
                filtered_data = {
                    country: result['values'].get(country, {})
                    for country in countries
                    if country in result['values']
                }
                result['values'] = filtered_data
            
            return {
                'success': True,
                'indicator': indicator,
                'data': result,
                'count': len(result.get('values', {}))
            }
        
        return {
            'success': False,
            'indicator': indicator,
            'message': 'No data found'
        }


class OECDConnector(BaseConnector):
    """OECD Statistics Connector"""
    
    # OECD datasets
    DATASETS = {
        'gdp': 'SNA_TABLE1',
        'prices': 'PRICES_CPI',
        'unemployment': 'STLABOUR',
        'trade': 'IMTS',
    }
    
    def __init__(self):
        super().__init__('OECD')
        self.base_url = 'https://stats.oecd.org/SDMX-JSON/data/'
    
    def get_api_key(self) -> str:
        return ""  # Basic OECD access doesn't require a key
    
    def get_base_url(self) -> str:
        return self.base_url
    
    def list_datasets(self) -> List[Dict]:
        """List available OECD datasets"""
        return [
            {'id': 'gdp', 'name': 'GDP Statistics', 'source': 'OECD'},
            {'id': 'prices', 'name': 'Consumer Prices', 'source': 'OECD'},
            {'id': 'unemployment', 'name': 'Labour Statistics', 'source': 'OECD'},
            {'id': 'trade', 'name': 'International Trade', 'source': 'OECD'},
        ]
    
    def fetch_data(self, dataset_id: str, **params) -> Dict:
        """Fetch data from OECD"""
        if dataset_id in self.DATASETS:
            dataset_code = self.DATASETS[dataset_id]
        else:
            dataset_code = dataset_id
        
        url = f"{self.base_url}{dataset_code}/all/all"
        
        try:
            result = self._make_request(url)
            return {
                'success': True,
                'dataset': dataset_id,
                'data': result
            }
        except:
            return {
                'success': False,
                'dataset': dataset_id,
                'message': 'Failed to fetch data'
            }


class ECBConnector(BaseConnector):
    """European Central Bank Data Connector"""
    
    def __init__(self):
        super().__init__('ECB')
        self.base_url = 'https://data-api.ecb.europa.eu/service/data/'
    
    def get_api_key(self) -> str:
        return ""  # ECB API doesn't require a key
    
    def get_base_url(self) -> str:
        return self.base_url
    
    def list_datasets(self) -> List[Dict]:
        """List available ECB datasets"""
        return [
            {'id': 'ICP', 'name': 'Inflation and Consumer Prices', 'source': 'ECB'},
            {'id': 'MIR', 'name': 'Interest Rates', 'source': 'ECB'},
            {'id': 'EXR', 'name': 'Exchange Rates', 'source': 'ECB'},
            {'id': 'GDP', 'name': 'GDP and Economic Activity', 'source': 'ECB'},
        ]
    
    def fetch_data(self, dataset_id: str, **params) -> Dict:
        """Fetch data from ECB"""
        url = f"{self.base_url}{dataset_id}"
        
        headers = {'Accept': 'application/json'}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return {
                    'success': True,
                    'dataset': dataset_id,
                    'data': response.json()
                }
        except Exception as e:
            logger.error(f"ECB fetch failed: {e}")
        
        return {
            'success': False,
            'dataset': dataset_id,
            'message': 'Failed to fetch data'
        }