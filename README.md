# iot-weather-tracking-app
Python IoT project for monitoring real-time weather conditions and evaluating forecast accuracy using data from the Open-Meteo API.

iot-weather-tracking-app/
│
├── weather_loop.py         # Collects real-time and forecast data continuously
├── calculate_mse.py        # Calculates Mean Square Error
├── visualize_weather.py    # Generates graphs and Tkinter dashboard
├── weather_data.csv        # Example dataset (3 days of data)
├── README.md               # Documentation
└── requirements.txt        # Libraries needed

requirements.txt
pandas
matplotlib
requests

# IoT Weather Tracking App

A Python-based IoT project that monitors real-time weather conditions and evaluates forecast accuracy using the [Open-Meteo API](https://open-meteo.com/).

## Features
- Collects forecasted and real-time weather data (temperature, wind speed)
- Stores 72 hours of data in a CSV file
- Calculates Mean Square Error (MSE) for accuracy evaluation
- Visualizes results in a Tkinter dashboard with Matplotlib charts
- Cost-effective (all tools and APIs are free)

## Tech Stack
- Language: Python
- Libraries: pandas, matplotlib, requests, tkinter
- Data Source: Open-Meteo API

## How It Works
1. `weather_loop.py` runs for 72 hours, collecting actual and forecast data every hour.
2. Data is stored in `weather_data.csv`.
3. `calculate_mse.py` computes MSE values for temperature and wind speed.
4. `visualize_weather.py` plots graphs and displays them in a Tkinter dashboard.

## Results
- Temperature MSE: **0.288** (high accuracy)
- Wind Speed MSE: **0.739** (moderate variance)

## Example Output
Line graphs showing forecast vs actual temperature and wind speed over 3 days.

## How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run data collection (72 hours)
python weather_loop.py

# Calculate MSE
python calculate_mse.py

# Visualize results
python visualize_weather.py
