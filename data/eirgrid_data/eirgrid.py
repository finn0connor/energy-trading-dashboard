import requests
import pandas as pd
from datetime import datetime


BASE_URL = "https://www.smartgriddashboard.com/api/chart/"


def _format_date(date_str: str) -> str:
    """Convert YYYY-MM-DD to DD-MMM-YYYY"""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return dt.strftime('%d-%b-%Y')


def _fetch_data(chart_type: str, areas: str, start: str, end: str, region: str = "ALL") -> pd.DataFrame:
    """
    Fetch data from EirGrid Smart Grid Dashboard
    """
    params = {
        'region': region,
        'chartType': chart_type,
        'dateRange': 'day',
        'dateFrom': _format_date(start),
        'dateTo': _format_date(end),
        'areas': areas
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
        'eirgrid-content-request': 'Nextjs',
        'Referer': 'https://www.smartgriddashboard.com/'
    }
    
    response = requests.get(BASE_URL, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")
    
    data = response.json()
    
    if not isinstance(data, dict) or 'Rows' not in data:
        return pd.DataFrame()
    
    rows = data['Rows']
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows)
    
    # Rename columns
    df = df.rename(columns={
        'Value': 'value',
        'EffectiveTime': 'timestamp',
        'Region': 'region',
        'FieldName': 'field'
    })
    
    # Parse timestamp and convert to ISO string for JSON serialization
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%b-%Y %H:%M:%S')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    
    # Drop null values
    df = df.dropna(subset=['value'])
    
    # Map field names to area
    field_mapping = {
        'WIND_ACTUAL': 'actual',
        'WIND_FCAST': 'forecast',
        'SYSTEM_DEMAND': 'actual',
        'DEMAND_FORECAST_VALUE': 'forecast'
    }
    df['area'] = df['field'].map(field_mapping)
    
    return df


def get_wind(start: str, end: str, region: str = "ALL") -> pd.DataFrame:
    """
    Get wind generation actual and forecast
    """
    return _fetch_data('wind', 'windactual,windforecast', start, end, region)


def get_demand(start: str, end: str, region: str = "ALL") -> pd.DataFrame:
    """
    Get demand actual and forecast
    """
    return _fetch_data('demand', 'demandactual,demandforecast', start, end, region)


# Test
if __name__ == '__main__':
    from datetime import timedelta
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    start = yesterday.strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')
    
    print(f"=== Demand Data ({start} to {end}) ===")
    demand = get_demand(start, end)
    print(demand.head())
    print(f"\nTimestamp format: {demand['timestamp'].iloc[0]}")