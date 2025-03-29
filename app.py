
from mergulho_check_github import (
    get_fase_lua, get_vento, get_precipitacao, get_mare,
    get_fase_lua_descricao, get_vento_descricao,
    get_precipitacao_descricao, get_mare_descricao,
    get_estacao, CONFIG
)
from datetime import datetime

def generate_html():
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
    
    # Preparar dados
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
            "description": "Condições climáticas favoráveis para mergulho. Você pode mergulhar com relativa tranquilidade."
        }
    elif vento < 25 and precipitacao < 15 and mare < 2.0:
        evaluation = {
            "status": "⚠️ REGULAR",
            "score": 50,
            "description": "Condições climáticas moderadas para mergulho. Mergulhe com cautela e atenção às mudanças nas condições."
        }
    else:
        evaluation = {
            "status": "❌ NÃO RECOMENDADO",
            "score": 27,
            "description": "Condições climáticas desfavoráveis para mergulho. Não recomendado para mergulho hoje. Considere adiar."
        }

    # Gerar HTML
    conditions_html = ""
    for condition in conditions:
        conditions_html += f"""
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <div class="condition-icon">{condition['icon']}</div>
                    <h5 class="card-title">{condition['title']}</h5>
                    <p class="card-text">{condition['description']}</p>
                    <div class="alert alert-{condition['alert_type']}">
                        {condition['status']}
                    </div>
                </div>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Condições de Mergulho</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1>Condições de Mergulho - {CONFIG['CIDADE']}</h1>
            <p>Data e Hora: {data_hora.strftime('%d/%m/%Y %H:%M')}</p>
            <div class="row">
                {conditions_html}
            </div>
            <div class="card mt-4">
                <div class="card-body text-center">
                    <h3>Avaliação Geral</h3>
                    <div class="display-4">{evaluation['status']}</div>
                    <p class="lead">{evaluation['description']}</p>
                    <div class="progress">
                        <div class="progress-bar" role="progressbar" style="width: {evaluation['score']}%">
                            {evaluation['score']}/100
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    html_content = generate_html()
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("HTML gerado com sucesso!")
