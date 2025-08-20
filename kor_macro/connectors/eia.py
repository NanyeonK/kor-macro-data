"""
EIA (U.S. Energy Information Administration) API Connector

Provides access to energy data including oil prices, production, consumption, and inventories.
"""

import os
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from .base import BaseConnector
import logging

logger = logging.getLogger(__name__)

class EIAConnector(BaseConnector):
    """
    U.S. Energy Information Administration API Connector
    
    Provides access to energy market data including:
    - Crude oil prices and production
    - Natural gas prices and storage
    - Electricity generation and consumption
    - Renewable energy statistics
    """
    
    # Popular EIA series for energy markets
    PETROLEUM_SERIES = {
        'wti_spot': 'PET.RWTC.D',                    # WTI Crude Oil Spot Price
        'brent_spot': 'PET.RBRTE.D',                 # Brent Crude Oil Spot Price
        'gasoline_price': 'PET.EMM_EPM0_PTE_NUS_DPG.W',  # US Gasoline Price
        'crude_production_us': 'PET.WCRFPUS2.W',     # US Crude Oil Production
        'crude_stocks': 'PET.WCESTUS1.W',            # US Crude Oil Stocks
        'opec_production': 'PET.STEO.COPR_OPEC.M',   # OPEC Production
    }
    
    NATURAL_GAS_SERIES = {
        'henry_hub_spot': 'NG.RNGWHHD.D',            # Henry Hub Natural Gas Spot Price
        'gas_production': 'NG.N9070US2.M',           # US Natural Gas Production
        'gas_consumption': 'NG.N3010US2.M',          # US Natural Gas Consumption
        'gas_storage': 'NG.N5010US1.W',              # US Natural Gas Storage
    }
    
    ELECTRICITY_SERIES = {
        'total_generation': 'ELEC.GEN.ALL-US-99.M',  # Total Electricity Generation
        'renewable_generation': 'ELEC.GEN.REN-US-99.M',  # Renewable Generation
        'nuclear_generation': 'ELEC.GEN.NUC-US-99.M',    # Nuclear Generation
        'coal_generation': 'ELEC.GEN.COW-US-99.M',       # Coal Generation
        'solar_generation': 'ELEC.GEN.SUN-US-99.M',      # Solar Generation
    }
    
    # Regional data for Asia/Korea
    ASIA_SERIES = {
        'korea_petroleum_consumption': 'INTL.5-2-KOR-TBPD.A',  # Korea Petroleum Consumption
        'korea_electricity_generation': 'INTL.2-12-KOR-BKWH.A', # Korea Electricity Generation
        'japan_petroleum_consumption': 'INTL.5-2-JPN-TBPD.A',   # Japan Petroleum Consumption
        'china_petroleum_consumption': 'INTL.5-2-CHN-TBPD.A',   # China Petroleum Consumption
    }
    
    def __init__(self):
        """Initialize EIA connector with API key from environment"""
        super().__init__('EIA')
        self.api_key = self.get_api_key()
        self.base_url = 'https://api.eia.gov/v2/'
        
    def get_api_key(self) -> str:
        """Get EIA API key from environment"""
        key = os.getenv('EIA_API_KEY')
        if not key:
            logger.warning("EIA_API_KEY not found in environment. Some features may be limited.")
            # EIA allows limited access without key
            return ''
        return key
    
    def get_base_url(self) -> str:
        """Get base URL for EIA API"""
        return self.base_url
    
    def list_datasets(self) -> List[Dict]:
        """List available EIA datasets"""
        datasets = []
        
        # Petroleum datasets
        for key, series_id in self.PETROLEUM_SERIES.items():
            datasets.append({
                'id': series_id,
                'name': key.replace('_', ' ').title(),
                'category': 'Petroleum',
                'source': 'EIA',
                'frequency': self._get_frequency(series_id)
            })
        
        # Natural gas datasets
        for key, series_id in self.NATURAL_GAS_SERIES.items():
            datasets.append({
                'id': series_id,
                'name': key.replace('_', ' ').title(),
                'category': 'Natural Gas',
                'source': 'EIA',
                'frequency': self._get_frequency(series_id)
            })
        
        # Electricity datasets
        for key, series_id in self.ELECTRICITY_SERIES.items():
            datasets.append({
                'id': series_id,
                'name': key.replace('_', ' ').title(),
                'category': 'Electricity',
                'source': 'EIA',
                'frequency': self._get_frequency(series_id)
            })
        
        # Asia/Korea datasets
        for key, series_id in self.ASIA_SERIES.items():
            datasets.append({
                'id': series_id,
                'name': key.replace('_', ' ').title(),
                'category': 'International/Asia',
                'source': 'EIA',
                'frequency': self._get_frequency(series_id)
            })
        
        return datasets
    
    def _get_frequency(self, series_id: str) -> str:
        """Determine frequency from series ID"""
        if series_id.endswith('.D'):
            return 'Daily'
        elif series_id.endswith('.W'):
            return 'Weekly'
        elif series_id.endswith('.M'):
            return 'Monthly'
        elif series_id.endswith('.A'):
            return 'Annual'
        else:
            return 'Unknown'
    
    def fetch_data(self, series_id: str, 
                  start_date: str = '2010-01-01',
                  end_date: str = None,
                  **params) -> pd.DataFrame:
        """
        Fetch data from EIA API
        
        Args:
            series_id: EIA series ID (e.g., 'PET.RWTC.D' for WTI crude)
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            
        Returns:
            DataFrame with date and value columns
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Build API URL
        url = f"{self.base_url}seriesid/{series_id}"
        
        params = {
            'api_key': self.api_key,
            'start': start_date.replace('-', ''),
            'end': end_date.replace('-', ''),
            'out': 'json'
        }
        
        try:
            response = self._make_request(url, params)
            
            if response and 'series' in response and len(response['series']) > 0:
                series_data = response['series'][0]
                
                # Convert to DataFrame
                df = pd.DataFrame(series_data['data'])
                
                # Parse dates based on frequency
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                elif 'period' in df.columns:
                    df['date'] = pd.to_datetime(df['period'])
                
                # Rename value column
                df = df.rename(columns={'value': 'value', 'v': 'value'})
                
                # Convert value to numeric
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                
                # Sort by date
                df = df.sort_values('date')
                
                # Keep only date and value
                df = df[['date', 'value']]
                
                logger.info(f"Successfully fetched {len(df)} records for {series_id}")
                return df
            else:
                logger.warning(f"No data found for series {series_id}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error fetching EIA data: {e}")
            return pd.DataFrame()
    
    def get_wti_crude_price(self, start_date: str = '2010-01-01', 
                           end_date: str = None) -> pd.DataFrame:
        """Get WTI crude oil spot price"""
        return self.fetch_data('PET.RWTC.D', start_date, end_date)
    
    def get_brent_crude_price(self, start_date: str = '2010-01-01',
                             end_date: str = None) -> pd.DataFrame:
        """Get Brent crude oil spot price"""
        return self.fetch_data('PET.RBRTE.D', start_date, end_date)
    
    def get_henry_hub_gas_price(self, start_date: str = '2010-01-01',
                                end_date: str = None) -> pd.DataFrame:
        """Get Henry Hub natural gas spot price"""
        return self.fetch_data('NG.RNGWHHD.D', start_date, end_date)
    
    def get_us_gasoline_price(self, start_date: str = '2010-01-01',
                              end_date: str = None) -> pd.DataFrame:
        """Get US regular gasoline retail price"""
        return self.fetch_data('PET.EMM_EPM0_PTE_NUS_DPG.W', start_date, end_date)
    
    def get_korea_energy_data(self, data_type: str = 'petroleum_consumption',
                              start_date: str = '2010-01-01',
                              end_date: str = None) -> pd.DataFrame:
        """
        Get Korea energy data
        
        Args:
            data_type: Type of data ('petroleum_consumption' or 'electricity_generation')
            start_date: Start date
            end_date: End date
            
        Returns:
            DataFrame with Korea energy data
        """
        if data_type == 'petroleum_consumption':
            series_id = 'INTL.5-2-KOR-TBPD.A'
        elif data_type == 'electricity_generation':
            series_id = 'INTL.2-12-KOR-BKWH.A'
        else:
            raise ValueError(f"Unknown data type: {data_type}")
        
        return self.fetch_data(series_id, start_date, end_date)
    
    def get_crude_oil_inventories(self, start_date: str = '2010-01-01',
                                  end_date: str = None) -> pd.DataFrame:
        """Get US crude oil inventories (weekly)"""
        return self.fetch_data('PET.WCESTUS1.W', start_date, end_date)
    
    def get_renewable_generation(self, start_date: str = '2010-01-01',
                                 end_date: str = None) -> pd.DataFrame:
        """Get US renewable electricity generation"""
        return self.fetch_data('ELEC.GEN.REN-US-99.M', start_date, end_date)