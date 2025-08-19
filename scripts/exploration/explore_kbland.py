"""Explore KB Land website to understand available data"""

import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

def explore_kb_land():
    """Explore KB Land website structure and available data"""
    
    print("="*60)
    print("Exploring KB Land Data Portal")
    print("="*60)
    
    # Main URLs to explore
    urls_to_check = [
        ('Main Page', 'https://data.kbland.kr'),
        ('Statistics', 'https://data.kbland.kr/kbstats'),
        ('Market Trends', 'https://data.kbland.kr/kbstats/wmh'),
        ('API Info', 'https://data.kbland.kr/api-info'),
        ('Data Download', 'https://data.kbland.kr/data-download'),
    ]
    
    findings = {}
    
    for name, url in urls_to_check:
        print(f"\nChecking: {name}")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, 
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for data categories
                print("  Status: ✓ Accessible")
                
                # Find menu items or navigation
                nav_items = soup.find_all(['nav', 'ul', 'div'], class_=['menu', 'nav', 'gnb', 'lnb'])
                if nav_items:
                    print("  Navigation found:")
                    for nav in nav_items[:2]:  # First 2 navigation elements
                        links = nav.find_all('a')
                        for link in links[:10]:  # First 10 links
                            href = link.get('href', '')
                            text = link.get_text(strip=True)
                            if text and len(text) < 50:
                                print(f"    - {text}: {href}")
                
                # Look for data tables
                tables = soup.find_all('table')
                if tables:
                    print(f"  Found {len(tables)} data tables")
                
                # Look for API endpoints in scripts
                scripts = soup.find_all('script')
                api_endpoints = []
                for script in scripts:
                    if script.string:
                        # Look for API URLs
                        if 'api' in script.string.lower() or 'data' in script.string.lower():
                            lines = script.string.split('\n')
                            for line in lines:
                                if 'url' in line.lower() or 'endpoint' in line.lower():
                                    api_endpoints.append(line.strip()[:100])
                
                if api_endpoints:
                    print("  Potential API endpoints found:")
                    for endpoint in api_endpoints[:5]:
                        print(f"    {endpoint}")
                
                # Look for data download links
                download_links = soup.find_all('a', href=lambda x: x and ('.csv' in x or '.xlsx' in x or 'download' in x.lower()))
                if download_links:
                    print(f"  Found {len(download_links)} download links")
                    for link in download_links[:5]:
                        print(f"    - {link.get_text(strip=True)}: {link.get('href')}")
                
                findings[name] = {
                    'status': 'accessible',
                    'tables': len(tables),
                    'downloads': len(download_links),
                    'has_navigation': bool(nav_items)
                }
                
            else:
                print(f"  Status: ✗ HTTP {response.status_code}")
                findings[name] = {'status': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"  Status: ✗ Error - {str(e)[:50]}")
            findings[name] = {'status': 'error', 'message': str(e)[:100]}
    
    # Check for REST API
    print("\n" + "="*60)
    print("Checking for REST API endpoints")
    print("="*60)
    
    api_endpoints_to_test = [
        'https://data.kbland.kr/api/v1/stats',
        'https://data.kbland.kr/api/data',
        'https://api.kbland.kr/v1/stats',
        'https://api.kbland.kr/data',
    ]
    
    for endpoint in api_endpoints_to_test:
        print(f"\nTesting: {endpoint}")
        try:
            response = requests.get(endpoint, 
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=5)
            print(f"  Response: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  JSON Response: {json.dumps(data, ensure_ascii=False)[:200]}")
                except:
                    print(f"  HTML Response: {response.text[:200]}")
        except Exception as e:
            print(f"  Failed: {str(e)[:50]}")
    
    # Save findings
    output_path = Path('dataset_lists/kb_land_exploration.json')
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)
    
    print(f"\nFindings saved to: {output_path}")
    
    return findings

def check_kb_actual_data():
    """Try to get actual data from KB Land"""
    
    print("\n" + "="*60)
    print("Attempting to fetch actual KB Land data")
    print("="*60)
    
    # These are common KB Land data endpoints based on their service
    test_urls = [
        {
            'name': 'KB 주택가격동향 (House Price Trends)',
            'url': 'https://data.kbland.kr/kbstats/wmh/main',
            'description': 'Monthly house price index'
        },
        {
            'name': 'KB 월간 주택가격동향',
            'url': 'https://kbland.kr/webview/stats/priceTrend',
            'description': 'Monthly price trends'
        },
        {
            'name': 'KB 시세조회',
            'url': 'https://kbland.kr/map',
            'description': 'Price inquiry by region'
        }
    ]
    
    for item in test_urls:
        print(f"\n{item['name']}")
        print(f"URL: {item['url']}")
        print(f"Description: {item['description']}")
        
        try:
            response = requests.get(item['url'], 
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10)
            
            if response.status_code == 200:
                print(f"✓ Accessible")
                
                # Check content type
                content_type = response.headers.get('content-type', '')
                print(f"  Content-Type: {content_type}")
                
                # If JSON response
                if 'json' in content_type:
                    data = response.json()
                    print(f"  JSON Data: {json.dumps(data, ensure_ascii=False)[:300]}")
                else:
                    # Parse HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for data elements
                    data_elements = soup.find_all(['div', 'span', 'p'], 
                        class_=lambda x: x and any(keyword in str(x).lower() 
                        for keyword in ['price', 'index', 'rate', 'data', 'value']))
                    
                    if data_elements:
                        print(f"  Found {len(data_elements)} potential data elements")
                        for elem in data_elements[:3]:
                            text = elem.get_text(strip=True)
                            if text and len(text) < 100:
                                print(f"    - {text}")
            else:
                print(f"✗ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"✗ Error: {str(e)[:100]}")

def main():
    """Main exploration function"""
    
    print("\n🔍 KB Land Data Portal Exploration\n")
    
    # Explore website structure
    findings = explore_kb_land()
    
    # Try to get actual data
    check_kb_actual_data()
    
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    print("\nKB Land appears to provide:")
    print("1. Housing price indices (apartment, house, land)")
    print("2. Jeonse (deposit) rate trends")
    print("3. Transaction volume statistics")
    print("4. Regional market analysis")
    print("5. Price trends by property type")
    print("6. Market outlook and forecasts")
    print("\nNote: KB Land data is primarily visual/dashboard-based")
    print("Direct API access may be limited - web scraping required")

if __name__ == "__main__":
    main()