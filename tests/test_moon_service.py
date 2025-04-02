import unittest
from unittest.mock import patch, Mock
from datetime import datetime
from src.mergulho_emailer.services.moon_service import MoonService
from src.mergulho_emailer.models.moon_phase import MoonPhase

class TestMoonService(unittest.TestCase):
    def setUp(self):
        self.moon_service = MoonService()
        self.test_date = datetime(2024, 4, 2)

    @patch('requests.get')
    def test_get_moon_phase_usno_success(self, mock_get):
        """Testa a obtenção de fases lunares via USNO com sucesso"""
        # Configurar mock
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            'phasedata': [
                {'phase': 'New Moon', 'year': 2024, 'month': 4, 'day': 2},
                {'phase': 'First Quarter', 'year': 2024, 'month': 4, 'day': 9},
                {'phase': 'Full Moon', 'year': 2024, 'month': 4, 'day': 16},
                {'phase': 'Last Quarter', 'year': 2024, 'month': 4, 'day': 23}
            ]
        }
        mock_get.return_value = mock_response

        # Executar teste
        fase_atual, fase_proxima, proximas_fases = self.moon_service.get_moon_phase(self.test_date)
        
        self.assertIsInstance(fase_atual, MoonPhase)
        self.assertEqual(fase_atual.phase, 'Lua Nova')
        self.assertEqual(len(proximas_fases), 3)

    @patch('requests.get')
    def test_get_moon_phase_usno_failure_openweather_success(self, mock_get):
        """Testa o fallback para OpenWeather quando USNO falha"""
        def mock_get_side_effect(url, *args, **kwargs):
            if 'usno.navy.mil' in url:
                raise Exception("USNO API Error")
            
            mock_response = Mock()
            mock_response.ok = True
            mock_response.json.return_value = {
                'daily': [{'moon_phase': 0.1}]  # Lua Nova
            }
            return mock_response

        mock_get.side_effect = mock_get_side_effect

        # Executar teste
        fase_atual, fase_proxima, proximas_fases = self.moon_service.get_moon_phase(self.test_date)
        
        self.assertIsInstance(fase_atual, MoonPhase)
        self.assertEqual(fase_atual.phase, 'Lua Nova')
        self.assertEqual(len(proximas_fases), 0)

    @patch('requests.get')
    def test_get_moon_phase_all_failures(self, mock_get):
        """Testa o caso em que todas as APIs falham"""
        mock_get.side_effect = Exception("API Error")

        # Executar teste
        fase_atual, fase_proxima, proximas_fases = self.moon_service.get_moon_phase(self.test_date)
        
        self.assertIsNone(fase_atual)
        self.assertIsNone(fase_proxima)
        self.assertEqual(len(proximas_fases), 0)

    @patch('requests.get')
    def test_get_moon_phase_empty_response(self, mock_get):
        """Testa o caso de resposta vazia da API"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        # Executar teste
        fase_atual, fase_proxima, proximas_fases = self.moon_service.get_moon_phase(self.test_date)
        
        self.assertIsNone(fase_atual)
        self.assertIsNone(fase_proxima)
        self.assertEqual(len(proximas_fases), 0)

if __name__ == '__main__':
    unittest.main() 