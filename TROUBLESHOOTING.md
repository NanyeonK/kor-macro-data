# Korean Macro Data - Troubleshooting Guide

This guide helps you resolve common issues when using the Korean Macro Data package.

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [API Connection Problems](#api-connection-problems)
3. [Data Retrieval Errors](#data-retrieval-errors)
4. [Data Merging Issues](#data-merging-issues)
5. [Performance Problems](#performance-problems)
6. [Common Error Messages](#common-error-messages)
7. [FAQ](#frequently-asked-questions-faq)

---

## Installation Issues

### Problem: "ModuleNotFoundError: No module named 'kor_macro'"

**Solution:**
```bash
# Ensure package is installed
pip install kor-macro-data

# Or install from GitHub
pip install git+https://github.com/NanyeonK/kor-macro-data.git

# For development
git clone https://github.com/NanyeonK/kor-macro-data.git
cd kor-macro-data
pip install -e .
```

### Problem: "No module named 'dotenv'" or other dependencies

**Solution:**
```bash
# Install all required dependencies
pip install pandas numpy requests python-dotenv beautifulsoup4 lxml openpyxl

# Or use requirements.txt
pip install -r requirements.txt
```

### Problem: Import errors with connectors

**Solution:**
```python
# Correct import
from kor_macro.connectors import BOKConnector  # ✅

# Wrong imports
from kor_macro import BOKConnector  # ❌
import BOKConnector  # ❌
```

---

## API Connection Problems

### Problem: "BOK API key not found in environment"

**Solution:**

1. Create `.env` file in your project root:
```bash
BOK_API_KEY=your_actual_key_here
KOSIS_API_KEY=your_actual_key_here
```

2. Or set environment variable directly:
```python
import os
os.environ['BOK_API_KEY'] = 'your_key_here'
```

3. Or pass directly to connector:
```python
bok = BOKConnector()
bok.api_key = 'your_key_here'  # Override
```

### Problem: "Authentication failed" or "Invalid API key"

**Diagnostic Steps:**
```python
# Test your API key
from kor_macro.connectors import BOKConnector

bok = BOKConnector()
print(f"API Key loaded: {bok.api_key[:5]}...")  # Check first 5 chars

# Test connection
if bok.test_connection():
    print("✅ API key is valid")
else:
    print("❌ API key is invalid or expired")
```

**Solutions:**
1. Check for typos in API key
2. Ensure no extra spaces or quotes
3. Verify key hasn't expired
4. Get new key from provider

### Problem: "Connection timeout" or "Request failed"

**Solution:**
```python
# Increase timeout
connector.timeout = 60  # seconds

# Add retry logic
import time

def fetch_with_retry(connector, *args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return connector.fetch_data(*args)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise e
```

### Problem: Rate limiting errors

**Solution:**
```python
# Add delays between requests
import time

def fetch_multiple(connector, items):
    results = []
    for item in items:
        data = connector.fetch_data(item)
        results.append(data)
        time.sleep(1)  # 1 second delay
    return results

# Or use rate limiter
from time import sleep

class RateLimiter:
    def __init__(self, calls_per_second=1):
        self.delay = 1.0 / calls_per_second
        self.last_call = 0
    
    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.delay:
            sleep(self.delay - elapsed)
        self.last_call = time.time()
```

---

## Data Retrieval Errors

### Problem: "No data found for series" or empty DataFrame

**Diagnostic Script:**
```python
# Check data availability
def diagnose_data_issue(connector, series_id, start_date, end_date):
    print(f"Checking {series_id}...")
    
    # Try different date ranges
    test_ranges = [
        (start_date, end_date),  # Original
        ('2020-01-01', '2024-12-31'),  # Recent
        ('2010-01-01', '2020-12-31'),  # Historical
    ]
    
    for start, end in test_ranges:
        try:
            data = connector.fetch_data(series_id, start, end)
            if not data.empty:
                print(f"✅ Data available from {start} to {end}")
                print(f"   Records: {len(data)}")
                return data
        except Exception as e:
            print(f"❌ Failed for {start}-{end}: {e}")
    
    return None
```

### Problem: Korean characters showing as ??? or encoding errors

**Solution:**
```python
# Set encoding when reading/writing
df = pd.read_csv('file.csv', encoding='utf-8-sig')  # For Korean
df.to_csv('output.csv', encoding='utf-8-sig', index=False)

# For Excel files
df = pd.read_excel('file.xlsx', engine='openpyxl')
df.to_excel('output.xlsx', engine='openpyxl', index=False)
```

### Problem: Date parsing errors

**Solution:**
```python
# Handle different date formats
from datetime import datetime

def parse_flexible_date(date_str):
    """Parse various date formats"""
    formats = [
        '%Y-%m-%d',  # 2024-01-15
        '%Y%m%d',    # 20240115
        '%Y.%m.%d',  # 2024.01.15
        '%Y/%m/%d',  # 2024/01/15
        '%d-%m-%Y',  # 15-01-2024
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # Try pandas parser as fallback
    return pd.to_datetime(date_str)
```

---

## Data Merging Issues

### Problem: "Temporal shift detected" during integrity check

**Diagnosis:**
```python
from kor_macro.validation import DataIntegrityChecker

checker = DataIntegrityChecker()
report = checker.check_merge_integrity('merged_data.csv')

if not report['passed']:
    print("Issues found:")
    for issue in report['issues']:
        print(f"  - {issue}")
```

**Solution:**
```python
# Ensure proper date alignment
merger = KoreanMacroDataMerger()

# Load with explicit date columns
df1 = pd.read_csv('data1.csv', parse_dates=['date'])
df2 = pd.read_csv('data2.csv', parse_dates=['date'])

# Align dates before merging
df1.set_index('date', inplace=True)
df2.set_index('date', inplace=True)

# Merge with validation
merger.load_dataframe(df1, 'dataset1')
merger.load_dataframe(df2, 'dataset2')

merged = merger.create_research_dataset(freq='M')
```

### Problem: Missing data after merging

**Solution:**
```python
# Use appropriate join method
def smart_merge(dataframes, how='outer'):
    """Merge multiple dataframes intelligently"""
    
    # Start with first dataframe
    result = dataframes[0]
    
    for df in dataframes[1:]:
        # Check overlap
        overlap = result.index.intersection(df.index)
        print(f"Overlap: {len(overlap)} dates")
        
        # Merge
        result = pd.merge(
            result, df,
            left_index=True,
            right_index=True,
            how=how,  # 'outer' keeps all dates
            suffixes=('', f'_{df.name}')
        )
    
    # Fill missing values
    result = result.fillna(method='ffill', limit=1)  # Forward fill
    
    return result
```

### Problem: Duplicate columns after merging

**Solution:**
```python
# Handle duplicate columns
def clean_merged_data(df):
    """Remove duplicate columns"""
    
    # Find duplicates
    duplicates = df.columns[df.columns.duplicated()].tolist()
    
    if duplicates:
        print(f"Found duplicates: {duplicates}")
        
        # Keep first occurrence
        df = df.loc[:, ~df.columns.duplicated()]
    
    # Rename columns for clarity
    df.columns = [col.replace('value_value_', 'value_') for col in df.columns]
    
    return df
```

---

## Performance Problems

### Problem: Slow data fetching

**Solution:**
```python
# Parallel fetching
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_parallel(connector, series_list, max_workers=5):
    """Fetch multiple series in parallel"""
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(connector.fetch_data, series): series
            for series in series_list
        }
        
        # Collect results
        for future in futures:
            series = futures[future]
            try:
                results[series] = future.result(timeout=30)
            except Exception as e:
                print(f"Failed to fetch {series}: {e}")
                results[series] = pd.DataFrame()
    
    return results

# Usage
series = ['GDP', 'CPI', 'UNRATE', 'DFF']
data = fetch_parallel(fred_connector, series)
```

### Problem: High memory usage with large datasets

**Solution:**
```python
# Use chunking for large data
def process_large_dataset(filepath, chunk_size=10000):
    """Process large files in chunks"""
    
    chunks = []
    
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        # Process each chunk
        processed = chunk.groupby('date').mean()
        chunks.append(processed)
    
    # Combine chunks
    result = pd.concat(chunks)
    
    return result

# Use data types efficiently
def optimize_datatypes(df):
    """Reduce memory usage"""
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != 'object':
            c_min = df[col].min()
            c_max = df[col].max()
            
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
            else:
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
    
    return df
```

### Problem: Caching for repeated queries

**Solution:**
```python
import pickle
import os
from datetime import datetime, timedelta

class DataCache:
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_path(self, key):
        return os.path.join(self.cache_dir, f"{key}.pkl")
    
    def is_cached(self, key, max_age_hours=24):
        path = self.get_cache_path(key)
        if os.path.exists(path):
            age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(path))
            return age < timedelta(hours=max_age_hours)
        return False
    
    def load(self, key):
        with open(self.get_cache_path(key), 'rb') as f:
            return pickle.load(f)
    
    def save(self, key, data):
        with open(self.get_cache_path(key), 'wb') as f:
            pickle.dump(data, f)
    
    def fetch_with_cache(self, key, fetch_func, max_age_hours=24):
        if self.is_cached(key, max_age_hours):
            print(f"Loading from cache: {key}")
            return self.load(key)
        else:
            print(f"Fetching fresh data: {key}")
            data = fetch_func()
            self.save(key, data)
            return data

# Usage
cache = DataCache()
data = cache.fetch_with_cache(
    'bok_base_rate_2024',
    lambda: bok.get_base_rate('2024-01-01', '2024-12-31'),
    max_age_hours=24
)
```

---

## Common Error Messages

### "KeyError: 'value'"
**Cause:** Column name mismatch
**Solution:**
```python
# Check column names
print(df.columns.tolist())

# Standardize column names
df.columns = ['date', 'value'] if len(df.columns) == 2 else df.columns
```

### "ValueError: cannot reindex from a duplicate axis"
**Cause:** Duplicate dates in data
**Solution:**
```python
# Remove duplicates
df = df[~df.index.duplicated(keep='first')]

# Or aggregate duplicates
df = df.groupby(df.index).mean()
```

### "JSONDecodeError"
**Cause:** API returned non-JSON response
**Solution:**
```python
# Check response content
response = requests.get(url)
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"Response: {response.text[:200]}")  # First 200 chars
```

### "AttributeError: 'NoneType' object has no attribute 'find'"
**Cause:** Web scraping found no matching element
**Solution:**
```python
# Add error checking
element = soup.find('div', class_='data')
if element:
    data = element.text
else:
    print("Element not found - page structure may have changed")
```

---

## Frequently Asked Questions (FAQ)

### Q: How do I know what data is available?

**A:** Check these resources:
```python
# 1. List available datasets
connector.list_datasets()

# 2. Check documentation
# See DATA_CATALOG.md for complete list

# 3. Test specific series
test_series = ['GDP', 'CPI', 'UNRATE']
for series in test_series:
    try:
        data = connector.fetch_data(series, limit=1)
        print(f"✅ {series} is available")
    except:
        print(f"❌ {series} not available")
```

### Q: Why is my data not updating?

**A:** Check update schedule:
- **Real-time**: BOK exchange rates, FRED daily series
- **Daily**: Most financial markets data
- **Weekly**: KB Land housing indices, EIA energy data
- **Monthly**: Economic indicators (GDP, CPI, employment)
- **Quarterly/Annual**: World Bank, IMF data

### Q: How do I handle missing data?

**A:** Multiple strategies:
```python
# Forward fill (use last known value)
df.fillna(method='ffill', inplace=True)

# Interpolation
df.interpolate(method='linear', inplace=True)

# Drop missing
df.dropna(inplace=True)

# Custom handling
df['value'].fillna(df['value'].rolling(window=3).mean(), inplace=True)
```

### Q: Can I use this package without API keys?

**A:** Limited functionality:
- ❌ BOK: Requires API key
- ❌ KOSIS: Requires API key  
- ✅ KB Land: Works via web scraping
- ✅ FRED: Limited access without key
- ✅ World Bank: No key required
- ✅ EIA: Limited access without key

### Q: How do I export data for R/Stata/MATLAB?

**A:** See export examples:
```python
# For R
df.to_csv('data.csv')

# For Stata
df.to_stata('data.dta')

# For MATLAB
import scipy.io
scipy.io.savemat('data.mat', {'data': df.values})

# For Excel
df.to_excel('data.xlsx')
```

### Q: What's the difference between merge and join?

**A:**
- **Merge**: Combines data based on common columns
- **Join**: Combines based on index
- **Concat**: Stacks data vertically or horizontally

```python
# Merge on column
merged = pd.merge(df1, df2, on='date')

# Join on index
joined = df1.join(df2, how='outer')

# Concat vertically
combined = pd.concat([df1, df2], axis=0)
```

### Q: How do I cite this package?

**A:**
```bibtex
@software{kor_macro_data,
  title = {Korean Macro Data: A Python Package for Korean Economic Data},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/NanyeonK/kor-macro-data},
  version = {1.0.0}
}
```

---

## Getting Help

### Still having issues?

1. **Check Examples**: Look at `examples/` directory
2. **Read Docs**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
3. **GitHub Issues**: [Report a bug](https://github.com/NanyeonK/kor-macro-data/issues)
4. **Debug Mode**: Enable logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Contact

- **GitHub**: [NanyeonK/kor-macro-data](https://github.com/NanyeonK/kor-macro-data)
- **Issues**: [GitHub Issues](https://github.com/NanyeonK/kor-macro-data/issues)

---

**Remember**: Most issues are related to API keys, date formats, or rate limiting. Check these first!