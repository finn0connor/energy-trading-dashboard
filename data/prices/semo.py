import requests
import pandas as pd

def get_imbalance_prices(start_date, end_date):
    """
    Pull imbalance prices from SEMO API.
    
    Parameters:
    -----------
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing imbalance price data
    """
    
    url = "https://reports.sem-o.com/api/v1/dynamic/BM-026"
    
    params = {
        "StartTime": f">={start_date}T00:00",
        "EndTime": f"<={end_date}T23:59",
        "sort_by": "StartTime",
        "order_by": "ASC",
        "page_size": 5000
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    data = response.json()
    df = pd.DataFrame(data.get("items", []))
    
    return df