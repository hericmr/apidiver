import unittest
from unittest.mock import Mock, patch
from src.mergulho_emailer.app import MergulhoEmailer
from src.mergulho_emailer.models.weather import Weather
from src.mergulho_emailer.models.moon_phase import MoonPhase

class TestMergulhoEmailer(unittest.TestCase):
    def setUp(self):
        self.app = MergulhoEmailer()
        self.weather = Weather(wind_speed=10.0, precipitation=2.5, tide_height=1.2)
        self.moon_phase = MoonPhase({
            'phase': 'Lua Nova',
            'year': 2024,
            'month': 4,
            'day': 2
        })

    def test_evaluate_conditions(self):
        """Testa a avaliação das condições de mergulho"""
        # Teste com condições ideais
        evaluation, score, description, recommendation = self.app.evaluate_conditions(
            self.weather, self.moon_phase, (1.0, 'Norte')
        )
        self.assertIsInstance(score, int)
        self.assertIsInstance(evaluation, str)
        self.assertIsInstance(description, str)
        self.assertIsInstance(recommendation, str)

        # Teste com condições ruins
        bad_weather = Weather(wind_speed=25.0, precipitation=15.0, tide_height=0.3)
        evaluation, score, description, recommendation = self.app.evaluate_conditions(
            bad_weather, self.moon_phase, (3.0, 'Sul')
        )
        self.assertLess(score, 60)

    @patch('src.mergulho_emailer.services.moon_service.MoonService')
    @patch('src.mergulho_emailer.services.weather_service.WeatherService')
    @patch('src.mergulho_emailer.services.email_service.EmailService')
    def test_run(self, mock_email_service, mock_weather_service, mock_moon_service):
        """Testa a execução do processo principal"""
        # Configurar mocks
        mock_moon_service.return_value.get_moon_phase.return_value = (
            self.moon_phase, None, []
        )
        mock_weather_service.return_value.get_weather_data.return_value = self.weather
        mock_weather_service.return_value.get_currents.return_value = (1.0, 'Norte')
        mock_email_service.return_value.send_report.return_value = True

        # Executar o processo
        success = self.app.run()
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main() 