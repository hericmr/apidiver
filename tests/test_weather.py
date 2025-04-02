import unittest
from datetime import datetime
from freezegun import freeze_time
from src.mergulho_emailer.models.weather import Weather

class TestWeather(unittest.TestCase):
    def setUp(self):
        self.weather = Weather(wind_speed=10.0, precipitation=2.5, tide_height=1.2)

    def test_get_wind_description(self):
        """Testa a geração da descrição do vento para diferentes velocidades"""
        test_cases = [
            (3.0, "Vento Calmo"),
            (8.0, "Vento Leve"),
            (12.0, "Vento Moderado"),
            (18.0, "Vento Forte"),
            (25.0, "Vento Muito Forte")
        ]

        for wind_speed, expected_name in test_cases:
            weather = Weather(wind_speed=wind_speed, precipitation=0, tide_height=0)
            nome, descricao = weather.get_wind_description()
            self.assertEqual(nome, expected_name)
            self.assertIsInstance(descricao, str)
            self.assertTrue(len(descricao) > 0)

    def test_get_precipitation_description(self):
        """Testa a geração da descrição da precipitação para diferentes valores"""
        test_cases = [
            (0.5, "Sem Chuva"),
            (2.5, "Chuva Leve"),
            (7.5, "Chuva Moderada"),
            (15.0, "Chuva Forte")
        ]

        for precip, expected_name in test_cases:
            weather = Weather(wind_speed=0, precipitation=precip, tide_height=0)
            nome, descricao = weather.get_precipitation_description()
            self.assertEqual(nome, expected_name)
            self.assertIsInstance(descricao, str)
            self.assertTrue(len(descricao) > 0)

    def test_get_tide_description(self):
        """Testa a geração da descrição da maré para diferentes alturas"""
        test_cases = [
            (0.3, "Maré Baixa"),
            (0.8, "Maré Média-Baixa"),
            (1.2, "Maré Média"),
            (1.8, "Maré Média-Alta"),
            (2.5, "Maré Alta")
        ]

        for height, expected_name in test_cases:
            weather = Weather(wind_speed=0, precipitation=0, tide_height=height)
            nome, descricao = weather.get_tide_description()
            self.assertEqual(nome, expected_name)
            self.assertIsInstance(descricao, str)
            self.assertTrue(len(descricao) > 0)

    @freeze_time("2024-01-15")  # Verão
    def test_get_season_summer(self):
        """Testa a determinação da estação no verão"""
        self.assertEqual(self.weather.get_season(), "Verão")

    @freeze_time("2024-04-15")  # Outono
    def test_get_season_autumn(self):
        """Testa a determinação da estação no outono"""
        self.assertEqual(self.weather.get_season(), "Outono")

    @freeze_time("2024-07-15")  # Inverno
    def test_get_season_winter(self):
        """Testa a determinação da estação no inverno"""
        self.assertEqual(self.weather.get_season(), "Inverno")

    @freeze_time("2024-10-15")  # Primavera
    def test_get_season_spring(self):
        """Testa a determinação da estação na primavera"""
        self.assertEqual(self.weather.get_season(), "Primavera")

if __name__ == '__main__':
    unittest.main() 