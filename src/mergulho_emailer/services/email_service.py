import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from ..config.settings import Settings
from ..models.moon_phase import MoonPhase

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
                            <p>{descricao_vento}</p>
                            <p>{impacto_vento}</p>
                        </div>
                        <div class="info-item">
                            <h3>Precipitação</h3>
                            <p>{descricao_precip}</p>
                            <p>{impacto_precip}</p>
                        </div>
                        <div class="info-item">
                            <h3>Maré</h3>
                            <p>{descricao_mare}</p>
                            <p>{impacto_mare}</p>
                        </div>
                        <div class="info-item">
                            <h3>Correntes</h3>
                            <p>{descricao_corrente}</p>
                            <p>{impacto_corrente}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-header">
                    \U0001f319 Fase Lunar
                </div>
                <div class="section-content">
                    <div class="info-grid">
                        <div class="info-item">
                            <h3>Fase Atual</h3>
                            <p>{nome_fase}</p>
                            <p>{descricao_fase}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-header">
                    \U0001f30f Recomendações
                </div>
                <div class="section-content">
                    <div class="info-item full-width">
                        <p>{recomendacao}</p>
                    </div>
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
        }}
        .info-item p {{
            font-size: 16px;
            color: #2c3e50;
            line-height: 1.5;
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