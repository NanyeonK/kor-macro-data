"""Dataset Discovery Tool - List and search all available Korean data statistics"""

import os
import json
import pandas as pd
from typing import Dict, List, Optional
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class DatasetDiscovery:
    """Discover and search available datasets from Korean APIs"""
    
    def __init__(self):
        self.bok_api_key = os.getenv('BOK_API_KEY')
        self.kosis_api_key = os.getenv('KOSIS_API_KEY')
        self.seoul_api_key = os.getenv('SEOUL_API_KEY')
        self.results_dir = Path("dataset_lists")
        self.results_dir.mkdir(exist_ok=True)
        
    def discover_bok_statistics(self, save_to_file=True) -> List[Dict]:
        """
        Discover all available BOK ECOS statistics
        
        BOK provides a StatisticTableList endpoint to get all available statistics
        """
        print("\n" + "="*60)
        print("Discovering Bank of Korea (BOK) Statistics")
        print("="*60)
        
        try:
            # BOK API endpoint for listing all statistics
            url = f"https://ecos.bok.or.kr/api/StatisticTableList/{self.bok_api_key}/json/kr/1/100000/"
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            statistics = []
            if 'StatisticTableList' in data and 'row' in data['StatisticTableList']:
                rows = data['StatisticTableList']['row']
                
                for row in rows:
                    stat = {
                        'stat_code': row.get('STAT_CODE', ''),
                        'stat_name': row.get('STAT_NAME', ''),
                        'cycle': row.get('CYCLE', ''),  # D: Daily, M: Monthly, Q: Quarterly, Y: Yearly
                        'source': row.get('ORG_NAME', ''),
                        'start_time': row.get('START_TIME', ''),
                        'end_time': row.get('END_TIME', ''),
                        'item_code': row.get('ITEM_CODE', ''),
                        'item_name': row.get('ITEM_NAME', '')
                    }
                    statistics.append(stat)
                
                print(f"✓ Found {len(statistics)} BOK statistics")
                
                if save_to_file:
                    # Save to CSV
                    df = pd.DataFrame(statistics)
                    csv_path = self.results_dir / "bok_all_statistics.csv"
                    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                    print(f"  Saved to: {csv_path}")
                    
                    # Also save a summary by category
                    summary = df.groupby('cycle').agg({
                        'stat_code': 'count',
                        'stat_name': lambda x: list(x)[:5]  # Sample 5 names
                    }).rename(columns={'stat_code': 'count'})
                    
                    print("\nBOK Statistics by Period:")
                    print(f"  Daily: {len(df[df['cycle'] == 'D'])} datasets")
                    print(f"  Monthly: {len(df[df['cycle'] == 'M'])} datasets")
                    print(f"  Quarterly: {len(df[df['cycle'] == 'Q'])} datasets")
                    print(f"  Yearly: {len(df[df['cycle'] == 'Y'])} datasets")
                
                return statistics
                
        except Exception as e:
            print(f"✗ Error discovering BOK statistics: {e}")
            return []
    
    def discover_kosis_statistics(self, org_id='101', save_to_file=True) -> List[Dict]:
        """
        Discover KOSIS statistics for a given organization
        
        org_id: Organization ID (101=Statistics Korea, 301=Seoul, etc.)
        """
        print("\n" + "="*60)
        print("Discovering KOSIS Statistics")
        print("="*60)
        
        try:
            # KOSIS API endpoint for listing statistics
            url = "https://kosis.kr/openapi/statisticsList.do"
            
            params = {
                'method': 'getList',
                'apiKey': self.kosis_api_key,
                'vwCd': 'MT_ZTITLE',  # View code for listing
                'parentListId': 'M',   # Parent list
                'format': 'json',
                'jsonVD': 'Y',
                'perPage': '10000'     # Get many results
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Try to parse response
            try:
                data = response.json()
            except:
                # KOSIS sometimes returns non-JSON for list requests
                # Try alternate endpoint
                url2 = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
                params2 = {
                    'method': 'getMeta',
                    'apiKey': self.kosis_api_key,
                    'orgId': org_id,
                    'format': 'json'
                }
                response = requests.get(url2, params=params2, timeout=30)
                data = response.json() if response.status_code == 200 else []
            
            statistics = []
            
            # Parse KOSIS response (structure varies)
            if isinstance(data, list):
                for item in data:
                    stat = {
                        'tbl_id': item.get('TBL_ID', ''),
                        'tbl_nm': item.get('TBL_NM', ''),
                        'org_id': item.get('ORG_ID', org_id),
                        'list_id': item.get('LIST_ID', ''),
                        'vw_cd': item.get('VW_CD', ''),
                        'prd_de': item.get('PRD_DE', '')
                    }
                    if stat['tbl_id']:  # Only add if has ID
                        statistics.append(stat)
            
            # If no results from meta, try getting sample tables
            if not statistics:
                print("  Using sample KOSIS tables (full list requires different authentication)")
                # Provide commonly used KOSIS tables
                sample_tables = [
                    {'tbl_id': 'DT_1B040A3', 'tbl_nm': '인구총조사', 'category': 'Population'},
                    {'tbl_id': 'DT_1DA7001S', 'tbl_nm': '고용률', 'category': 'Employment'},
                    {'tbl_id': 'DT_1YL2001', 'tbl_nm': '아파트 매매가격지수', 'category': 'Real Estate'},
                    {'tbl_id': 'DT_1YL2101', 'tbl_nm': '부동산 거래현황', 'category': 'Real Estate'},
                    {'tbl_id': 'DT_1J17001', 'tbl_nm': '평균임금', 'category': 'Wages'},
                    {'tbl_id': 'DT_1C61', 'tbl_nm': '지역내총생산', 'category': 'Regional GDP'},
                    {'tbl_id': 'DT_1YL1601', 'tbl_nm': '건축허가현황', 'category': 'Construction'},
                    {'tbl_id': 'DT_1JC1501', 'tbl_nm': '가구수', 'category': 'Household'},
                ]
                statistics = sample_tables
                
            print(f"✓ Found {len(statistics)} KOSIS statistics")
            
            if save_to_file and statistics:
                # Save to CSV
                df = pd.DataFrame(statistics)
                csv_path = self.results_dir / "kosis_statistics.csv"
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                print(f"  Saved to: {csv_path}")
            
            return statistics
            
        except Exception as e:
            print(f"✗ Error discovering KOSIS statistics: {e}")
            return []
    
    def discover_seoul_datasets(self, save_to_file=True) -> List[Dict]:
        """
        Discover Seoul Open Data datasets
        
        Seoul provides a list service endpoint
        """
        print("\n" + "="*60)
        print("Discovering Seoul Open Data Datasets")
        print("="*60)
        
        try:
            # Seoul API provides OpenApiList service
            url = f"http://openapi.seoul.go.kr:8088/{self.seoul_api_key}/json/OpenApiList/1/200/"
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            datasets = []
            if 'OpenApiList' in data and 'row' in data['OpenApiList']:
                rows = data['OpenApiList']['row']
                
                for row in rows:
                    dataset = {
                        'service_name': row.get('SERVICE_NAME', ''),
                        'service_desc': row.get('SERVICE_NAME_KOR', ''),
                        'category': row.get('CATE1_NM', ''),
                        'update_cycle': row.get('UPDATE_CYCLE', ''),
                        'provider': row.get('PROVIDE_DEPT_NM', ''),
                        'url': row.get('SERVICE_URL', '')
                    }
                    datasets.append(dataset)
                
                print(f"✓ Found {len(datasets)} Seoul datasets")
                
                if save_to_file:
                    # Save to CSV
                    df = pd.DataFrame(datasets)
                    csv_path = self.results_dir / "seoul_all_datasets.csv"
                    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                    print(f"  Saved to: {csv_path}")
                    
                    # Show categories
                    if 'category' in df.columns:
                        categories = df['category'].value_counts()
                        print("\nSeoul Datasets by Category:")
                        for cat, count in categories.head(5).items():
                            print(f"  {cat}: {count} datasets")
                
                return datasets
                
        except Exception as e:
            print(f"✗ Error discovering Seoul datasets: {e}")
            # Return sample datasets as fallback
            sample_datasets = [
                {'service_name': 'RealtimeCityAir', 'service_desc': '실시간 대기환경 정보'},
                {'service_name': 'tbLnOpendataRtmsV', 'service_desc': '부동산 실거래가 정보'},
                {'service_name': 'CardSubwayStatsNew', 'service_desc': '지하철 승하차 인원 정보'},
                {'service_name': 'tbLnOpendataRentV', 'service_desc': '부동산 전월세가 정보'},
                {'service_name': 'GetParkInfo', 'service_desc': '공영주차장 정보'},
            ]
            if save_to_file:
                df = pd.DataFrame(sample_datasets)
                csv_path = self.results_dir / "seoul_sample_datasets.csv"
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                print(f"  Saved sample datasets to: {csv_path}")
            
            return sample_datasets
    
    def search_datasets(self, keyword: str, source: str = 'all') -> List[Dict]:
        """
        Search for datasets containing keyword
        
        Args:
            keyword: Search term (e.g., '부동산', 'real estate', 'GDP')
            source: 'bok', 'kosis', 'seoul', or 'all'
        """
        print(f"\nSearching for '{keyword}' in {source} datasets...")
        results = []
        
        # Load or fetch dataset lists
        if source in ['bok', 'all']:
            bok_file = self.results_dir / "bok_all_statistics.csv"
            if bok_file.exists():
                df = pd.read_csv(bok_file)
                # Search in stat_name and item_name (convert to string first)
                df['stat_name'] = df['stat_name'].astype(str)
                df['item_name'] = df['item_name'].astype(str)
                mask = df['stat_name'].str.contains(keyword, case=False, na=False) | \
                       df['item_name'].str.contains(keyword, case=False, na=False)
                matches = df[mask].to_dict('records')
                for match in matches:
                    match['source'] = 'BOK'
                results.extend(matches)
                print(f"  BOK: {len(matches)} matches")
        
        if source in ['kosis', 'all']:
            kosis_file = self.results_dir / "kosis_statistics.csv"
            if kosis_file.exists():
                df = pd.read_csv(kosis_file)
                if 'tbl_nm' in df.columns:
                    mask = df['tbl_nm'].str.contains(keyword, case=False, na=False)
                    matches = df[mask].to_dict('records')
                    for match in matches:
                        match['source'] = 'KOSIS'
                        results.extend(matches)
                    print(f"  KOSIS: {len(matches)} matches")
        
        if source in ['seoul', 'all']:
            seoul_file = self.results_dir / "seoul_all_datasets.csv"
            if not seoul_file.exists():
                seoul_file = self.results_dir / "seoul_sample_datasets.csv"
            
            if seoul_file.exists():
                df = pd.read_csv(seoul_file)
                # Search in service_name and service_desc
                mask = df['service_desc'].str.contains(keyword, case=False, na=False) if 'service_desc' in df.columns else False
                if isinstance(mask, bool):
                    mask = df['service_name'].str.contains(keyword, case=False, na=False)
                matches = df[mask].to_dict('records')
                for match in matches:
                    match['source'] = 'Seoul'
                    results.extend(matches)
                print(f"  Seoul: {len(matches)} matches")
        
        return results
    
    def generate_catalog_summary(self):
        """Generate a summary of all discovered datasets"""
        print("\n" + "="*60)
        print("Dataset Catalog Summary")
        print("="*60)
        
        summary = {
            'generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sources': {}
        }
        
        # BOK Summary
        bok_file = self.results_dir / "bok_all_statistics.csv"
        if bok_file.exists():
            df = pd.read_csv(bok_file)
            summary['sources']['BOK'] = {
                'total': len(df),
                'by_cycle': df['cycle'].value_counts().to_dict() if 'cycle' in df.columns else {}
            }
            print(f"\nBank of Korea: {len(df)} total datasets")
        
        # KOSIS Summary
        kosis_file = self.results_dir / "kosis_statistics.csv"
        if kosis_file.exists():
            df = pd.read_csv(kosis_file)
            summary['sources']['KOSIS'] = {
                'total': len(df)
            }
            print(f"KOSIS: {len(df)} datasets")
        
        # Seoul Summary
        seoul_file = self.results_dir / "seoul_all_datasets.csv"
        if not seoul_file.exists():
            seoul_file = self.results_dir / "seoul_sample_datasets.csv"
        if seoul_file.exists():
            df = pd.read_csv(seoul_file)
            summary['sources']['Seoul'] = {
                'total': len(df),
                'by_category': df['category'].value_counts().to_dict() if 'category' in df.columns else {}
            }
            print(f"Seoul Open Data: {len(df)} datasets")
        
        # Save summary
        summary_file = self.results_dir / "catalog_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\nSummary saved to: {summary_file}")
        return summary


