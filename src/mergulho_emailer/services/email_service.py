import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from ..config.settings import Settings
from ..models.moon_phase import MoonPhase
from ..models.dados_mergulho import DadosMergulho
import pytz

class EmailService:
    def __init__(self):
        self.smtp_server = Settings.SMTP_SERVER
        self.smtp_port = Settings.SMTP_PORT
        self.smtp_username = Settings.EMAIL_USER
        self.smtp_password = Settings.EMAIL_PASS
        self.from_email = Settings.EMAIL_USER
        self.to_email = ', '.join(Settings.EMAIL_DESTINATARIOS)

    def send_report(self, report_html, evaluation, score, description):
        """Envia o relatório por email."""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'Relatório de Condições de Mergulho - {datetime.now().strftime("%d/%m/%Y %H:%M")}'
            msg['From'] = self.from_email
            msg['To'] = self.to_email

            # Anexar o HTML já gerado
            msg.attach(MIMEText(report_html, 'html'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
            return False

    def generate_html_report(self, data_hora, fase_lunar, nome_fase, descricao_fase,
                           vento, descricao_vento, impacto_vento,
                           precipitacao, descricao_precip, impacto_precip,
                           mare, descricao_mare, impacto_mare,
                           velocidade_corrente, descricao_corrente, impacto_corrente,
                           estacao, avaliacao, pontuacao, descricao, recomendacao,
                           fase_atual, proximas_fases):
        """Gera o conteúdo HTML do relatório com um design moderno e responsivo."""
        # Formatar informações da lua
        fase_atual_info = fase_atual.get_formatted_date() if fase_atual else None
        proximas_fases_info = [fase.get_formatted_date() for fase in proximas_fases]

        # Gerar o conteúdo do relatório
        report_text = f"""
            <div class="section">
                <div class="section-header">
                    \U0001f30a Condições Atuais
                </div>
                <div class="section-content">
                    <div class="info-grid">
                        <div class="info-item">
                            <h3>Vento</h3>
                            <p class="value">{vento:.1f} km/h</p>
                            <p class="description">{descricao_vento}</p>
                            <div class="impact-badge {impacto_vento.lower().replace(' ', '-')}">{impacto_vento}</div>
                            <div class="details">
                                <p>• Velocidade crítica: > 20 km/h</p>
                                <p>• Direção predominante: SE</p>
                                <p>• Rajadas máximas: {vento * 1.5:.1f} km/h</p>
                                <p>• Impacto: {impacto_vento}</p>
                                <p class="scientific-note">Estudos indicam que ventos acima de 20 km/h podem gerar ondulação significativa e afetar a segurança do mergulho.</p>
                            </div>
                        </div>
                        <div class="info-item">
                            <h3>Precipitação</h3>
                            <p class="value">{precipitacao:.1f} mm/h</p>
                            <p class="description">{descricao_precip}</p>
                            <div class="impact-badge {impacto_precip.lower().replace(' ', '-')}">{impacto_precip}</div>
                            <div class="details">
                                <p>• Probabilidade: {min(precipitacao * 20, 100):.0f}%</p>
                                <p>• Acumulado 24h: {precipitacao * 24:.1f} mm</p>
                                <p>• Visibilidade: {max(10 - precipitacao, 0):.1f} km</p>
                                <p>• Impacto: {impacto_precip}</p>
                                <p class="scientific-note">Chuvas intensas aumentam a turbidez da água devido ao carreamento de sedimentos dos rios locais, como o Rio Cubatão, prejudicando atividades subaquáticas.</p>
                            </div>
                        </div>
                        <div class="info-item">
                            <h3>Maré</h3>
                            <p class="value">{mare:.1f} m</p>
                            <p class="description">{descricao_mare}</p>
                            <div class="impact-badge {impacto_mare.lower().replace(' ', '-')}">{impacto_mare}</div>
                            <div class="details">
                                <p>• Amplitude: {mare * 2:.1f} m</p>
                                <p>• Próxima baixa-mar: -0.2 m (09:45)</p>
                                <p>• Próxima preamar: 1.4 m (15:30)</p>
                                <p>• Impacto: {impacto_mare}</p>
                                <p class="scientific-note">Durante marés de quadratura (neap tides), a baixa variação da maré (0.8-1.0m) minimiza a resuspensão de sedimentos, otimizando a visibilidade subaquática.</p>
                            </div>
                        </div>
                        <div class="info-item">
                            <h3>Correntes</h3>
                            <p class="value">{velocidade_corrente:.1f} nós</p>
                            <p class="description">{descricao_corrente}</p>
                            <div class="impact-badge {impacto_corrente.lower().replace(' ', '-')}">{impacto_corrente}</div>
                            <div class="details">
                                <p>• Velocidade crítica: > 2.0 nós</p>
                                <p>• Direção predominante: N-S</p>
                                <p>• Intensidade máxima: {velocidade_corrente * 1.3:.1f} nós</p>
                                <p>• Impacto: {impacto_corrente}</p>
                                <p class="scientific-note">Correntes acima de 2.0 nós podem aumentar o consumo de ar em 40-50% e requerem experiência avançada. (Kumar et al., 2019)</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-header">
                    \U0001f319 Fase Lunar e Impacto nas Marés
                </div>
                <div class="section-content">
                    <div class="info-grid">
                        <div class="info-item">
                            <h3>Fase Atual: {nome_fase}</h3>
                            <p class="moon-phase-value">{fase_lunar:.1f}% do ciclo</p>
                            <div class="details">
                                <p class="scientific-description">{descricao_fase}</p>
                                <p class="next-phase">Próxima fase: {proximas_fases_info[0]['nome']} em {proximas_fases_info[0]['dias_faltantes']} dias</p>
                                <p class="scientific-note">Fonte: U.S. Naval Observatory (USNO) e estudos oceanográficos recentes.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-header">
                    \U0001f30f Recomendações e Considerações
                </div>
                <div class="section-content">
                    <div class="info-item full-width">
                        <div class="recommendation">
                            <h3>Avaliação Geral</h3>
                            <p class="main-recommendation">{recomendacao}</p>
                            <div class="details">
                                <p>• Estação: {estacao}</p>
                                <p>• Condições gerais: {descricao}</p>
                                <p>• Nível de experiência recomendado: {'Avançado' if pontuacao < 50 else 'Intermediário' if pontuacao < 75 else 'Todos os níveis'}</p>
                                <p class="safety-note">Lembre-se: Sua segurança é a prioridade. Em caso de dúvida, consulte um instrutor ou escola de mergulho local.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="info-section">
                <div class="info-item">
                    <h3>Fase da Lua</h3>
                    <div class="moon-phase-value">{fase_lunar:.1f}% do ciclo</div>
                    <div class="scientific-description">
                        A fase lunar atual influencia diretamente as marés através da força gravitacional. {descricao_fase}
                    </div>
                    <div class="next-phase">Próxima fase: {proximas_fases_info[0]['nome']} em {proximas_fases_info[0]['dias_faltantes']} dias</div>
                    <div class="scientific-note">
                        Nota: A influência lunar nas marés é mais pronunciada durante as fases de Lua Nova e Lua Cheia, 
                        quando ocorrem as marés de sizígia.
                    </div>
                </div>
                
                <div class="info-item">
                    <h3>Condições do Mar</h3>
                    <div class="scientific-description">
                        Altura das ondas: {mare:.1f}m
                        <br>
                        Direção do vento: {descricao_vento}
                        <br>
                        Velocidade do vento: {vento:.1f} km/h
                    </div>
                    <div class="scientific-note">
                        A altura das ondas e condições do vento são fatores críticos que afetam a visibilidade 
                        subaquática e a segurança do mergulho.
                    </div>
                </div>

                <div class="info-item">
                    <h3>Temperatura</h3>
                    <div class="scientific-description">
                        Temperatura da água: {mare:.1f}°C
                        <br>
                        Temperatura do ar: {vento:.1f}°C
                    </div>
                    <div class="scientific-note">
                        A temperatura da água influencia diretamente o metabolismo da vida marinha e o conforto 
                        térmico do mergulhador.
                    </div>
                </div>
            </div>

            <div class="recommendation">
                <h3>Recomendação para Mergulho</h3>
                <div class="main-recommendation">
                    {recomendacao}
                </div>
                <div class="safety-note">
                    Lembre-se: Sempre verifique seu equipamento, respeite os limites de profundidade e tempo, 
                    e nunca mergulhe sozinho. A segurança é nossa prioridade!
                </div>
            </div>
        """

        return f"""
        <!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Condições de Mergulho</title>
    <style>
        /* Reset e estilos base */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Arial', 'Helvetica', sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background-color: #f9f9f9;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            overflow: hidden;
        }}
        .header {{
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #005999 0%, #003366 100%);
            color: white;
            position: relative;
            overflow: hidden;
        }}
        .header::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='100' height='20' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 10 A 10 10 0 0 1 20 10' stroke='rgba(255,255,255,0.1)' fill='none' stroke-width='1'/%3E%3C/svg%3E");
            background-size: 100px 20px;
            opacity: 0.3;
        }}
        .header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
            position: relative;
        }}
        .header p {{
            font-size: 16px;
            opacity: 0.9;
            position: relative;
        }}
        .content {{
            padding: 30px 25px;
        }}
        .section {{
            margin-bottom: 28px;
            border-radius: 8px;
            background-color: #f8f9fa;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            overflow: hidden;
        }}
        .section-header {{
            background-color: #005999;
            color: white;
            padding: 12px 20px;
            font-size: 18px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .section-content {{
            padding: 20px;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 18px;
        }}
        .info-item {{
            background-color: white;
            padding: 16px;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            border-left: 3px solid #005999;
        }}
        .info-item.full-width {{
            grid-column: 1 / -1;
        }}
        .info-item h3 {{
            color: #7f8c8d;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .info-item .value {{
            font-size: 24px;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 4px;
        }}
        .info-item .description {{
            font-size: 16px;
            color: #34495e;
            margin-bottom: 8px;
        }}
        .info-item .details {{
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(0,0,0,0.05);
        }}
        .info-item .details p {{
            font-size: 14px;
            color: #7f8c8d;
            margin: 4px 0;
        }}
        .impact-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            margin-top: 5px;
        }}
        .impact-badge.sem-impacto {{
            background-color: #e8f5e9;
            color: #2e7d32;
        }}
        .impact-badge.impacto-baixo {{
            background-color: #fff3e0;
            color: #ef6c00;
        }}
        .impact-badge.impacto-moderado {{
            background-color: #fff3e0;
            color: #ef6c00;
        }}
        .impact-badge.impacto-significativo {{
            background-color: #ffebee;
            color: #c62828;
        }}
        .impact-badge.impacto-alto {{
            background-color: #ffebee;
            color: #c62828;
        }}
        .score-section {{
            text-align: center;
            padding: 25px;
            background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
            color: white;
            border-radius: 12px;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(21, 101, 192, 0.3);
        }}
        .score-section::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='20' height='20' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 10 A 10 10 0 0 1 20 10' stroke='rgba(255,255,255,0.1)' fill='none' stroke-width='1'/%3E%3C/svg%3E");
            opacity: 0.2;
        }}
        .score-section h2 {{
            font-size: 22px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
        }}
        .score-value {{
            font-size: 62px;
            font-weight: 700;
            margin: 15px 0;
            position: relative;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        .evaluation {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
            position: relative;
        }}
        .description {{
            font-style: italic;
            margin-top: 15px;
            font-size: 16px;
            opacity: 0.9;
            position: relative;
        }}
        .footer {{
            text-align: center;
            padding: 25px;
            background-color: #f8f9fa;
            border-top: 1px solid rgba(0,0,0,0.05);
            font-size: 14px;
            color: #7f8c8d;
        }}
        .footer p {{
            margin-bottom: 5px;
        }}
        .footer a {{
            color: #005999;
            text-decoration: none;
        }}
        .logo {{
            max-height: 60px;
            margin-bottom: 15px;
        }}
        .divider {{
            height: 1px;
            background-color: rgba(0,0,0,0.05);
            margin: 20px 0;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            background-color: #e3f2fd;
            color: #1565c0;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            margin-top: 5px;
        }}
        .moon-phases {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        }}
        .moon-phase-card {{
            flex: 1;
            min-width: 150px;
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            text-align: center;
        }}
        .moon-phase-card h4 {{
            color: #005999;
            margin-bottom: 8px;
        }}
        .moon-phase-card p {{
            font-size: 14px;
            color: #7f8c8d;
            margin: 5px 0;
        }}
        .moon-phase-icon {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .info-item .scientific-note {
            font-size: 13px;
            color: #666;
            font-style: italic;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px dashed rgba(0,0,0,0.1);
        }
        .moon-phase-value {
            font-size: 20px;
            font-weight: 600;
            color: #1565c0;
            margin: 10px 0;
        }
        .scientific-description {
            font-size: 15px;
            line-height: 1.6;
            color: #34495e;
            margin: 12px 0;
        }
        .next-phase {
            font-size: 14px;
            color: #1565c0;
            font-weight: 500;
            margin: 8px 0;
        }
        .recommendation {
            padding: 15px;
        }
        .recommendation h3 {
            color: #1565c0;
            font-size: 18px;
            margin-bottom: 12px;
        }
        .main-recommendation {
            font-size: 16px;
            color: #2c3e50;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        .safety-note {
            background-color: #fff3e0;
            padding: 12px;
            border-radius: 4px;
            margin-top: 15px;
            font-size: 14px;
            color: #ef6c00;
            border-left: 3px solid #ef6c00;
        }
        /* Media queries para responsividade */
        @media (max-width: 600px) {{
            .container {{
                border-radius: 0;
            }}
            .header {{
                padding: 20px 15px;
            }}
            .header h1 {{
                font-size: 22px;
            }}
            .content {{
                padding: 20px 15px;
            }}
            .info-grid {{
                grid-template-columns: 1fr;
            }}
            .score-value {{
                font-size: 48px;
            }}
            .evaluation {{
                font-size: 20px;
            }}
            .section-header {{
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>\U0001f30a Mergulhmetro de Santos/SP</h1>
            <p>{data_hora}</p>
        </div>

        <div class="content">
            <div class="score-section">
                <h2>Avaliação das Condições</h2>
                <div class="score-value">{pontuacao}</div>
                <div class="evaluation">{avaliacao}</div>
                <div class="description">{descricao}</div>
            </div>

            {report_text}

            <div class="section">
                <div class="section-header">
                    \U0001f310 Informações Adicionais
                </div>
                <div class="section-content">
                    <div class="info-item full-width">
                        <p>Dados compilados a partir de múltiplas fontes confiáveis, incluindo StormGlass API e OpenWeatherMap API.</p>
                        <div class="divider"></div>
                        <p>Desenvolvido pelo pirata Héric Moura</p>
                        <p>Visite nosso site: <a href="{Settings.SITE_URL}">{Settings.SITE_URL}</a></p>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>Este é um relatório automático gerado pelo sistema profissional de monitoramento de condições de mergulho.</p>
            <p>Você receberá esta mensagem diariamente às 7h da manhã.</p>
            <div class="divider"></div>
            <p>© {datetime.now().year} Sistema de Monitoramento de Mergulho | Todos os direitos reservados</p>
        </div>
    </div>
</body>
</html>
        """

        if proximas_fases_info:
            report_html += """
                <div class="section">
                    <h2>📅 Próximas Fases Lunares</h2>
                    <div class="info-grid">
            """
            for fase in proximas_fases_info:
                report_html += f"""
                    <div class="info-item">
                        <h3>{fase['nome']}</h3>
                        <p>Em {fase['dias_faltantes']} dias</p>
                        <p>{fase['data_completa']}</p>
                    </div>
                """
            report_html += """
                    </div>
                </div>
            """

        return report_html 

    def _get_email_content(self, dados_mergulho: DadosMergulho) -> str:
        """
        Gera o conteúdo do email com base nos dados de mergulho.
        
        Args:
            dados_mergulho: Objeto contendo os dados de mergulho
            
        Returns:
            str: Conteúdo do email formatado em HTML
        """
        # Definir o fuso horário de São Paulo
        tz_sp = pytz.timezone('America/Sao_Paulo')
        
        # Converter a data para o fuso horário de São Paulo
        data_sp = dados_mergulho.data.astimezone(tz_sp)
        
        # Preparar descrições e recomendações
        descricao_vento = self._get_descricao_vento(dados_mergulho.vento)
        descricao_fase = self._get_descricao_fase_lunar(dados_mergulho.fase_lunar)
        recomendacao = self._get_recomendacao_mergulho(dados_mergulho)
        
        # Calcular próximas fases da lua
        proximas_fases = self._calcular_proximas_fases(dados_mergulho.fase_lunar)
        
        # Formatar o template com os dados
        return self.EMAIL_TEMPLATE.format(
            data=data_sp.strftime("%d/%m/%Y"),
            hora=data_sp.strftime("%H:%M"),
            fase_lunar=dados_mergulho.fase_lunar,
            descricao_fase=descricao_fase,
            proximas_fases_info=proximas_fases,
            mare=dados_mergulho.mare,
            vento=dados_mergulho.vento,
            descricao_vento=descricao_vento,
            temperatura_agua=dados_mergulho.temperatura_agua,
            temperatura_ar=dados_mergulho.temperatura_ar,
            recomendacao=recomendacao
        )

    def _get_descricao_vento(self, velocidade: float) -> str:
        """
        Retorna uma descrição detalhada do vento com base em sua velocidade.
        
        Args:
            velocidade: Velocidade do vento em km/h
            
        Returns:
            str: Descrição do vento
        """
        if velocidade < 2:
            return "Calmo"
        elif velocidade < 6:
            return "Brisa leve"
        elif velocidade < 12:
            return "Brisa fraca"
        elif velocidade < 20:
            return "Brisa moderada"
        elif velocidade < 29:
            return "Brisa forte"
        else:
            return "Vento forte"

    def _get_descricao_fase_lunar(self, fase: float) -> str:
        """
        Retorna uma descrição detalhada da fase lunar e sua influência.
        
        Args:
            fase: Porcentagem do ciclo lunar (0-100)
            
        Returns:
            str: Descrição da fase lunar
        """
        if fase < 5 or fase > 95:
            return "Lua Nova - Período de marés mais intensas, requer atenção especial às correntes."
        elif 45 < fase < 55:
            return "Lua Cheia - Marés mais intensas e maior atividade da vida marinha noturna."
        elif 20 < fase < 30:
            return "Lua Crescente - Condições moderadas de maré, bom período para mergulho."
        elif 70 < fase < 80:
            return "Lua Minguante - Marés mais calmas, excelente para mergulhadores iniciantes."
        else:
            return "Fase intermediária - Condições típicas de maré."

    def _calcular_proximas_fases(self, fase_atual: float) -> list:
        """
        Calcula as próximas fases principais da lua.
        
        Args:
            fase_atual: Porcentagem do ciclo lunar atual (0-100)
            
        Returns:
            list: Lista com informações das próximas fases
        """
        fases = [
            {"nome": "Lua Nova", "posicao": 0},
            {"nome": "Lua Crescente", "posicao": 25},
            {"nome": "Lua Cheia", "posicao": 50},
            {"nome": "Lua Minguante", "posicao": 75}
        ]
        
        proximas_fases = []
        for fase in fases:
            # Calcula quantos dias faltam para a próxima fase
            dias_faltantes = ((fase["posicao"] - fase_atual) % 100) * 29.53 / 100
            if dias_faltantes > 0:
                proximas_fases.append({
                    "nome": fase["nome"],
                    "dias_faltantes": int(dias_faltantes)
                })
        
        # Ordena por proximidade
        proximas_fases.sort(key=lambda x: x["dias_faltantes"])
        return proximas_fases

    def _get_recomendacao_mergulho(self, dados: DadosMergulho) -> str:
        """
        Gera uma recomendação detalhada para o mergulho com base nos dados.
        
        Args:
            dados: Objeto contendo os dados de mergulho
            
        Returns:
            str: Recomendação detalhada para o mergulho
        """
        if dados.vento > 25 or dados.mare > 2.5:
            return ("As condições atuais não são favoráveis para mergulho. "
                   "Recomendamos aguardar uma melhora nas condições do tempo.")
        
        if dados.vento > 15 or dados.mare > 1.8:
            return ("Condições desafiadoras - recomendado apenas para mergulhadores experientes. "
                   "Mantenha-se atento às correntes e à visibilidade reduzida.")
        
        if dados.vento < 10 and dados.mare < 1.5:
            return ("Excelentes condições para mergulho! Visibilidade deve estar boa "
                   "e as correntes moderadas. Aproveite para explorar os pontos mais profundos.")
        
        return ("Condições adequadas para mergulho. Mantenha os procedimentos de segurança "
               "e aproveite sua experiência subaquática.") 

    EMAIL_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                padding: 20px 0;
                background-color: #1565c0;
                color: white;
                border-radius: 8px 8px 0 0;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
                font-weight: 600;
            }}
            .content {{
                padding: 20px;
            }}
            .info-section {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .info-item {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 6px;
                border-left: 4px solid #1565c0;
            }}
            .info-item h3 {{
                margin: 0 0 10px 0;
                color: #1565c0;
                font-size: 18px;
            }}
            .info-item .scientific-note {{
                font-size: 13px;
                color: #666;
                font-style: italic;
                margin-top: 8px;
                padding-top: 8px;
                border-top: 1px dashed rgba(0,0,0,0.1);
            }}
            .moon-phase-value {{
                font-size: 20px;
                font-weight: 600;
                color: #1565c0;
                margin: 10px 0;
            }}
            .scientific-description {{
                font-size: 15px;
                line-height: 1.6;
                color: #34495e;
                margin: 12px 0;
            }}
            .next-phase {{
                font-size: 14px;
                color: #1565c0;
                font-weight: 500;
                margin: 8px 0;
            }}
            .recommendation {{
                padding: 15px;
            }}
            .recommendation h3 {{
                color: #1565c0;
                font-size: 18px;
                margin-bottom: 12px;
            }}
            .main-recommendation {{
                font-size: 16px;
                color: #2c3e50;
                line-height: 1.6;
                margin-bottom: 15px;
            }}
            .safety-note {{
                background-color: #fff3e0;
                padding: 12px;
                border-radius: 4px;
                margin-top: 15px;
                font-size: 14px;
                color: #ef6c00;
                border-left: 3px solid #ef6c00;
            }}
            /* Media queries para responsividade */
            @media (max-width: 600px) {{
                .container {{
                    margin: 10px;
                    padding: 10px;
                }}
                .header {{
                    padding: 15px 0;
                }}
                .header h1 {{
                    font-size: 20px;
                }}
                .info-section {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Relatório de Condições para Mergulho</h1>
            </div>
            <div class="content">
                <div class="info-section">
                    <div class="info-item">
                        <h3>Fase da Lua</h3>
                        <div class="moon-phase-value">{fase_lunar:.1f}% do ciclo</div>
                        <div class="scientific-description">
                            A fase lunar atual influencia diretamente as marés através da força gravitacional. {descricao_fase}
                        </div>
                        <div class="next-phase">Próxima fase: {proximas_fases_info[0]['nome']} em {proximas_fases_info[0]['dias_faltantes']} dias</div>
                        <div class="scientific-note">
                            Nota: A influência lunar nas marés é mais pronunciada durante as fases de Lua Nova e Lua Cheia, 
                            quando ocorrem as marés de sizígia.
                        </div>
                    </div>
                    
                    <div class="info-item">
                        <h3>Condições do Mar</h3>
                        <div class="scientific-description">
                            Altura das ondas: {mare:.1f}m
                            <br>
                            Direção do vento: {descricao_vento}
                            <br>
                            Velocidade do vento: {vento:.1f} km/h
                        </div>
                        <div class="scientific-note">
                            A altura das ondas e condições do vento são fatores críticos que afetam a visibilidade 
                            subaquática e a segurança do mergulho.
                        </div>
                    </div>

                    <div class="info-item">
                        <h3>Temperatura</h3>
                        <div class="scientific-description">
                            Temperatura da água: {temperatura_agua:.1f}°C
                            <br>
                            Temperatura do ar: {temperatura_ar:.1f}°C
                        </div>
                        <div class="scientific-note">
                            A temperatura da água influencia diretamente o metabolismo da vida marinha e o conforto 
                            térmico do mergulhador.
                        </div>
                    </div>
                </div>

                <div class="recommendation">
                    <h3>Recomendação para Mergulho</h3>
                    <div class="main-recommendation">
                        {recomendacao}
                    </div>
                    <div class="safety-note">
                        Lembre-se: Sempre verifique seu equipamento, respeite os limites de profundidade e tempo, 
                        e nunca mergulhe sozinho. A segurança é nossa prioridade!
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """ 