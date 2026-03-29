from data.eirgrid_data.eirgrid import get_demand
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)

start = yesterday.strftime('%Y-%m-%d')
end = today.strftime('%Y-%m-%d')

df = get_demand(start, end)

print("=== Actual Data ===")
actual = df[df['area'] == 'actual']
print(f"Rows: {len(actual)}")
if len(actual):
    print(f"Time range: {actual['timestamp'].min()} to {actual['timestamp'].max()}")
    print(f"Value range: {actual['value'].min()} to {actual['value'].max()}")
    print(actual.tail())

print("\n=== Forecast Data ===")
forecast = df[df['area'] == 'forecast']
print(f"Rows: {len(forecast)}")
if len(forecast):
    print(f"Time range: {forecast['timestamp'].min()} to {forecast['timestamp'].max()}")
    print(f"Value range: {forecast['value'].min()} to {forecast['value'].max()}")
    print(forecast.tail())