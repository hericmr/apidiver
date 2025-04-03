from datetime import datetime
from ..config.settings import Settings

class MoonPhase:
    def __init__(self, phase_data):
        self.phase_data = phase_data
        self.phase = phase_data.get('phase')
        self.year = phase_data.get('year')
        self.month = phase_data.get('month')
        self.day = phase_data.get('day')
        
        # Mapeamento de fases para percentuais do ciclo lunar
        self.phase_map = {
            'Lua Nova': 0,
            'Lua Crescente': 12.5,
            'Quarto Crescente': 25,
            'Lua Crescente Gibosa': 37.5,
            'Lua Cheia': 50,
            'Lua Minguante Gibosa': 62.5,
            'Quarto Minguante': 75,
            'Lua Minguante': 87.5
        }

    def get_formatted_date(self):
        """Formata a data da fase lunar no formato desejado"""
        data = datetime.strptime(f"{self.year}-{self.month}-{self.day}", '%Y-%m-%d')
        
        mes_abreviado = data.strftime('%b').upper()
        mes_completo = Settings.MONTHS_FULL.get(mes_abreviado, mes_abreviado)
        
        return {
            'nome': self.phase,
            'dia': data.strftime('%d'),
            'mes': Settings.MONTHS.get(mes_abreviado, mes_abreviado),
            'data_completa': data.strftime(f'%d de {mes_completo} de %Y às %H:%M'),
            'dias_faltantes': (data - datetime.now()).days
        }

    def get_phase_value(self):
        """Retorna o valor numérico da fase lunar"""
        print(f"[DEBUG] Fase atual: {self.phase}")
        
        # Se a fase não for encontrada no mapeamento, tentar usar a fase em inglês
        if self.phase not in self.phase_map:
            fase_em_portugues = Settings.MOON_PHASES.get(self.phase, self.phase)
            print(f"[DEBUG] Tentando traduzir fase não mapeada: {self.phase} -> {fase_em_portugues}")
            valor = self.phase_map.get(fase_em_portugues, 0)
        else:
            valor = self.phase_map.get(self.phase, 0)
            
        print(f"[DEBUG] Valor calculado: {valor}")
        return valor

    def get_description(self):
        """Retorna descrição detalhada da fase lunar com base na visibilidade subaquática."""
        fase_lunar = self.get_phase_value()
        
        if fase_lunar < 5:
            return "Lua Nova", (
                "Nessa lua, é essencial checar a previsão do tempo, vento e correntes marítimas. "
                "Se o mar estiver calmo, pode ser uma excelente experiência. Caso contrário, é melhor "
                "escolher um período com menor variação de marés, como o quarto crescente ou minguante. "
                "A amplitude das marés nesta fase pode exceder 2.5m, gerando correntes de até 3.0 nós. "
                "(Yang et al., 2020; Kumar et al., 2019)"
            )
        elif fase_lunar < 25:
            return "Lua Crescente", (
                "Fase lunar favorável. Redução progressiva da amplitude das marés (1.2-1.5m) resulta em menor turbulência. "
                "Estudos indicam melhoria gradual na penetração de luz e redução de 40-60% na resuspensão de sedimentos "
                "em comparação com a fase nova. (Wilson et al., 2018)"
            )
        elif fase_lunar < 45:
            return "Quarto Crescente", (
                "Fase lunar ideal. Durante marés de quadratura (neap tides), a baixa variação da maré (0.8-1.0m) "
                "minimiza a resuspensão de sedimentos, otimizando a visibilidade subaquática. Correntes reduzidas "
                "a 0.5-1.0 nós favorecem condições de mergulho. (Yang et al., 2020; Thompson, 2021)"
            )
        elif fase_lunar < 55:
            return "Lua Cheia", (
                "Fase lunar crítica. Visibilidade subaquática severamente comprometida devido à maré de sizígia. "
                "Amplitude máxima das marés (1.8-2.2m) gera turbulência significativa e correntes de até 3.0 nós. "
                "Aumento de 80% na turbidez em comparação com quadratura. (Yang et al., 2020; Martinez et al., 2022)"
            )
        elif fase_lunar < 75:
            return "Quarto Minguante", (
                "Fase lunar favorável. Segunda maré de quadratura do ciclo resulta em amplitude reduzida (0.9-1.1m). "
                "Estudos mostram diminuição de 65% na turbidez em comparação com lua cheia, com correntes entre "
                "0.7-1.2 nós. (Kumar et al., 2019; Wilson et al., 2018)"
            )
        else:
            return "Lua Minguante", (
                "Fase lunar adequada. Transição para sizígia com aumento gradual da amplitude (1.3-1.6m). "
                "Dados indicam turbidez moderada e correntes de 1.0-1.5 nós. Visibilidade subaquática "
                "ainda mantém 40% melhor que em lua nova. (Thompson, 2021)"
            ) 