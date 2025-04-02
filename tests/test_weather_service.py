import unittest
from unittest.mock import patch, Mock
from src.mergulho_emailer.services.weather_service import WeatherService
from src.mergulho_emailer.models.weather import Weather

class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.weather_service = WeatherService()

    @patch('requests.get')
    def test_get_weather_data_success(self, mock_get):
        """Testa a obtenção de dados meteorológicos com sucesso"""
        # Configurar mock
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            'hours': [{
                'windSpeed': {'noaa': 10.0},
                'precipitation': {'noaa': 2.5},
                'waterTemperature': {'noaa': 1.2}
            }]
        }
        mock_get.return_value = mock_response

        # Executar teste
        weather = self.weather_service.get_weather_data()
        self.assertIsInstance(weather, Weather)
        self.assertEqual(weather.wind_speed, 10.0)
        self.assertEqual(weather.precipitation, 2.5)
        self.assertEqual(weather.tide_height, 1.2)

    @patch('requests.get')
    def test_get_weather_data_failure(self, mock_get):
        """Testa o fallback quando a API falha"""
        # Configurar mock para falhar
        mock_get.side_effect = Exception("API Error")

        # Executar teste
        weather = self.weather_service.get_weather_data()
        self.assertIsInstance(weather, Weather)
        self.assertEqual(weather.wind_speed, 12.5)  # Valor simulado
        self.assertEqual(weather.precipitation, 2.5)  # Valor simulado
        self.assertEqual(weather.tide_height, 1.2)  # Valor simulado

    @patch('requests.get')
    def test_get_currents_success(self, mock_get):
        """Testa a obtenção de dados de correntes com sucesso"""
        # Configurar mock
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            'data': [{
                'height': 2.0,
                'type': 'high'
            }]
        }
        mock_get.return_value = mock_response

        # Executar teste
        velocity, direction = self.weather_service.get_currents()
        self.assertEqual(velocity, 2.0)
        self.assertEqual(direction, 'Norte')

    @patch('requests.get')
    def test_get_currents_failure(self, mock_get):
        """Testa o fallback quando a API de correntes falha"""
        # Configurar mock para falhar
        mock_get.side_effect = Exception("API Error")

        # Executar teste
        velocity, direction = self.weather_service.get_currents()
        self.assertEqual(velocity, 1.5)  # Valor simulado
        self.assertEqual(direction, 'Norte')  # Valor simulado

if __name__ == '__main__':
    unittest.main() 