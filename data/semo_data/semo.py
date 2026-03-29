import requests
import pandas as pd


def get_imbalance_data(start_date, end_date):
    """
    Pull imbalance data from SEMO API (BM-026).
    
    Columns: ['TradeDate', 'StartTime', 'EndTime', 'NetImbalanceVolume', 'ImbalanceSettlementPrice']
    
    Parameters:
    -----------
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    
    Returns:
    --------
    pd.DataFrame
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


def get_daily_load_forecast(start_date, end_date, jurisdiction="All", 
                           participant=None, resource_name=None, resource_type=None):
    """
    Pull daily load forecast data from SEMO API (BM-010).

    Columns: ['DeliveryDate', 'TradeDate', 'StartTime', 'EndTime', 'LoadForecastROI', 'LoadForecastNI', 'AggregatedForecast']
    
    Parameters:
    -----------
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    jurisdiction : str
        'All', 'ROI', or 'NI'
    participant : str, optional
        Filter by participant name
    resource_name : str, optional
        Filter by resource/unit name
    resource_type : str, optional
        Filter by resource type
    
    Returns:
    --------
    pd.DataFrame
    """
    
    url = "https://reports.sem-o.com/api/v1/dynamic/BM-010"
    
    params = {
        "StartTime": f">={start_date}T00:00",
        "EndTime": f"<={end_date}T23:59",
        "sort_by": "StartTime",
        "order_by": "ASC",
        "Jurisdiction": jurisdiction,
        "ParticipantName": participant or "",
        "ResourceName": resource_name or "",
        "ResourceType": resource_type or "",
        "page_size": 5000
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    data = response.json()
    df = pd.DataFrame(data.get("items", []))
    
    return df


def get_wind_forecast(start_date, end_date, jurisdiction="All",
                      participant=None, resource_name=None, resource_type=None):
    """
    Pull wind forecast data from SEMO API (BM-016).

    Columns: ['DeliveryDate', 'TradeDate', 'StartTime', 'EndTime', 'LoadForecastROI', 'LoadForecastNI', 'AggregatedForecast']
    
    Parameters:
    -----------
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    jurisdiction : str
        'All', 'ROI', or 'NI'
    participant : str, optional
        Filter by participant name
    resource_name : str, optional
        Filter by resource/unit name
    resource_type : str, optional
        Filter by resource type
    
    Returns:
    --------
    pd.DataFrame
    """
    
    url = "https://reports.sem-o.com/api/v1/dynamic/BM-016"
    
    params = {
        "StartTime": f">={start_date}T00:00",
        "EndTime": f"<={end_date}T23:59",
        "sort_by": "StartTime",
        "order_by": "ASC",
        "Jurisdiction": jurisdiction,
        "ParticipantName": participant or "",
        "ResourceName": resource_name or "",
        "ResourceType": resource_type or "",
        "page_size": 5000
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    data = response.json()
    df = pd.DataFrame(data.get("items", []))
    
    return df


def get_metered_generation(start_date, end_date, participant=None, resource_name=None):
    """
    Pull daily metered generation data from SEMO API (BM-086).
    
    Can filter by either participant name or resource/unit name.

    Columns: ['TradeDate', 'ParticipantName', 'ResourceName', 'ResourceType', 'StartTime', 'EndTime', 'Jurisdiction', 'MeteredMW']
    
    Parameters:
    -----------
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    participant : str, optional
        Filter by market participant name
    resource_name : str, optional
        Filter by resource/unit name
    
    Returns:
    --------
    pd.DataFrame
    """
    
    url = "https://reports.sem-o.com/api/v1/dynamic/BM-086"
    
    params = {
        "StartTime": f">={start_date}T00:00:00<={end_date}T23:59:00",
        "sort_by": "StartTime",
        "order_by": "ASC",
        "ParticipantName": participant or "",
        "ResourceName": resource_name or "",
        "page_size": 5000
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    data = response.json()
    df = pd.DataFrame(data.get("items", []))
    
    return df


def get_interconnector_flows(start_date, end_date, jurisdiction="All",
                             participant=None, resource_name=None, resource_type=None):
    """
    Pull interconnector flows and residual capacity from SEMO API (BM-087).
    
    Includes EWIC (East-West) and Moyle interconnector data.

    Columns: ['TradeDate', 'ResourceName', 'StartTime', 'EndTime', 'MeteredFlow', 'FlowVariance', 'ResidualCapacity']
    
    Parameters:
    -----------
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    jurisdiction : str
        'All', 'ROI', or 'NI'
    participant : str, optional
        Filter by participant name
    resource_name : str, optional
        Filter by interconnector name (e.g., 'EWIC', 'Moyle')
    resource_type : str, optional
        Filter by resource type
    
    Returns:
    --------
    pd.DataFrame
    """
    
    url = "https://reports.sem-o.com/api/v1/dynamic/BM-087"
    
    params = {
        "StartTime": f">={start_date}T00:00:00<={end_date}T23:59:00",
        "sort_by": "StartTime",
        "order_by": "ASC",
        "Jurisdiction": jurisdiction,
        "ParticipantName": participant or "",
        "ResourceName": resource_name or "",
        "ResourceType": resource_type or "",
        "page_size": 5000
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    data = response.json()
    df = pd.DataFrame(data.get("items", []))
    
    return df

def get_system_frequency(start_date, end_date, jurisdiction="All",
                         participant=None, resource_name=None, resource_type=None):
    """
    Pull average system frequency data from SEMO API (BM-089).
    
    Useful for identifying system stress events.

    Columns: ['DeliveryDate', 'TradeDate', 'StartTime', 'EndTime', 'NominalFrequency', 'AverageFrequency']
    
    Parameters:
    -----------
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    jurisdiction : str
        'All', 'ROI', or 'NI'
    participant : str, optional
        Filter by participant name
    resource_name : str, optional
        Filter by resource/unit name
    resource_type : str, optional
        Filter by resource type
    
    Returns:
    --------
    pd.DataFrame
    """
    
    url = "https://reports.sem-o.com/api/v1/dynamic/BM-089"
    
    params = {
        "StartTime": f">={start_date}T00:00:00<={end_date}T23:59:00",
        "sort_by": "StartTime",
        "order_by": "ASC",
        "Jurisdiction": jurisdiction,
        "ParticipantName": participant or "",
        "ResourceName": resource_name or "",
        "ResourceType": resource_type or "",
        "page_size": 5000
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    data = response.json()
    df = pd.DataFrame(data.get("items", []))
    
    return df

def get_balancing_costs(start_date, end_date, jurisdiction="All",
                        participant=None, resource_name=None, resource_type=None):
    """
    Pull balancing and imbalance market cost data from SEMO API (BM-095).
    
    Columns: ['StartTime', 'EndTime', 'ImbalanceVolume', 'ImbalancePrice', 'ImbalanceCost']

    Parameters:
    -----------
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    jurisdiction : str
        'All', 'ROI', or 'NI'
    participant : str, optional
        Filter by participant name
    resource_name : str, optional
        Filter by resource/unit name
    resource_type : str, optional
        Filter by resource type
    
    Returns:
    --------
    pd.DataFrame
    """
    
    url = "https://reports.sem-o.com/api/v1/dynamic/BM-095"
    
    params = {
        "StartTime": f">={start_date}T00:00",
        "EndTime": f"<={end_date}T23:59",
        "sort_by": "StartTime",
        "order_by": "ASC",
        "Jurisdiction": jurisdiction,
        "ParticipantName": participant or "",
        "ResourceName": resource_name or "",
        "ResourceType": resource_type or "",
        "page_size": 5000
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    data = response.json()
    df = pd.DataFrame(data.get("items", []))
    
    return df


# Test when run directly
if __name__ == "__main__":
    # Test imbalance data
    df_imbalance = get_imbalance_data("2026-01-01", "2026-01-07")
    print("Imbalance Data:")
    print(df_imbalance.head())
    print(f"Columns: {df_imbalance.columns.tolist()}")
    
    # Test daily load forecast
    df_load = get_daily_load_forecast("2026-01-01", "2026-01-07")
    print("\nDaily Load Forecast:")
    print(df_load.head())
    print(f"Columns: {df_load.columns.tolist()}")
    
    # Test wind forecast
    df_wind = get_wind_forecast("2026-01-01", "2026-01-07")
    print("\nWind Forecast:")
    print(df_wind.head())
    print(f"Columns: {df_wind.columns.tolist()}")
    
    # Test metered generation
    df_gen = get_metered_generation("2026-01-01", "2026-01-07")
    print("\nMetered Generation:")
    print(df_gen.head())
    print(f"Columns: {df_gen.columns.tolist()}")
    
    # Test interconnector flows
    df_ic = get_interconnector_flows("2026-01-01", "2026-01-07")
    print("\nInterconnector Flows & Capacity:")
    print(df_ic.head())
    print(f"Columns: {df_ic.columns.tolist()}")

    # Test system frequency
    df_freq = get_system_frequency("2026-01-01", "2026-01-07")
    print("\nSystem Frequency:")
    print(df_freq.head())
    print(f"Columns: {df_freq.columns.tolist()}")

    # Test balancing costs
    df_costs = get_balancing_costs("2026-01-01", "2026-01-07")
    print("\nBalancing & Imbalance Costs:") 
    print(df_costs.head())
    print(f"Columns: {df_costs.columns.tolist()}")