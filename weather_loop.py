import csv, time, requests
from datetime import datetime

LAT, LON = 3.139, 101.6869
TIMEZONE = "Asia/Kuala_Lumpur"

API_FORECAST = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}&hourly=temperature_2m,wind_speed_10m&timezone={TIMEZONE}"
)
API_CURRENT = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}&current=temperature_2m,wind_speed_10m&timezone={TIMEZONE}"
)

def collect_once():
    current = requests.get(API_CURRENT).json()["current"]
    forecast = requests.get(API_FORECAST).json()["hourly"]

    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    iso_hour = now.isoformat(timespec="hours")

    try:
        idx = forecast["time"].index(iso_hour)
    except ValueError:
        idx = min(range(len(forecast["time"])), key=lambda i: abs(datetime.fromisoformat(forecast["time"][i]) - now))

    forecast_temp = forecast["temperature_2m"][idx]
    forecast_wind = forecast["wind_speed_10m"][idx]
    actual_temp = current["temperature_2m"]
    actual_wind = current["wind_speed_10m"]

    row = [now.strftime("%Y-%m-%d %H:%M:%S"), forecast_temp, actual_temp, forecast_wind, actual_wind]

    with open("weather_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)

    print("Collected at:", row[0])

# Loop forever (1 reading every 1 hour)
print("📡 Starting data collection (press Ctrl+C to stop)...")
try:
    while True:
        collect_once()
        time.sleep(3600)  # 3600 seconds = 1 hour
except KeyboardInterrupt:
    print("\n Stopped by user")