from datetime import datetime
from dataclasses import dataclass

@dataclass
class DadosMergulho:
    """
    Classe que representa os dados de mergulho coletados.
    
    Attributes:
        data (datetime): Data e hora da coleta dos dados
        fase_lunar (float): Porcentagem do ciclo lunar (0-100)
        mare (float): Altura da maré em metros
        vento (float): Velocidade do vento em km/h
        temperatura_agua (float): Temperatura da água em °C
        temperatura_ar (float): Temperatura do ar em °C
        visibilidade (float): Visibilidade em metros
        corrente (float): Velocidade da corrente em nós
    """
    data: datetime
    fase_lunar: float
    mare: float
    vento: float
    temperatura_agua: float
    temperatura_ar: float
    visibilidade: float
    corrente: float 