def main():
    """Main function to discover all datasets"""
    discovery = DatasetDiscovery()
    
    # Discover all datasets
    print("\n🔍 Starting Dataset Discovery Process...")
    
    # 1. Discover BOK statistics
    bok_stats = discovery.discover_bok_statistics()
    
    # 2. Discover KOSIS statistics
    kosis_stats = discovery.discover_kosis_statistics()
    
    # 3. Discover Seoul datasets
    seoul_datasets = discovery.discover_seoul_datasets()
    
    # 4. Generate summary
    summary = discovery.generate_catalog_summary()
    
    # 5. Test search functionality
    print("\n" + "="*60)
    print("Testing Search Functionality")
    print("="*60)
    
    # Search examples
    search_terms = ['부동산', '금리', 'GDP', '인구']
    for term in search_terms:
        results = discovery.search_datasets(term)
        print(f"\nSearch '{term}': {len(results)} total results")
        if results:
            # Show first 3 results
            for i, result in enumerate(results[:3]):
                if 'stat_name' in result:
                    print(f"  [{result['source']}] {result['stat_name']}")
                elif 'tbl_nm' in result:
                    print(f"  [{result['source']}] {result['tbl_nm']}")
                elif 'service_desc' in result:
                    print(f"  [{result['source']}] {result['service_desc']}")
    
    print("\n✅ Dataset discovery complete!")
    print(f"📁 Results saved in: {discovery.results_dir}")
    print("\nYou can now:")
    print("1. Browse dataset lists in the CSV files")
    print("2. Use search_datasets() to find specific data")
    print("3. Use the dataset IDs to fetch actual data")


if __name__ == "__main__":
    main()