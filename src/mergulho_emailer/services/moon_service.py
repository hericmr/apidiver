import requests
from datetime import datetime
from ..config.settings import Settings
from ..models.moon_phase import MoonPhase

def formatar_data_fase(fase):
    """Formata a data da fase lunar no formato desejado"""
    data = datetime.strptime(f"{fase['year']}-{fase['month']}-{fase['day']}", '%Y-%m-%d')
    
    # Mapeamento de meses para português
    meses = {
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
    
    # Mapeamento de meses para nomes completos em português
    meses_completos = {
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
    
    mes_abreviado = data.strftime('%b').upper()
    mes_completo = meses_completos.get(mes_abreviado, mes_abreviado)
    
    return {
        'nome': fase['phase'],
        'dia': data.strftime('%d'),
        'mes': meses.get(mes_abreviado, mes_abreviado),
        'data_completa': data.strftime(f'%d de {mes_completo} de %Y às %H:%M'),
        'dias_faltantes': (data - datetime.now()).days
    }

class MoonService:
    def __init__(self):
        self.lat = Settings.LATITUDE
        self.lon = Settings.LONGITUDE

    def get_moon_phase(self, data=None):
        """Retorna a fase lunar atual e próximas fases usando a API do U.S. Naval Observatory"""
        if data is None:
            data = datetime.now()

        try:
            # Data atual em formato YYYY-MM-DD para a API USNO
            data_formatada = data.strftime('%Y-%m-%d')

            # Usar a API do U.S. Naval Observatory (USNO)
            url = f"https://aa.usno.navy.mil/api/moon/phases/date?date={data_formatada}&nump=4"

            response = requests.get(url)
            if response.ok:
                dados = response.json()

                if dados and dados.get('phasedata'):
                    # Ordenar fases por data
                    fases = sorted(dados['phasedata'], 
                                 key=lambda x: datetime.strptime(f"{x['year']}-{x['month']}-{x['day']}", '%Y-%m-%d'))

                    # Traduzir nomes das fases para português
                    for fase in fases:
                        fase['phase'] = Settings.MOON_PHASES.get(fase['phase'], fase['phase'])

                    # Encontrar a fase atual e a próxima
                    fase_atual = None
                    fase_proxima = None
                    data_atual = data.date()

                    for i in range(len(fases)):
                        data_fase = datetime.strptime(f"{fases[i]['year']}-{fases[i]['month']}-{fases[i]['day']}", '%Y-%m-%d').date()
                        if i > 0:
                            data_fase_anterior = datetime.strptime(f"{fases[i-1]['year']}-{fases[i-1]['month']}-{fases[i-1]['day']}", '%Y-%m-%d').date()
                            if data_fase_anterior <= data_atual < data_fase:
                                fase_atual = fases[i-1]
                                fase_proxima = fases[i]
                                break
                        if i == len(fases) - 1 and not fase_atual:
                            # Se estamos após a última fase listada
                            fase_atual = fases[-1]
                            fase_proxima = None

                    if not fase_atual:
                        # Se estamos antes da primeira fase listada
                        fase_atual = fases[0]
                        fase_proxima = fases[1] if len(fases) > 1 else None

                    # Criar objetos MoonPhase
                    fase_atual_obj = MoonPhase(fase_atual) if fase_atual else None
                    fase_proxima_obj = MoonPhase(fase_proxima) if fase_proxima else None
                    proximas_fases = [MoonPhase(fase) for fase in fases[1:]] if fase_atual == fases[0] else [MoonPhase(fase) for fase in fases]

                    return fase_atual_obj, fase_proxima_obj, proximas_fases

        except Exception as e:
            print(f"Erro ao consultar fase da lua: {e}")

        # Fallback: usar OpenWeatherMap
        try:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self.lat}&lon={self.lon}&exclude=minutely,hourly,alerts&appid={Settings.OPENWEATHER_API_KEY}"
            response = requests.get(url)
            if response.ok:
                dados = response.json()
                if dados and dados.get('daily'):
                    fase = dados['daily'][0]['moon_phase']
                    # Criar um objeto MoonPhase simulado
                    fase_simulada = {
                        'phase': 'Lua Nova' if fase < 0.25 else 'Quarto Crescente' if fase < 0.5 else 'Lua Cheia' if fase < 0.75 else 'Quarto Minguante',
                        'year': data.year,
                        'month': data.month,
                        'day': data.day
                    }
                    return MoonPhase(fase_simulada), None, []
        except Exception as e:
            print(f"Erro no fallback OpenWeatherMap: {e}")

        return None, None, [] 