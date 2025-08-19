"""
Data Merger and Aggregation Module for Korean Macro Data
Provides flexible time-based aggregation and standardized English column names
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List, Optional, Union, Literal
import warnings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KoreanMacroDataMerger:
    """
    Merge and aggregate Korean macroeconomic data with standardized English columns
    """
    
    # Column name mapping: Korean/Original -> English
    COLUMN_MAPPINGS = {
        # BOK columns
        'STAT_CODE': 'stat_code',
        'STAT_NAME': 'stat_name',
        'ITEM_CODE1': 'item_code',
        'ITEM_NAME1': 'item_name',
        'DATA_VALUE': 'value',
        'TIME': 'date',
        'UNIT_NAME': 'unit',
        
        # KOSIS columns
        'PRD_DE': 'date',
        'C1_NM': 'region',
        'C2_NM': 'category',
        'DT': 'value',
        'UNIT_NM': 'unit',
        
        # FRED columns
        'realtime_start': 'realtime_start',
        'realtime_end': 'realtime_end',
        'date': 'date',
        'value': 'value',
        
        # KB Land columns (Korean)
        '날짜': 'date',
        '시점': 'date',
        '지역': 'region',
        '구분': 'category',
        '종합': 'total_index',
        '아파트': 'apartment_index',
        '단독주택': 'detached_house_index',
        '연립주택': 'row_house_index',
        '서울': 'seoul',
        '강남': 'gangnam',
        '강북': 'gangbuk',
        '경기': 'gyeonggi',
        '인천': 'incheon',
        '수도권': 'capital_area',
        '지방': 'regional',
        '매매': 'sale_price',
        '전세': 'jeonse_price',
        '월세': 'monthly_rent',
        '거래량': 'transaction_volume',
        '심리지수': 'sentiment_index',
    }
    
    def __init__(self, data_dir: Union[str, Path] = None):
        """
        Initialize the data merger
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = Path(data_dir) if data_dir else Path('.')
        self.datasets = {}
        self.merged_data = None
        
    def standardize_columns(self, df: pd.DataFrame, source: str = 'auto') -> pd.DataFrame:
        """
        Standardize column names to English
        
        Args:
            df: DataFrame to standardize
            source: Data source ('bok', 'kosis', 'fred', 'kb', 'auto')
        
        Returns:
            DataFrame with standardized column names
        """
        df = df.copy()
        
        # Rename columns based on mapping
        for old_col, new_col in self.COLUMN_MAPPINGS.items():
            if old_col in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # Ensure date column is datetime
        date_columns = ['date', 'TIME', 'PRD_DE', '날짜', '시점']
        for col in date_columns:
            if col in df.columns:
                try:
                    # Handle different date formats
                    if df[col].dtype == 'object':
                        # Try different date formats
                        if '.' in str(df[col].iloc[0]):
                            # BOK format: 2024.01
                            df['date'] = pd.to_datetime(df[col], format='%Y.%m', errors='coerce')
                        elif len(str(df[col].iloc[0])) == 8:
                            # YYYYMMDD format
                            df['date'] = pd.to_datetime(df[col], format='%Y%m%d', errors='coerce')
                        elif len(str(df[col].iloc[0])) == 6:
                            # YYYYMM format
                            df['date'] = pd.to_datetime(df[col], format='%Y%m', errors='coerce')
                        else:
                            df['date'] = pd.to_datetime(df[col], errors='coerce')
                    else:
                        df['date'] = pd.to_datetime(df[col], errors='coerce')
                    
                    if col != 'date':
                        df = df.drop(columns=[col])
                except:
                    logger.warning(f"Could not parse date column: {col}")
        
        return df
    
    def load_data(self, 
                  filepath: Union[str, Path], 
                  data_name: str,
                  source: str = 'auto',
                  **kwargs) -> pd.DataFrame:
        """
        Load and standardize a data file
        
        Args:
            filepath: Path to data file
            data_name: Name for this dataset
            source: Data source type
            **kwargs: Additional arguments for pd.read_csv/read_excel
        
        Returns:
            Standardized DataFrame
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Load based on file extension
        if filepath.suffix.lower() == '.xlsx':
            df = pd.read_excel(filepath, **kwargs)
        else:
            # Try UTF-8 with BOM first, then regular UTF-8
            try:
                df = pd.read_csv(filepath, encoding='utf-8-sig', **kwargs)
            except:
                df = pd.read_csv(filepath, **kwargs)
        
        # Standardize columns
        df = self.standardize_columns(df, source)
        
        # Store dataset
        self.datasets[data_name] = df
        logger.info(f"Loaded {data_name}: {len(df)} rows, {list(df.columns)[:5]}...")
        
        return df
    
    def aggregate_time_series(self,
                            df: pd.DataFrame,
                            freq: Literal['D', 'W', 'M', 'Q', 'Y'],
                            agg_func: Union[str, Dict] = 'mean',
                            value_col: str = 'value',
                            date_col: str = 'date') -> pd.DataFrame:
        """
        Aggregate time series data to specified frequency
        
        Args:
            df: DataFrame with time series data
            freq: Frequency - 'D'(daily), 'W'(weekly), 'M'(monthly), 'Q'(quarterly), 'Y'(yearly)
            agg_func: Aggregation function or dict of {column: function}
            value_col: Name of value column
            date_col: Name of date column
        
        Returns:
            Aggregated DataFrame
        """
        df = df.copy()
        
        # Ensure date column is datetime
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df = df.dropna(subset=[date_col])
        else:
            raise ValueError(f"Date column '{date_col}' not found")
        
        # Set date as index
        df = df.set_index(date_col)
        
        # Prepare aggregation
        if isinstance(agg_func, str):
            # Simple aggregation for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            agg_dict = {col: agg_func for col in numeric_cols}
        else:
            agg_dict = agg_func
        
        # Resample and aggregate
        freq_map = {
            'D': 'D',   # Daily
            'W': 'W',   # Weekly (Sunday)
            'M': 'M',   # Month end
            'Q': 'Q',   # Quarter end
            'Y': 'Y'    # Year end
        }
        
        resampled = df.resample(freq_map[freq])
        
        # Apply aggregation
        if agg_dict:
            result = resampled.agg(agg_dict)
        else:
            result = resampled.mean()  # Default to mean for all numeric columns
        
        # Reset index
        result = result.reset_index()
        result = result.rename(columns={result.columns[0]: 'date'})
        
        # Add frequency indicator
        result['frequency'] = freq
        
        return result
    
    def merge_datasets(self,
                      datasets: Dict[str, pd.DataFrame] = None,
                      on: str = 'date',
                      how: str = 'outer',
                      freq: Optional[str] = None) -> pd.DataFrame:
        """
        Merge multiple datasets on a common column (usually date)
        
        Args:
            datasets: Dict of {name: DataFrame} to merge, uses self.datasets if None
            on: Column to merge on
            how: Merge type ('outer', 'inner', 'left', 'right')
            freq: If provided, aggregate all data to this frequency before merging
        
        Returns:
            Merged DataFrame
        """
        if datasets is None:
            datasets = self.datasets
        
        if not datasets:
            raise ValueError("No datasets to merge")
        
        # Aggregate to common frequency if specified
        if freq:
            aggregated_datasets = {}
            for name, df in datasets.items():
                try:
                    # Try to aggregate if it has date and value columns
                    if 'date' in df.columns and any(col in df.columns for col in ['value', 'index']):
                        aggregated_datasets[name] = self.aggregate_time_series(df, freq)
                    else:
                        aggregated_datasets[name] = df
                except Exception as e:
                    logger.warning(f"Could not aggregate {name}: {e}")
                    aggregated_datasets[name] = df
            datasets = aggregated_datasets
        
        # Start with first dataset
        dataset_names = list(datasets.keys())
        merged = datasets[dataset_names[0]].copy()
        
        # Add source column for first dataset
        merged[f'source_{dataset_names[0]}'] = True
        
        # Rename value columns to include source
        if 'value' in merged.columns:
            merged = merged.rename(columns={'value': f'value_{dataset_names[0]}'})
        
        # Merge remaining datasets
        for name in dataset_names[1:]:
            df = datasets[name].copy()
            
            # Add source column
            df[f'source_{name}'] = True
            
            # Rename value column
            if 'value' in df.columns:
                df = df.rename(columns={'value': f'value_{name}'})
            
            # Prepare for merge - keep only necessary columns
            merge_cols = [on] + [col for col in df.columns if col != on]
            df = df[merge_cols]
            
            # Merge
            merged = pd.merge(merged, df, on=on, how=how, suffixes=('', f'_{name}'))
        
        # Sort by date if it exists
        if 'date' in merged.columns:
            merged = merged.sort_values('date')
        
        # Fill source columns
        for name in dataset_names:
            if f'source_{name}' in merged.columns:
                merged[f'source_{name}'] = merged[f'source_{name}'].fillna(False)
        
        self.merged_data = merged
        return merged
    
    def create_research_dataset(self,
                               freq: str = 'M',
                               start_date: str = None,
                               end_date: str = None) -> pd.DataFrame:
        """
        Create a unified research dataset with all available data
        
        Args:
            freq: Target frequency for aggregation
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            Unified research DataFrame
        """
        if not self.datasets:
            raise ValueError("No datasets loaded. Use load_data() first.")
        
        # Merge all datasets
        merged = self.merge_datasets(freq=freq)
        
        # Filter by date range if specified
        if 'date' in merged.columns:
            if start_date:
                merged = merged[merged['date'] >= pd.to_datetime(start_date)]
            if end_date:
                merged = merged[merged['date'] <= pd.to_datetime(end_date)]
        
        # Calculate additional features
        merged = self.add_derived_features(merged)
        
        return merged
    
    def add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add derived features useful for analysis
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with additional features
        """
        df = df.copy()
        
        if 'date' in df.columns:
            df['year'] = pd.to_datetime(df['date']).dt.year
            df['quarter'] = pd.to_datetime(df['date']).dt.quarter
            df['month'] = pd.to_datetime(df['date']).dt.month
            df['week'] = pd.to_datetime(df['date']).dt.isocalendar().week
            df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
            df['is_quarter_end'] = pd.to_datetime(df['date']).dt.is_quarter_end
            df['is_month_end'] = pd.to_datetime(df['date']).dt.is_month_end
        
        # Calculate percentage changes for value columns
        value_cols = [col for col in df.columns if 'value' in col.lower() or 'index' in col.lower()]
        for col in value_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[f'{col}_pct_change'] = df[col].pct_change() * 100
                df[f'{col}_pct_change_yoy'] = df[col].pct_change(12) * 100  # Year-over-year
        
        return df
    
    def save_merged_data(self,
                        filepath: Union[str, Path],
                        format: str = 'csv',
                        run_integrity_check: bool = True) -> Optional[bool]:
        """
        Save merged data to file with automatic integrity checking
        
        Args:
            filepath: Output file path
            format: Output format ('csv', 'excel', 'parquet')
            run_integrity_check: Whether to run integrity check after saving (default: True)
            
        Returns:
            bool: True if integrity check passed, False if issues found, None if check skipped
        """
        if self.merged_data is None:
            raise ValueError("No merged data to save. Run merge_datasets() first.")
        
        filepath = Path(filepath)
        
        if format == 'csv':
            self.merged_data.to_csv(filepath, index=False, encoding='utf-8-sig')
        elif format == 'excel':
            self.merged_data.to_excel(filepath, index=False)
        elif format == 'parquet':
            self.merged_data.to_parquet(filepath, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Saved merged data to {filepath}")
        
        # Run integrity check if requested
        if run_integrity_check and format == 'csv':
            return self._run_integrity_check(filepath)
        
        return None
    
    def _run_integrity_check(self, filepath: Union[str, Path]) -> bool:
        """
        Run integrity check on saved file
        
        Args:
            filepath: Path to the saved CSV file
            
        Returns:
            bool: True if all checks passed, False if issues found
        """
        print("\n" + "="*60)
        print("RUNNING AUTOMATIC INTEGRITY CHECK")
        print("="*60)
        
        try:
            from data_integrity_checker import DataIntegrityChecker
            checker = DataIntegrityChecker()
            
            # Run full integrity check
            checker.check_merge_integrity(str(filepath))
            
            # Report results
            if checker.issues:
                print("\n⚠️ WARNING: Integrity issues detected!")
                for issue in checker.issues:
                    print(f"   • {issue}")
                print("\nReview data_integrity_report.txt for details.")
                return False
            else:
                print("\n✅ All integrity checks passed!")
                print("The merged data is ready for analysis.")
                return True
                
        except ImportError:
            print("⚠️ Integrity checker module not available.")
            print("To enable automatic integrity checking, ensure data_integrity_checker.py is available.")
            return None
        except Exception as e:
            print(f"⚠️ Error during integrity check: {e}")
            return None
    
    def get_data_summary(self) -> pd.DataFrame:
        """
        Get summary statistics for all loaded datasets
        
        Returns:
            Summary DataFrame
        """
        summary = []
        
        for name, df in self.datasets.items():
            info = {
                'dataset': name,
                'rows': len(df),
                'columns': len(df.columns),
                'date_range': None,
                'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
                'missing_values': df.isnull().sum().sum()
            }
            
            if 'date' in df.columns:
                try:
                    dates = pd.to_datetime(df['date'], errors='coerce').dropna()
                    if len(dates) > 0:
                        info['date_range'] = f"{dates.min().date()} to {dates.max().date()}"
                except:
                    pass
            
            summary.append(info)
        
        return pd.DataFrame(summary)


# Convenience functions
def quick_merge_korean_data(
    bok_files: List[str] = None,
    kb_files: List[str] = None,
    fred_files: List[str] = None,
    kosis_files: List[str] = None,
    frequency: str = 'M',
    output_file: str = 'merged_korean_macro_data.csv'
) -> pd.DataFrame:
    """
    Quick function to merge Korean macroeconomic data
    
    Args:
        bok_files: List of BOK data file paths
        kb_files: List of KB Land data file paths
        fred_files: List of FRED data file paths
        kosis_files: List of KOSIS data file paths
        frequency: Target frequency ('D', 'W', 'M', 'Q', 'Y')
        output_file: Output file path
    
    Returns:
        Merged DataFrame
    """
    merger = KoreanMacroDataMerger()
    
    # Load all data files
    all_files = []
    
    if bok_files:
        for i, file in enumerate(bok_files):
            name = f"bok_{Path(file).stem}"
            merger.load_data(file, name, source='bok')
            all_files.append(name)
    
    if kb_files:
        for i, file in enumerate(kb_files):
            name = f"kb_{Path(file).stem}"
            merger.load_data(file, name, source='kb')
            all_files.append(name)
    
    if fred_files:
        for i, file in enumerate(fred_files):
            name = f"fred_{Path(file).stem}"
            merger.load_data(file, name, source='fred')
            all_files.append(name)
    
    if kosis_files:
        for i, file in enumerate(kosis_files):
            name = f"kosis_{Path(file).stem}"
            merger.load_data(file, name, source='kosis')
            all_files.append(name)
    
    # Create research dataset
    merged = merger.create_research_dataset(freq=frequency)
    
    # Save
    merger.save_merged_data(output_file, format='csv')
    
    print(f"Successfully merged {len(all_files)} datasets")
    print(f"Output shape: {merged.shape}")
    print(f"Date range: {merged['date'].min()} to {merged['date'].max()}")
    print(f"Saved to: {output_file}")
    
    return merged


if __name__ == "__main__":
    # Example usage
    print("Korean Macro Data Merger - Example Usage")
    print("="*60)
    
    # Initialize merger
    merger = KoreanMacroDataMerger()
    
    # Example: Load some data files
    # merger.load_data('bok_data_final/bok_base_rate.csv', 'base_rate', source='bok')
    # merger.load_data('fred_data/us_federal_funds_rate.csv', 'fed_rate', source='fred')
    
    # Merge with monthly aggregation
    # merged = merger.create_research_dataset(freq='M')
    
    # Get summary
    # summary = merger.get_data_summary()
    # print(summary)
    
    print("Data merger module ready for use!")