import csv

# Lists to store data
forecast_temp = []
actual_temp = []
forecast_wind = []
actual_wind = []

# Read your original file (or weather_data_fixed.csv if you used that)
with open("weather_data.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        forecast_temp.append(float(row[1]))
        actual_temp.append(float(row[2]))
        forecast_wind.append(float(row[3]))
        actual_wind.append(float(row[4]))

# Function to calculate Mean Square Error
def mse(forecast, actual):
    return sum((f - a) ** 2 for f, a in zip(forecast, actual)) / len(forecast)

# Calculate and print the results
print(" Temperature MSE:", round(mse(forecast_temp, actual_temp), 3))
print(" Wind Speed MSE:", round(mse(forecast_wind, actual_wind), 3))