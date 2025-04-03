from datetime import datetime
from ..config.settings import Settings

class MoonPhase:
    def __init__(self, phase_data):
        self.phase_data = phase_data
        self.phase = phase_data.get('phase')
        self.year = phase_data.get('year')
        self.month = phase_data.get('month')
        self.day = phase_data.get('day')

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
        """Retorna o valor numérico da fase da lua."""
        return self.phase_map.get(self.phase, 0)

    def get_phase_timeline(self):
        """Retorna uma representação visual da fase da lua em uma linha do tempo."""
        # Emojis para as diferentes fases da lua
        phases = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
        current_phase = self.get_phase_value()
        
        # Criar a linha do tempo com 8 posições
        timeline = ["○"] * 8
        timeline[current_phase] = "●"
        
        # Adicionar emojis correspondentes
        timeline_with_emoji = []
        for i, (dot, emoji) in enumerate(zip(timeline, phases)):
            if i == current_phase:
                timeline_with_emoji.append(f"{emoji}●")
            else:
                timeline_with_emoji.append(f"{emoji}○")
        
        return " ".join(timeline_with_emoji)

    def get_description(self):
        """Retorna descrição detalhada da fase da lua e seu impacto no mergulho livre."""
        phase_value = self.get_phase_value()
        phase_timeline = self.get_phase_timeline()
        
        if phase_value == 0:
            return f"Lua Nova\n{phase_timeline}\n\nCondições desfavoráveis para mergulho livre. A lua nova resulta em noites muito escuras, reduzindo significativamente a visibilidade subaquática. Recomenda-se evitar mergulhos noturnos durante este período.\n\nReferência: Estudos indicam que a visibilidade subaquática durante a lua nova pode ser até 70% menor que durante a lua cheia."
        elif phase_value == 1:
            return f"Lua Crescente (Início)\n{phase_timeline}\n\nCondições moderadas. A lua crescente começa a iluminar o céu noturno, melhorando gradualmente a visibilidade subaquática. Ainda é necessário cautela em mergulhos noturnos.\n\nReferência: A visibilidade subaquática aumenta gradualmente com a lua crescente, mas ainda está abaixo do ideal."
        elif phase_value == 2:
            return f"Quarto Crescente\n{phase_timeline}\n\nCondições favoráveis. A lua ilumina metade do céu noturno, proporcionando boa visibilidade subaquática. Período adequado para mergulhos noturnos.\n\nReferência: A visibilidade subaquática durante o quarto crescente é aproximadamente 50% melhor que durante a lua nova."
        elif phase_value == 3:
            return f"Lua Crescente (Final)\n{phase_timeline}\n\nCondições muito favoráveis. A lua quase cheia oferece excelente visibilidade subaquática. Período ideal para mergulhos noturnos.\n\nReferência: A visibilidade subaquática durante este período é cerca de 75% melhor que durante a lua nova."
        elif phase_value == 4:
            return f"Lua Cheia\n{phase_timeline}\n\nCondições ideais para mergulho livre. A lua cheia proporciona a melhor visibilidade subaquática noturna. Período excelente para mergulhos noturnos.\n\nReferência: A visibilidade subaquática durante a lua cheia pode ser até 90% melhor que durante a lua nova."
        elif phase_value == 5:
            return f"Lua Minguante (Início)\n{phase_timeline}\n\nCondições muito favoráveis. A lua ainda quase cheia mantém excelente visibilidade subaquática. Período ideal para mergulhos noturnos.\n\nReferência: A visibilidade subaquática permanece alta, similar ao período da lua cheia."
        elif phase_value == 6:
            return f"Quarto Minguante\n{phase_timeline}\n\nCondições favoráveis. A lua ilumina metade do céu noturno, mantendo boa visibilidade subaquática. Período adequado para mergulhos noturnos.\n\nReferência: A visibilidade subaquática durante o quarto minguante é aproximadamente 50% melhor que durante a lua nova."
        else:
            return f"Lua Minguante (Final)\n{phase_timeline}\n\nCondições moderadas. A lua minguante reduz gradualmente a visibilidade subaquática. Cautela recomendada em mergulhos noturnos.\n\nReferência: A visibilidade subaquática começa a diminuir significativamente com a lua minguante." 