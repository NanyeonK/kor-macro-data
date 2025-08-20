"""Base connector class for Korean data APIs"""

import os
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import requests
# from tenacity import retry, stop_after_attempt, wait_exponential  # Optional dependency
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is optional, environment variables can be set directly
    pass

class BaseConnector(ABC):
    """Abstract base class for API connectors"""
    
    def __init__(self, api_name: str):
        self.api_name = api_name
        self.logger = logging.getLogger(api_name)
        self.session = requests.Session()
        self.last_request_time = 0
        self.rate_limit_delay = 1.0  # seconds between requests
        
    @abstractmethod
    def get_api_key(self) -> str:
        """Get API key from environment"""
        pass
    
    @abstractmethod
    def get_base_url(self) -> str:
        """Get base URL for API"""
        pass
    
    @abstractmethod
    def list_datasets(self) -> List[Dict]:
        """List available datasets"""
        pass
    
    @abstractmethod
    def fetch_data(self, dataset_id: str, **params) -> Dict:
        """Fetch data from specific dataset"""
        pass
    
    def _rate_limit(self):
        """Simple rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: Optional[Dict] = None, 
                     method: str = 'GET', data: Optional[Dict] = None) -> Dict:
        """Make HTTP request with retry logic"""
        self._rate_limit()
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=30)
            elif method == 'POST':
                response = self.session.post(url, data=data, params=params, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            
            # Try to parse JSON, fallback to text
            try:
                return response.json()
            except:
                return {'raw_data': response.text}
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test if API connection works"""
        try:
            datasets = self.list_datasets()
            return len(datasets) > 0 if datasets else False
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False