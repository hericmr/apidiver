import requests
from datetime import datetime, timedelta
from ..config.settings import Settings
from ..models.weather import Weather

class WeatherService:
    def __init__(self):
        self.lat = Settings.LATITUDE
        self.lon = Settings.LONGITUDE
        self.api_key = Settings.STORMGLASS_API_KEY

    def get_weather_data(self):
        """Obtém dados meteorológicos da API Stormglass"""
        try:
            # Endpoint da API Stormglass
            url = f"https://api.stormglass.io/v2/weather/point"
            
            # Parâmetros da requisição
            params = {
                'lat': self.lat,
                'lng': self.lon,
                'params': ','.join(['windSpeed', 'precipitation', 'waterTemperature']),
                'start': datetime.now().isoformat(),
                'end': (datetime.now() + timedelta(days=1)).isoformat(),
                'key': self.api_key
            }

            response = requests.get(url, params=params)
            if response.ok:
                data = response.json()
                
                # Extrair dados relevantes
                wind_speed = data.get('hours', [{}])[0].get('windSpeed', {}).get('noaa', 0)
                precipitation = data.get('hours', [{}])[0].get('precipitation', {}).get('noaa', 0)
                tide_height = data.get('hours', [{}])[0].get('waterTemperature', {}).get('noaa', 0)

                return Weather(wind_speed, precipitation, tide_height)

        except Exception as e:
            print(f"Erro ao obter dados meteorológicos: {e}")

        # Fallback: retornar dados simulados
        return Weather(12.5, 2.5, 1.2)  # Valores simulados para demonstração

    def get_currents(self):
        """Obtém dados de correntes marítimas"""
        try:
            url = f"https://api.stormglass.io/v2/tide/extremes/point"
            
            params = {
                'lat': self.lat,
                'lng': self.lon,
                'start': datetime.now().isoformat(),
                'end': (datetime.now() + timedelta(days=1)).isoformat(),
                'key': self.api_key
            }

            response = requests.get(url, params=params)
            if response.ok:
                data = response.json()
                
                # Calcular velocidade e direção das correntes baseado nas marés
                if data.get('data'):
                    current_data = data['data'][0]
                    height = current_data.get('height', 0)
                    type = current_data.get('type', 'high')
                    
                    # Simular velocidade baseada no tipo de maré
                    velocity = 2.0 if type == 'high' else 1.0
                    direction = 'Norte' if type == 'high' else 'Sul'
                    
                    return velocity, direction

        except Exception as e:
            print(f"Erro ao obter dados de correntes: {e}")

        # Fallback: retornar dados simulados
        return 1.5, 'Norte'  # Valores simulados para demonstração 