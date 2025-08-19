"""
Data Integrity Checker for Korean Macro Data Merger
Validates that dates are not shifted or misaligned during merging
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class DataIntegrityChecker:
    """
    Checks for date alignment issues and temporal shifts in merged data
    """
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.validations = []
        
    def check_date_alignment(self, original_file, merged_df, source_name, date_col='date', value_col='value'):
        """
        Check if dates in original file match the merged dataframe
        """
        print(f"\n🔍 Checking {source_name}...")
        print("-" * 50)
        
        try:
            # Load original data
            if original_file.endswith('.csv'):
                original = pd.read_csv(original_file, encoding='utf-8-sig')
            else:
                print(f"  ⚠️ Skipping {source_name} - not a CSV file")
                return
            
            # Parse dates based on source type
            if 'TIME' in original.columns:  # BOK data
                original['parsed_date'] = pd.to_datetime(original['TIME'].astype(str), 
                                                        format='%Y%m%d', errors='coerce')
                if original['parsed_date'].isna().all():
                    original['parsed_date'] = pd.to_datetime(original['TIME'].astype(str), 
                                                            format='%Y.%m', errors='coerce')
                original_value_col = 'DATA_VALUE'
                
            elif 'date' in original.columns:  # FRED data
                original['parsed_date'] = pd.to_datetime(original['date'])
                original_value_col = 'value'
                
            elif 'PRD_DE' in original.columns:  # KOSIS data
                # Check if annual or monthly
                if original['PRD_DE'].astype(str).str.len().mode()[0] == 4:  # Annual
                    original['parsed_date'] = pd.to_datetime(original['PRD_DE'].astype(str) + '0101', 
                                                            format='%Y%m%d')
                else:  # Monthly
                    original['parsed_date'] = pd.to_datetime(original['PRD_DE'].astype(str) + '01', 
                                                            format='%Y%m%d')
                original_value_col = 'DT'
            else:
                print(f"  ⚠️ Cannot identify date column in {source_name}")
                return
            
            # Convert values to numeric
            original['original_value'] = pd.to_numeric(original[original_value_col], errors='coerce')
            
            # Filter valid data
            original_valid = original[['parsed_date', 'original_value']].dropna()
            
            if original_valid.empty:
                print(f"  ⚠️ No valid data found in {source_name}")
                return
            
            # For daily data, aggregate to monthly for comparison
            original_valid = original_valid.set_index('parsed_date')
            original_monthly = original_valid.resample('M').mean().reset_index()
            original_monthly['parsed_date'] = original_monthly['parsed_date'].dt.to_period('M').dt.to_timestamp()
            
            # Get corresponding column in merged data
            value_column = f"{source_name}_value"
            if value_column not in merged_df.columns:
                print(f"  ⚠️ Column {value_column} not found in merged data")
                return
            
            # Compare dates and values
            merged_subset = merged_df[['date', value_column]].copy()
            merged_subset = merged_subset[merged_subset[value_column].notna()]
            
            # Check for date shifts
            date_shifts = []
            value_mismatches = []
            
            for idx, row in original_monthly.iterrows():
                orig_date = row['parsed_date']
                orig_value = row['original_value']
                
                # Skip if NaT or NaN
                if pd.isna(orig_date) or pd.isna(orig_value):
                    continue
                
                # Find this date in merged data
                merged_row = merged_subset[merged_subset['date'] == orig_date]
                
                if merged_row.empty:
                    # Check if value appears on a different date (shifted)
                    value_matches = merged_subset[
                        np.abs(merged_subset[value_column] - orig_value) < 0.01
                    ]
                    
                    if not value_matches.empty:
                        shifted_date = value_matches.iloc[0]['date']
                        if pd.notna(shifted_date) and pd.notna(orig_date):
                            days_shifted = (shifted_date - orig_date).days
                            date_shifts.append({
                                'original_date': orig_date,
                                'shifted_to': shifted_date,
                                'days_shifted': days_shifted,
                                'value': orig_value
                            })
                else:
                    # Check if values match
                    merged_value = merged_row.iloc[0][value_column]
                    if abs(merged_value - orig_value) > 0.01:
                        value_mismatches.append({
                            'date': orig_date,
                            'original_value': orig_value,
                            'merged_value': merged_value,
                            'difference': merged_value - orig_value
                        })
            
            # Report findings
            if date_shifts:
                print(f"  ❌ DATE SHIFTS DETECTED: {len(date_shifts)} dates misaligned")
                for shift in date_shifts[:5]:  # Show first 5
                    print(f"     {shift['original_date'].strftime('%Y-%m-%d')} → "
                          f"{shift['shifted_to'].strftime('%Y-%m-%d')} "
                          f"({shift['days_shifted']} days)")
                if len(date_shifts) > 5:
                    print(f"     ... and {len(date_shifts) - 5} more")
                self.issues.append(f"{source_name}: {len(date_shifts)} date shifts")
            
            if value_mismatches:
                print(f"  ⚠️ VALUE MISMATCHES: {len(value_mismatches)} values differ")
                for mismatch in value_mismatches[:3]:  # Show first 3
                    print(f"     {mismatch['date'].strftime('%Y-%m-%d')}: "
                          f"{mismatch['original_value']:.2f} → {mismatch['merged_value']:.2f} "
                          f"(diff: {mismatch['difference']:.2f})")
                if len(value_mismatches) > 3:
                    print(f"     ... and {len(value_mismatches) - 3} more")
                self.warnings.append(f"{source_name}: {len(value_mismatches)} value mismatches")
            
            if not date_shifts and not value_mismatches:
                print(f"  ✅ Perfect alignment - no date shifts or value mismatches")
                self.validations.append(f"{source_name}: perfectly aligned")
            
            # Additional checks
            self._check_frequency_consistency(original_monthly, merged_subset, source_name)
            
        except Exception as e:
            print(f"  ❌ Error checking {source_name}: {e}")
            self.issues.append(f"{source_name}: error during validation - {str(e)}")
    
    def _check_frequency_consistency(self, original, merged, source_name):
        """
        Check if data frequency is consistent (no unexpected gaps)
        """
        # Check for unexpected gaps in original data
        if len(original) > 1:
            date_diffs = original['parsed_date'].diff().dt.days
            expected_monthly_gap = 30  # Approximate
            
            large_gaps = date_diffs[date_diffs > expected_monthly_gap * 1.5].dropna()
            if len(large_gaps) > 0:
                max_gap = large_gaps.max()
                print(f"  ⚠️ Frequency gaps detected: largest gap is {max_gap:.0f} days")
                self.warnings.append(f"{source_name}: irregular frequency (max gap: {max_gap:.0f} days)")
    
    def check_merge_integrity(self, merged_file='korean_macro_complete.csv'):
        """
        Comprehensive integrity check for the merged dataset
        """
        print("=" * 80)
        print("DATA INTEGRITY VALIDATION REPORT")
        print("Checking for date shifts and temporal misalignments")
        print("=" * 80)
        
        # Load merged data
        merged_df = pd.read_csv(merged_file)
        merged_df['date'] = pd.to_datetime(merged_df['date'])
        
        # Check BOK data sources
        bok_sources = {
            'base_rate': 'bok_data_final/bok_base_rate.csv',
            'usd_krw': 'bok_data_final/bok_usd_krw_exchange_rate.csv',
            'eur_krw': 'bok_data_final/bok_eur_krw_exchange_rate.csv',
            'cny_krw': 'bok_data_final/bok_cny_krw_exchange_rate.csv'
        }
        
        print("\n📊 CHECKING BOK DATA SOURCES")
        print("=" * 40)
        for name, filepath in bok_sources.items():
            if Path(filepath).exists():
                self.check_date_alignment(filepath, merged_df, name)
        
        # Check FRED data sources
        fred_sources = {
            'fed_rate': 'research_data_fixed/fred_us_federal_funds_rate.csv',
            'us_10y': 'research_data_fixed/fred_us_10-year_treasury.csv',
            'vix': 'research_data_fixed/fred_vix_index.csv',
            'us_gdp': 'research_data_fixed/fred_us_gdp_growth.csv',
            'wti_oil': 'research_data_fixed/fred_wti_oil_price.csv',
            'brent_oil': 'research_data_fixed/fred_brent_oil_price.csv',
            'dxy': 'research_data_fixed/fred_dxy_dollar_index.csv',
            'china_gdp': 'research_data_fixed/fred_china_gdp.csv'
        }
        
        print("\n📊 CHECKING FRED DATA SOURCES")
        print("=" * 40)
        for name, filepath in fred_sources.items():
            if Path(filepath).exists():
                self.check_date_alignment(filepath, merged_df, name)
        
        # Check KOSIS data sources
        kosis_sources = {
            'employment': 'research_data_fixed/kosis_DT_1DA7001.csv',
            'demographics': 'research_data_fixed/kosis_DT_1B8000F.csv'
        }
        
        print("\n📊 CHECKING KOSIS DATA SOURCES")
        print("=" * 40)
        for name, filepath in kosis_sources.items():
            if Path(filepath).exists():
                self.check_date_alignment(filepath, merged_df, name)
        
        # Generate summary report
        self._generate_summary_report(merged_df)
    
    def _generate_summary_report(self, merged_df):
        """
        Generate a comprehensive summary report
        """
        print("\n" + "=" * 80)
        print("INTEGRITY CHECK SUMMARY")
        print("=" * 80)
        
        # Overall status
        if self.issues:
            print("\n❌ CRITICAL ISSUES FOUND:")
            for issue in self.issues:
                print(f"   • {issue}")
        else:
            print("\n✅ NO CRITICAL ISSUES - All dates properly aligned")
        
        if self.warnings:
            print("\n⚠️ WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.validations:
            print("\n✅ VALIDATED SOURCES:")
            for validation in self.validations:
                print(f"   • {validation}")
        
        # Check for systematic patterns
        print("\n📈 SYSTEMATIC CHECKS:")
        
        # Check if dates are monotonic
        if merged_df['date'].is_monotonic_increasing:
            print("   ✅ Dates are properly ordered (monotonic increasing)")
        else:
            print("   ❌ Dates are NOT properly ordered!")
            self.issues.append("Date ordering issue in merged data")
        
        # Check for duplicate dates
        duplicates = merged_df['date'].duplicated().sum()
        if duplicates == 0:
            print("   ✅ No duplicate dates found")
        else:
            print(f"   ❌ Found {duplicates} duplicate dates!")
            self.issues.append(f"{duplicates} duplicate dates in merged data")
        
        # Check date continuity
        expected_dates = pd.date_range(start=merged_df['date'].min(), 
                                      end=merged_df['date'].max(), 
                                      freq='MS')
        missing_dates = set(expected_dates) - set(merged_df['date'])
        
        if len(missing_dates) == 0:
            print("   ✅ Date series is complete (no missing months)")
        else:
            print(f"   ❌ Missing {len(missing_dates)} months in date series!")
            self.issues.append(f"{len(missing_dates)} missing months")
        
        # Final verdict
        print("\n" + "=" * 80)
        if not self.issues:
            print("🎯 FINAL VERDICT: DATA INTEGRITY VALIDATED")
            print("All temporal alignments are correct. No date shifts detected.")
        else:
            print("⚠️ FINAL VERDICT: INTEGRITY ISSUES DETECTED")
            print(f"Found {len(self.issues)} critical issues that need attention.")
        print("=" * 80)
        
        # Save detailed report
        self._save_detailed_report(merged_df)
    
    def _save_detailed_report(self, merged_df):
        """
        Save a detailed integrity report to file
        """
        report_file = 'data_integrity_report.txt'
        
        with open(report_file, 'w') as f:
            f.write("DATA INTEGRITY VALIDATION REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("MERGED DATA STATISTICS:\n")
            f.write(f"- Total rows: {len(merged_df)}\n")
            f.write(f"- Date range: {merged_df['date'].min()} to {merged_df['date'].max()}\n")
            f.write(f"- Total columns: {len(merged_df.columns)}\n\n")
            
            if self.issues:
                f.write("CRITICAL ISSUES:\n")
                for issue in self.issues:
                    f.write(f"- {issue}\n")
                f.write("\n")
            
            if self.warnings:
                f.write("WARNINGS:\n")
                for warning in self.warnings:
                    f.write(f"- {warning}\n")
                f.write("\n")
            
            if self.validations:
                f.write("VALIDATED SOURCES:\n")
                for validation in self.validations:
                    f.write(f"- {validation}\n")
                f.write("\n")
            
            f.write("=" * 80 + "\n")
            f.write(f"Total Issues: {len(self.issues)}\n")
            f.write(f"Total Warnings: {len(self.warnings)}\n")
            f.write(f"Total Validated: {len(self.validations)}\n")
        
        print(f"\n📄 Detailed report saved to: {report_file}")


def main():
    """
    Run comprehensive integrity check on merged data
    """
    checker = DataIntegrityChecker()
    
    # Check if merged file exists
    if not Path('korean_macro_complete.csv').exists():
        print("❌ Error: korean_macro_complete.csv not found!")
        print("Please run merge_data_complete.py first.")
        return
    
    # Run integrity check
    checker.check_merge_integrity('korean_macro_complete.csv')
    
    # Return checker for further analysis if needed
    return checker


if __name__ == "__main__":
    checker = main()