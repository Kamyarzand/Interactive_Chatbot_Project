import os
import json
import requests
import logging
from datetime import datetime

class TemperatureMonitor:
    def __init__(self):
        self.api_key = "3c1a03f854eacdd71e366db34a06ccbe"
        self.data_file = "/home/dtuser/chatbot/tasks/temp_readings.json"
        self.readings = self.load_data()
        logging.basicConfig(
            filename='/home/dtuser/chatbot/tasks/monitor.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def get_cpu_temp(self):
        try:
            temp = os.popen("vcgencmd measure_temp").readline()
            return float(temp.replace("temp=", "").replace("'C\n", ""))
        except Exception as e:
            logging.error(f"Error getting CPU temp: {e}")
            return None

    def get_weather_data(self, city):
        try:
            # Get current weather
            current_response = requests.get(
                "http://api.openweathermap.org/data/2.5/weather",
                params={'q': city, 'appid': self.api_key, 'units': 'metric'}
            )
            
            # Get forecast
            forecast_response = requests.get(
                "http://api.openweathermap.org/data/2.5/forecast",
                params={'q': city, 'appid': self.api_key, 'units': 'metric'}
            )
            
            if current_response.status_code == 200 and forecast_response.status_code == 200:
                current_temp = current_response.json()['main']['temp']
                forecast_temp = forecast_response.json()['list'][0]['main']['temp']
                return current_temp, forecast_temp
            return None, None
        except Exception as e:
            logging.error(f"Error getting weather data: {e}")
            return None, None

    def record_reading(self, city):
        try:
            cpu_temp = self.get_cpu_temp()
            current_temp, forecast_temp = self.get_weather_data(city)
            
            if cpu_temp is None or current_temp is None:
                return False

            reading = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'cpu_temp': cpu_temp,
                'current_temp': current_temp,
                'forecast_temp': forecast_temp,
                'temp_difference': round(current_temp - forecast_temp, 2)
            }
            
            self.readings.append(reading)
            self.save_data()
            
            # Log detailed information
            logging.info(f"Weather forecast for {city}: {forecast_temp}C")
            logging.info(f"Current temperature in {city}: {current_temp}C")
            logging.info(f"Temperature difference from forecast: {reading['temp_difference']}C")
            logging.info(f"Current CPU Temperature: {cpu_temp}C")
            
            # Calculate and log CPU temperature change
            daily_cpu_change = self.get_cpu_temp_change()
            if daily_cpu_change is not None:
                logging.info(f"CPU temperature change today: {daily_cpu_change}C")
            
            return True
        except Exception as e:
            logging.error(f"Error recording reading: {e}")
            return False

    def get_cpu_temp_change(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            today_readings = [r for r in self.readings if r['timestamp'].startswith(today)]
            
            if len(today_readings) > 1:
                cpu_temps = [r['cpu_temp'] for r in today_readings]
                return round(max(cpu_temps) - min(cpu_temps), 2)
            return None
        except Exception as e:
            logging.error(f"Error calculating CPU temp change: {e}")
            return None

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            return []

    def save_data(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.readings, f)
        except Exception as e:
            logging.error(f"Error saving data: {e}")