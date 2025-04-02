class Weather:
    def __init__(self, wind_speed, precipitation, tide_height):
        self.wind_speed = wind_speed
        self.precipitation = precipitation
        self.tide_height = tide_height

    def get_wind_description(self):
        """Retorna descrição detalhada do impacto do vento no mergulho livre."""
        if self.wind_speed < 5:
            return "Vento Calmo", "Condições ideais para mergulho livre. Vento abaixo de 5 nós não afeta significativamente a superfície."
        elif self.wind_speed < 10:
            return "Vento Leve", "Condições favoráveis. Pequenas ondulações podem ser observadas, mas não comprometem a prática."
        elif self.wind_speed < 15:
            return "Vento Moderado", "Condições aceitáveis. Ondas moderadas podem dificultar a entrada e saída da água."
        elif self.wind_speed < 20:
            return "Vento Forte", "Condições desfavoráveis. Ondas significativas podem comprometer a segurança."
        else:
            return "Vento Muito Forte", "Condições perigosas. Não recomendado para mergulho livre."

    def get_precipitation_description(self):
        """Retorna descrição detalhada do impacto da precipitação no mergulho livre."""
        if self.precipitation < 1:
            return "Sem Chuva", "Condições ideais para mergulho livre."
        elif self.precipitation < 5:
            return "Chuva Leve", "Condições aceitáveis. A chuva leve pode reduzir a visibilidade superficial."
        elif self.precipitation < 10:
            return "Chuva Moderada", "Condições desfavoráveis. A chuva moderada pode reduzir significativamente a visibilidade."
        else:
            return "Chuva Forte", "Condições perigosas. Não recomendado para mergulho livre."

    def get_tide_description(self):
        """Retorna descrição detalhada do impacto da maré no mergulho livre."""
        if self.tide_height < 0.5:
            return "Maré Baixa", "Condições desfavoráveis. Risco de encalhe e visibilidade reduzida."
        elif self.tide_height < 1.0:
            return "Maré Média-Baixa", "Condições aceitáveis. Visibilidade pode estar comprometida."
        elif self.tide_height < 1.5:
            return "Maré Média", "Condições favoráveis. Visibilidade adequada."
        elif self.tide_height < 2.0:
            return "Maré Média-Alta", "Condições ideais. Boa visibilidade e profundidade adequada."
        else:
            return "Maré Alta", "Condições favoráveis. Boa visibilidade, mas correntes podem estar mais fortes."

    def get_season(self):
        """Determina a estação do ano baseado na data atual."""
        from datetime import datetime
        mes = datetime.now().month

        # Hemisfério Sul
        if mes in [12, 1, 2]:
            return "Verão"
        elif mes in [3, 4, 5]:
            return "Outono"
        elif mes in [6, 7, 8]:
            return "Inverno"
        else:  # mes in [9, 10, 11]
            return "Primavera" 