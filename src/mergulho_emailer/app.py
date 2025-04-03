from datetime import datetime
from .services.moon_service import MoonService
from .services.weather_service import WeatherService
from .services.email_service import EmailService
from .config.settings import Settings

class MergulhoEmailer:
    def __init__(self):
        self.moon_service = MoonService()
        self.weather_service = WeatherService()
        self.email_service = EmailService()

    def evaluate_conditions(self, weather, moon_phase, currents):
        """Avalia as condições gerais para mergulho"""
        # Inicializar pontuação
        score = 100

        # Avaliar vento - critérios mais rigorosos
        if weather.wind_speed > 15:
            score -= 40
        elif weather.wind_speed > 12:
            score -= 30
        elif weather.wind_speed > 8:
            score -= 20

        # Avaliar precipitação - critérios mais rigorosos
        if weather.precipitation > 5:
            score -= 35
        elif weather.precipitation > 2:
            score -= 25
        elif weather.precipitation > 0.5:
            score -= 15

        # Avaliar maré - critérios mais rigorosos
        if weather.tide_height < 0.7:
            score -= 30
        elif weather.tide_height < 1.2:
            score -= 20

        # Avaliar correntes - critérios mais rigorosos
        if currents[0] > 1.5:
            score -= 35
        elif currents[0] > 1.2:
            score -= 25
        elif currents[0] > 0.8:
            score -= 15

        # Avaliar fase lunar - critérios mais rigorosos
        if moon_phase and moon_phase.get_phase_value() > 40 and moon_phase.get_phase_value() < 60:
            score -= 25  # Lua cheia - período mais amplo

        # Determinar avaliação - critérios mais rigorosos
        if score >= 85:
            evaluation = "EXCELENTE"
            description = "Condições ideais para mergulho livre."
            recommendation = "Aproveite as condições favoráveis para praticar mergulho livre."
        elif score >= 70:
            evaluation = "BOA"
            description = "Condições favoráveis para mergulho livre."
            recommendation = "Pode praticar mergulho livre, mas fique atento às condições."
        elif score >= 50:
            evaluation = "RUIM"
            description = "Condições ruins para mergulho livre."
            recommendation = "Considere adiar o mergulho se possível."
        else:
            evaluation = "DESFAVORÁVEL"
            description = "Condições desfavoráveis para mergulho livre."
            recommendation = "Não recomendado praticar mergulho livre neste momento."

        return evaluation, score, description, recommendation

    def run(self):
        """Executa o processo principal"""
        try:
            # Obter data e hora atual
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

            # Obter dados da lua
            fase_atual, fase_proxima, proximas_fases = self.moon_service.get_moon_phase()
            if fase_atual:
                nome_fase, descricao_fase = fase_atual.get_description()
            else:
                nome_fase = "Desconhecida"
                descricao_fase = "Não foi possível determinar a fase lunar"

            # Obter dados meteorológicos
            weather = self.weather_service.get_weather_data()
            descricao_vento, impacto_vento = weather.get_wind_description()
            descricao_precip, impacto_precip = weather.get_precipitation_description()
            descricao_mare, impacto_mare = weather.get_tide_description()
            estacao = weather.get_season()

            # Obter dados de correntes
            velocidade_corrente, direcao_corrente = self.weather_service.get_currents()
            descricao_corrente = f"Correntes {direcao_corrente}"
            impacto_corrente = "Impacto significativo" if velocidade_corrente > 1.5 else "Impacto moderado"

            # Avaliar condições
            avaliacao, pontuacao, descricao, recomendacao = self.evaluate_conditions(
                weather, fase_atual, (velocidade_corrente, direcao_corrente)
            )

            # Gerar e enviar relatório
            report_html = self.email_service.generate_html_report(
                data_hora, fase_atual.get_phase_value() if fase_atual else 0,
                nome_fase, descricao_fase,
                weather.wind_speed, descricao_vento, impacto_vento,
                weather.precipitation, descricao_precip, impacto_precip,
                weather.tide_height, descricao_mare, impacto_mare,
                velocidade_corrente, descricao_corrente, impacto_corrente,
                estacao, avaliacao, pontuacao, descricao, recomendacao,
                fase_atual, proximas_fases,
                getattr(weather, 'temperatura_agua', 22.0), getattr(weather, 'temperatura_ar', 25.0)
            )

            # Enviar email
            if self.email_service.send_report(report_html, avaliacao, pontuacao, descricao):
                print("Processo concluído com sucesso!")
            else:
                print("Erro ao enviar email.")
            return True

        except Exception as e:
            print(f"Erro ao executar o processo: {e}")
            return False 