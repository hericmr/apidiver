import os

class Settings:
    # Location settings
    CIDADE = "Santos"
    ESTADO = "SP"
    LATITUDE = -23.9608
    LONGITUDE = -46.3336
    SITE_URL = "https://hericmr.github.io/mergulho"

    # API Keys
    STORMGLASS_API_KEY = "6b7ca118-da20-11ee-8a07-0242ac130002-6b7ca186-da20-11ee-8a07-0242ac130002"
    OPENWEATHER_API_KEY = "1234567890"  # Temporary key for testing

    # Email settings
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_USER = os.getenv("EMAIL_USER", "heric.m.r@gmail.com")
    EMAIL_PASS = os.getenv("EMAIL_PASS", "khuk mkoy jyvz vajk")
    EMAIL_DESTINATARIOS = os.getenv("EMAIL_DESTINATARIOS", "heric.m.r@gmail.com").split(",")

    # Moon phase mapping
    MOON_PHASES = {
        'New Moon': 'Lua Nova',
        'First Quarter': 'Quarto Crescente',
        'Full Moon': 'Lua Cheia',
        'Last Quarter': 'Quarto Minguante'
    }

    # Month mapping
    MONTHS = {
        'JAN': 'JAN',
        'FEB': 'FEV',
        'MAR': 'MAR',
        'APR': 'ABR',
        'MAY': 'MAI',
        'JUN': 'JUN',
        'JUL': 'JUL',
        'AUG': 'AGO',
        'SEP': 'SET',
        'OCT': 'OUT',
        'NOV': 'NOV',
        'DEC': 'DEZ'
    }

    MONTHS_FULL = {
        'JAN': 'janeiro',
        'FEB': 'fevereiro',
        'MAR': 'março',
        'APR': 'abril',
        'MAY': 'maio',
        'JUN': 'junho',
        'JUL': 'julho',
        'AUG': 'agosto',
        'SEP': 'setembro',
        'OCT': 'outubro',
        'NOV': 'novembro',
        'DEC': 'dezembro'
    } 