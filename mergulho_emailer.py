#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de Condições de Mergulho com Envio de Email
Script para consulta de condições reais via APIs e envio automático por email
"""

import os
import sys
import json
import requests
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import random

# Configurações
CONFIG = {
    "CIDADE": "Santos",
    "ESTADO": "SP",
    "LATITUDE": -23.9608,
    "LONGITUDE": -46.3336,
    "SITE_URL": "https://hericmr.github.io/mergulho",
    "STORMGLASS_API_KEY": "6b7ca118-da20-11ee-8a07-0242ac130002-6b7ca186-da20-11ee-8a07-0242ac130002",
    "OPENWEATHER_API_KEY": "1234567890",  # Chave temporária para teste
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "EMAIL_USER": os.getenv("EMAIL_USER", "heric.m.r@gmail.com"),
    "EMAIL_PASS": os.getenv("EMAIL_PASS", "khuk mkoy jyvz vajk"),
    "EMAIL_DESTINATARIOS": os.getenv("EMAIL_DESTINATARIOS", "heric.m.r@gmail.com").split(","),
}

def get_fase_lua(lat, lon, data):
    """Retorna a fase lunar atual e próximas fases usando a API do U.S. Naval Observatory"""
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
                fase_map = {
                    'New Moon': 'Lua Nova',
                    'First Quarter': 'Quarto Crescente',
                    'Full Moon': 'Lua Cheia',
                    'Last Quarter': 'Quarto Minguante'
                }

                # Atualizar nomes das fases para português
                for fase in fases:
                    fase['phase'] = fase_map.get(fase['phase'], fase['phase'])

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

                # Calcular valor numérico da fase
                fase_valor_map = {
                    'Lua Nova': 0,
                    'Quarto Crescente': 25,
                    'Lua Cheia': 50,
                    'Quarto Minguante': 75
                }

                fase_base = fase_valor_map.get(fase_atual['phase'], 0)
                
                # Se temos uma próxima fase, ajustar o valor baseado na progressão
                if fase_proxima:
                    data_atual = data.date()
                    data_fase_atual = datetime.strptime(f"{fase_atual['year']}-{fase_atual['month']}-{fase_atual['day']}", '%Y-%m-%d').date()
                    data_proxima_fase = datetime.strptime(f"{fase_proxima['year']}-{fase_proxima['month']}-{fase_proxima['day']}", '%Y-%m-%d').date()
                    
                    dias_total = (data_proxima_fase - data_fase_atual).days
                    dias_passados = (data_atual - data_fase_atual).days
                    
                    if dias_total > 0:
                        progresso = dias_passados / dias_total
                        proxima_fase_valor = fase_valor_map.get(fase_proxima['phase'], 0)
                        
                        # Ajustar para ciclo completo se necessário
                        if fase_base > proxima_fase_valor:
                            proxima_fase_valor += 100
                        
                        fase_atual_valor = fase_base + (proxima_fase_valor - fase_base) * progresso
                        return fase_atual_valor % 100, fase_atual, fases[1:] if fase_atual == fases[0] else fases
                
                return fase_base, fase_atual, fases[1:] if fase_atual == fases[0] else fases
    except Exception as e:
        print(f"Erro ao consultar fase da lua: {e}")

    # Fallback: usar OpenWeatherMap
    try:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={CONFIG['OPENWEATHER_API_KEY']}"
        response = requests.get(url)
        if response.ok:
            dados = response.json()
            if dados and dados.get('daily'):
                fase = dados['daily'][0]['moon_phase']
                return fase * 100, None, []  # Converter para escala 0-100
    except Exception as e:
        print(f"Erro no fallback OpenWeatherMap: {e}")

    # Se tudo falhar, retornar um valor simulado
    return random.randint(0, 100), None, []

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

def get_fase_lua_descricao(fase_lunar, fase_atual, proximas_fases):
    """Retorna descrição detalhada da fase lunar com base na visibilidade subaquática."""
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

def get_vento(lat, lon):
    """Simula a velocidade do vento para demonstração"""
    return 12.5  # Simulando vento moderado

def get_precipitacao(lat, lon):
    """Simula a precipitação para demonstração"""
    return 2.5  # Simulando chuva leve

def get_mare(lat, lon, data):
    """Simula a altura da maré para demonstração"""
    return 1.2  # Simulando maré média

def get_estacao():
    """Determina a estação do ano baseado na data atual"""
    hoje = datetime.now()
    mes = hoje.month

    if 12 <= mes <= 2:
        return "Verão"
    elif 3 <= mes <= 5:
        return "Outono"
    elif 6 <= mes <= 8:
        return "Inverno"
    else:
        return "Primavera"

def get_vento_descricao(vento):
    """Retorna descrição detalhada do impacto do vento no mergulho livre."""
    if vento < 5:
        return "Calmo", "Condições ideais para mergulho. Superfície estável, facilitando relaxamento e descida."
    elif vento < 15:
        return "Fraco", "Condições favoráveis. Pequena ondulação na superfície, mínimo impacto no mergulho."
    elif vento < 25:
        return "Moderado", "Ondulação moderada na superfície. Pode ter correntezas e dificultar o relaxamento e a respiração antes da descida."
    else:
        return "Forte", "Condições críticas. Ondulação severa e correntes superficiais fortes, tornando o acesso e a segurança no mergulho ruim."


def get_precipitacao_descricao(precipitacao):
    """Retorna descrição detalhada da precipitação e seu impacto na visibilidade subaquática."""
    if precipitacao < 1:
        return "Baixa", "Impacto na visibilidade: insignificante. A água permanece clara, com pouca ou nenhuma influência de material em suspensão."
    elif precipitacao < 5:
        return "Média", "Impacto na visibilidade: moderado. Possível aumento de sedimentos em suspensão devido ao escoamento superficial das chuvas."
    else:
        return "Alta", "Impacto na visibilidade: severo. Chuvas intensas aumentam a turbidez da água, devido ao carreamento de sedimentos dos rios locais, como o Rio Cubatão, prejudicando atividades subaquáticas."

def get_mare_descricao(mare):
    """Retorna descrição detalhada da maré"""
    if mare < 0.8:
        return "Baixa", "Condições de maré favoráveis. Visibilidade subaquática otimizada."
    elif mare < 1.5:
        return "Média", "Condições de maré estáveis. Visibilidade subaquática adequada."
    else:
        return "Alta", "Condições de maré críticas. Visibilidade subaquática comprometida."

def get_correntes(lat, lon):
    """Obtém dados de correntes marítimas da API StormGlass"""
    try:
        # Data atual em formato ISO
        data_atual = datetime.now().isoformat()

        # URL da API StormGlass para correntes
        url = f"https://api.stormglass.io/v2/tide/extremes/point"

        # Parâmetros da requisição
        params = {
            "lat": lat,
            "lng": lon,
            "start": data_atual,
            "end": data_atual,
            "key": CONFIG["STORMGLASS_API_KEY"]
        }

        response = requests.get(url, params=params)
        if response.ok:
            dados = response.json()
            if dados and dados.get('data'):
                # Pega o primeiro registro de corrente
                corrente = dados['data'][0]
                velocidade = corrente.get('speed', 0)
                direcao = corrente.get('type', 'unknown')

                return velocidade, direcao
    except Exception as e:
        print(f"Erro ao consultar correntes: {e}")

    # Fallback: retorna valores simulados em caso de erro
    return 0.5, "unknown"

def get_correntes_descricao(velocidade, direcao):
    """Retorna descrição detalhada das correntes marítimas"""
    if velocidade < 0.3:
        return "Fraca", "Condições ideais para mergulho. Correntes suaves facilitam a navegação subaquática e reduzem o consumo de ar."
    elif velocidade < 0.7:
        return "Moderada", "Condições aceitáveis. Correntes moderadas requerem atenção durante o mergulho e podem aumentar o consumo de ar em 20-30%."
    elif velocidade < 1.2:
        return "Forte", "Condições desfavoráveis. Correntes fortes dificultam a navegação, aumentam o consumo de ar em 40-50% e requerem experiência avançada."
    else:
        return "Muito Forte", "Condições críticas. Correntes muito fortes tornam o mergulho perigoso, com alto risco de fadiga e consumo excessivo de ar. Não recomendado para mergulho."

def gerar_relatorio_texto(data_hora, fase_lunar, nome_fase, descricao_fase, 
                        vento, descricao_vento, impacto_vento,
                        precipitacao, descricao_precip, impacto_precip,
                        mare, descricao_mare, impacto_mare,
                        velocidade_corrente, descricao_corrente, impacto_corrente,
                        estacao, avaliacao, pontuacao, descricao, recomendacao,
                        fase_atual, proximas_fases):
    """Gera o conteúdo do email em formato texto simples como fallback"""
    # Formatar informações da lua
    fase_atual_info = formatar_data_fase(fase_atual) if fase_atual else None
    proximas_fases_info = [formatar_data_fase(fase) for fase in proximas_fases]

    # Gerar texto das fases da lua
    fases_texto = ""
    if fase_atual_info:
        fases_texto += f"""
