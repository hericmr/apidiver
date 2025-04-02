import unittest
from datetime import datetime
from src.mergulho_emailer.models.moon_phase import MoonPhase

class TestMoonPhase(unittest.TestCase):
    def setUp(self):
        self.phase_data = {
            'phase': 'Lua Nova',
            'year': 2024,
            'month': 4,
            'day': 2
        }
        self.moon_phase = MoonPhase(self.phase_data)

    def test_get_phase_value(self):
        """Testa o cálculo do valor numérico da fase lunar"""
        self.assertEqual(self.moon_phase.get_phase_value(), 0)

    def test_get_formatted_date(self):
        """Testa a formatação da data da fase lunar"""
        formatted = self.moon_phase.get_formatted_date()
        self.assertEqual(formatted['nome'], 'Lua Nova')
        self.assertEqual(formatted['dia'], '02')
        self.assertEqual(formatted['mes'], 'ABR')

    def test_get_description(self):
        """Testa a geração da descrição da fase lunar"""
        nome, descricao = self.moon_phase.get_description()
        self.assertEqual(nome, 'Lua Nova')
        self.assertIsInstance(descricao, str)
        self.assertTrue(len(descricao) > 0)

if __name__ == '__main__':
    unittest.main() 