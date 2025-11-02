import requests

class WeatherService:
    def __init__(self):
        self.api_key = "3c1a03f854eacdd71e366db34a06ccbe"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def get_location_weather(self, city):
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                return self._format_weather_data(city, data)
            elif response.status_code == 404:
                return f"City '{city}' not found."
            else:
                return f"Error getting weather data: {data.get('message', 'Unknown error')}"
                
        except requests.RequestException as e:
            return f"Network error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _format_weather_data(self, city, data):
        return (
            f"\nCurrent weather in {city.title()}:"
            f"\n🌡️ Temperature: {data['main']['temp']}°C"
            f"\n💧 Humidity: {data['main']['humidity']}%"
            f"\n🌪️ Wind Speed: {data['wind']['speed']} m/s"
            f"\n☁️ Conditions: {data['weather'][0]['description']}"
            f"\n🌅 Feels like: {data['main']['feels_like']}°C"
        )

    def extract_city(self, text):
        text = text.lower()
        # Support multiple formats
        if text.startswith("weather in"):
            return text[11:].strip()
        elif text.startswith("weather"):
            return text[7:].strip()
        elif "weather" in text:
            parts = text.split("weather")
            if len(parts) > 1:
                return parts[1].strip()
        return None