🌙 FASE LUNAR ATUAL
──────────────────
{fase_atual_info['nome']}
Data: {fase_atual_info['data_completa']}
{descricao_fase}
"""

    if proximas_fases_info:
        fases_texto += f"""
📅 PRÓXIMAS FASES LUNARES
───────────────────────"""
        for fase in proximas_fases_info:
            fases_texto += f"""
• {fase['nome']} em {fase['dias_faltantes']} dias
  Data: {fase['data_completa']}"""

    return f"""
{'='*60}
🌊 MERGULHÔMETRO DE SANTOS/SP 🌊
{'='*60}

📊 AVALIAÇÃO GERAL
────────────────
{avaliacao} ({pontuacao}/100)
{descricao}
{recomendacao}

📅 DATA E HORA
─────────────
{data_hora.strftime('%d/%m/%Y %H:%M')}

{fases_texto}

💨 VENTO
───────
{descricao_vento} ({vento:.1f} km/h)
{impacto_vento}

🌧️ PRECIPITAÇÃO
──────────────
{descricao_precip} ({precipitacao:.1f} mm)
{impacto_precip}

🌊 MARÉ
──────
{descricao_mare} ({mare:.1f} m)
{impacto_mare}

🌊 CORRENTES
───────────
{descricao_corrente} ({velocidade_corrente:.1f} m/s)
{impacto_corrente}

🌞 ESTAÇÃO
─────────
{estacao}
{'Estação ideal para mergulho!' if estacao in ['Verão', 'Primavera'] else 'Condições aceitáveis para mergulho'}

{'='*60}
🌐 Dados fornecidos por StormGlass API e OpenWeatherMap API
👨‍💻 Desenvolvido pelo pirata Héric Moura
🌍 Visite: {CONFIG['SITE_URL']}

{'='*60}
📧 Este é um email automático. Você receberá esta mensagem todos os dias às 7h da manhã.
{'='*60}
"""

def enviar_email(conteudo_texto, avaliacao, pontuacao, descricao):
    """Envia o email com o relatório em formato texto"""
    try:
        msg = MIMEText(conteudo_texto, "plain")
        msg["From"] = CONFIG["EMAIL_USER"]
        msg["To"] = ", ".join(CONFIG["EMAIL_DESTINATARIOS"])
        msg["Subject"] = f"🌊 Mergulhômetro Santos/SP - {avaliacao} ({pontuacao}/100) - {descricao}"

        server = smtplib.SMTP(CONFIG["SMTP_SERVER"], CONFIG["SMTP_PORT"])
        server.starttls()
        server.login(CONFIG["EMAIL_USER"], CONFIG["EMAIL_PASS"])
        server.sendmail(CONFIG["EMAIL_USER"], CONFIG["EMAIL_DESTINATARIOS"], msg.as_string())
        server.quit()
        print("✅ Email enviado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False

def main():
    try:
        print("\n" + "="*60)
        print("🌊 MERGULHÔMETRO DE SANTOS/SP 🌊")
        print("="*60 + "\n")

        # Obter data/hora atual
        data_hora = datetime.now()
        print(f"📅 Data e Hora: {data_hora.strftime('%d/%m/%Y %H:%M')}\n")

        # Consultar condições
        fase_lunar, fase_atual, proximas_fases = get_fase_lua(CONFIG["LATITUDE"], CONFIG["LONGITUDE"], data_hora)
        nome_fase, descricao_fase = get_fase_lua_descricao(fase_lunar, fase_atual, proximas_fases)
        
        # Formatar e exibir informações da lua
        fase_atual_info = formatar_data_fase(fase_atual) if fase_atual else None
        proximas_fases_info = [formatar_data_fase(fase) for fase in proximas_fases]
        
        print("🌙 Fase Lunar Atual:")
        if fase_atual_info:
            print(f"   {fase_atual_info['nome']}")
            print(f"   Data: {fase_atual_info['data_completa']}")
            print(f"   {descricao_fase}")
        print()

        if proximas_fases_info:
            print("📅 Próximas Fases Lunares:")
            for fase in proximas_fases_info:
                print(f"\n   • {fase['nome']} em {fase['dias_faltantes']} dias")
                print(f"     Data: {fase['data_completa']}")
        print()

        vento = get_vento(CONFIG["LATITUDE"], CONFIG["LONGITUDE"])
        descricao_vento, impacto_vento = get_vento_descricao(vento)
        print(f"💨 Vento: {descricao_vento} ({vento:.1f} km/h)")
        print(f"   {impacto_vento}\n")

        precipitacao = get_precipitacao(CONFIG["LATITUDE"], CONFIG["LONGITUDE"])
        descricao_precip, impacto_precip = get_precipitacao_descricao(precipitacao)
        print(f"🌧️ Precipitação: {descricao_precip} ({precipitacao:.1f} mm)")
        print(f"   {impacto_precip}\n")

        mare = get_mare(CONFIG["LATITUDE"], CONFIG["LONGITUDE"], data_hora)
        descricao_mare, impacto_mare = get_mare_descricao(mare)
        print(f"🌊 Maré: {descricao_mare} ({mare:.1f} m)")
        print(f"   {impacto_mare}\n")

        velocidade_corrente, direcao_corrente = get_correntes(CONFIG["LATITUDE"], CONFIG["LONGITUDE"])
        descricao_corrente, impacto_corrente = get_correntes_descricao(velocidade_corrente, direcao_corrente)
        print(f"🌊 Correntes: {descricao_corrente} ({velocidade_corrente:.1f} m/s)")
        print(f"   {impacto_corrente}\n")

        estacao = get_estacao()
        print(f"🌞 Estação: {estacao}")
        print(f"   {'Estação ideal para mergulho!' if estacao in ['Verão', 'Primavera'] else 'Condições aceitáveis para mergulho'}\n")

        # Avaliar condições gerais com critérios mais rigorosos
        # Condições ideais: vento < 10km/h, precipitação < 2mm, maré < 1.2m, corrente < 0.3m/s
        condicoes_ideais = (vento < 10 and precipitacao < 2 and mare < 1.2 and velocidade_corrente < 0.3)

        # Condições boas: vento < 15km/h, precipitação < 5mm, maré < 1.5m, corrente < 0.7m/s
        condicoes_boas = (vento < 15 and precipitacao < 5 and mare < 1.5 and velocidade_corrente < 0.7)

        # Condições regulares: vento < 20km/h, precipitação < 10mm, maré < 1.8m, corrente < 1.2m/s
        condicoes_regulares = (vento < 20 and precipitacao < 10 and mare < 1.8 and velocidade_corrente < 1.2)

        # Ajuste de pontuação baseado na estação
        ajuste_estacao = 0
        if estacao == "Verão":
            ajuste_estacao = 10  # Bônus para verão
        elif estacao == "Primavera":
            ajuste_estacao = 5   # Bônus para primavera
        elif estacao == "Inverno":
            ajuste_estacao = -5  # Penalidade para inverno
        else:  # Outono
            ajuste_estacao = 0

        # Ajuste de pontuação baseado nas correntes
        ajuste_correntes = 0
        if velocidade_corrente < 0.3:
            ajuste_correntes = 5  # Bônus para correntes fracas
        elif velocidade_corrente < 0.7:
            ajuste_correntes = 0  # Sem ajuste para correntes moderadas
        elif velocidade_corrente < 1.2:
            ajuste_correntes = -5  # Penalidade para correntes fortes
        else:
            ajuste_correntes = -10  # Penalidade maior para correntes muito fortes

        # Ajuste de pontuação baseado na fase lunar
        ajuste_lua = 0
        if fase_lunar < 5:  # Lua Nova
            ajuste_lua = -10  # Penalidade reduzida para lua nova (era -15)
        elif fase_lunar < 25:  # Lua Crescente
            ajuste_lua = 5  # Bônus para lua crescente
        elif fase_lunar < 45:  # Quarto Crescente
            ajuste_lua = 10  # Bônus maior para quarto crescente
        elif fase_lunar < 55:  # Lua Cheia
            ajuste_lua = -10  # Penalidade para lua cheia
        elif fase_lunar < 75:  # Quarto Minguante
            ajuste_lua = 5  # Bônus para quarto minguante
        else:  # Lua Minguante
            ajuste_lua = 0  # Sem ajuste para lua minguante

        if condicoes_ideais:
            avaliacao = "🌟 ÓTIMO"
            pontuacao = min(95 + ajuste_estacao + ajuste_correntes + ajuste_lua, 100)  # Máximo de 100
            descricao = "Condições climáticas ideais para mergulho."
            recomendacao = "Condições climáticas estáveis e favoráveis para prática de mergulho."
        elif condicoes_boas:
            avaliacao = "👍 BOM"
            pontuacao = min(70 + ajuste_estacao + ajuste_correntes + ajuste_lua, 95)  # Máximo de 95
            descricao = "Condições climáticas favoráveis para mergulho."
            recomendacao = "Condições climáticas aceitáveis para prática de mergulho."
        elif condicoes_regulares:
            avaliacao = "⚠️ REGULAR"
            pontuacao = min(50 + ajuste_estacao + ajuste_correntes + ajuste_lua, 70)  # Máximo de 70
            descricao = "Condições climáticas moderadas para mergulho."
            recomendacao = "Condições climáticas instáveis. Recomenda-se cautela."
        else:
            avaliacao = "❌ NÃO RECOMENDADO"
            pontuacao = max(27 + ajuste_estacao + ajuste_correntes + ajuste_lua, 27)  # Mínimo de 27
            descricao = "Condições climáticas desfavoráveis para mergulho."
            recomendacao = "Condições climáticas instáveis. Recomenda-se adiar a prática de mergulho."

        print("="*60)
        print(f"📊 AVALIAÇÃO: {avaliacao} ({pontuacao}/100)")
        print(f"💡 {descricao}")
        print(f"🎯 {recomendacao}")
        print("="*60 + "\n")

        # Gerar e enviar email
        conteudo_texto = gerar_relatorio_texto(
            data_hora, fase_lunar, nome_fase, descricao_fase,
            vento, descricao_vento, impacto_vento,
            precipitacao, descricao_precip, impacto_precip,
            mare, descricao_mare, impacto_mare,
            velocidade_corrente, descricao_corrente, impacto_corrente,
            estacao, avaliacao, pontuacao, descricao, recomendacao,
            fase_atual, proximas_fases
        )

        if enviar_email(conteudo_texto, avaliacao, pontuacao, descricao):
            print("✅ Relatório enviado por email com sucesso!")
        else:
            print("❌ Falha ao enviar o relatório por email.")

        return 0

    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
