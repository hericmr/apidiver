
from flask import Flask, render_template
from mergulho_check_github import (
    get_fase_lua, get_vento, get_precipitacao, get_mare,
    get_fase_lua_descricao, get_vento_descricao,
    get_precipitacao_descricao, get_mare_descricao,
    get_estacao, CONFIG
)
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    data_hora = datetime.now()
    
    # Coletar dados
    fase_lunar = get_fase_lua(CONFIG["LATITUDE"], CONFIG["LONGITUDE"], data_hora)
    vento = get_vento(CONFIG["LATITUDE"], CONFIG["LONGITUDE"])
    precipitacao = get_precipitacao(CONFIG["LATITUDE"], CONFIG["LONGITUDE"])
    mare = get_mare(CONFIG["LATITUDE"], CONFIG["LONGITUDE"], data_hora)
    
    # Processar descrições
    nome_fase, desc_fase = get_fase_lua_descricao(fase_lunar)
    desc_vento, imp_vento = get_vento_descricao(vento)
    desc_precip, imp_precip = get_precipitacao_descricao(precipitacao)
    desc_mare, imp_mare = get_mare_descricao(mare)
    
    # Preparar dados para template
    conditions = [
        {
            "icon": "🌙",
            "title": "Fase da Lua",
            "description": desc_fase,
            "status": nome_fase,
            "alert_type": "info"
        },
        {
            "icon": "💨",
            "title": "Vento",
            "description": imp_vento,
            "status": f"{desc_vento} ({vento:.1f} km/h)",
            "alert_type": "primary"
        },
        {
            "icon": "🌧️",
            "title": "Precipitação",
            "description": imp_precip,
            "status": f"{desc_precip} ({precipitacao:.1f} mm)",
            "alert_type": "secondary"
        },
        {
            "icon": "🌊",
            "title": "Maré",
            "description": imp_mare,
            "status": f"{desc_mare} ({mare:.1f} m)",
            "alert_type": "info"
        },
        {
            "icon": "🌞",
            "title": "Estação",
            "description": "Condições da estação atual",
            "status": get_estacao(),
            "alert_type": "warning"
        }
    ]
    
    # Calcular avaliação
    condicoes_ideais = (vento < 15 and precipitacao < 5 and mare < 1.5)
    if condicoes_ideais:
        evaluation = {
            "status": "🌟 ÓTIMO",
            "score": 90,
            "description": "Condições ideais para mergulho hoje!"
        }
    elif vento < 20 and precipitacao < 10 and mare < 1.8:
        evaluation = {
            "status": "👍 BOM",
            "score": 70,
            "description": "Boas condições para mergulho hoje."
        }
    elif vento < 25 and precipitacao < 15 and mare < 2.0:
        evaluation = {
            "status": "⚠️ REGULAR",
            "score": 50,
            "description": "Condições aceitáveis para mergulho hoje."
        }
    else:
        evaluation = {
            "status": "❌ NÃO RECOMENDADO",
            "score": 27,
            "description": "Condições não recomendadas para mergulho hoje."
        }
    
    return render_template('index.html', 
                         conditions=conditions,
                         evaluation=evaluation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
