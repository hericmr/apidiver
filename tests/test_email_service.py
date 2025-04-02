import unittest
from unittest.mock import patch, Mock, MagicMock
from src.mergulho_emailer.services.email_service import EmailService
from src.mergulho_emailer.models.moon_phase import MoonPhase

class TestEmailService(unittest.TestCase):
    def setUp(self):
        self.email_service = EmailService()
        self.test_report = "Test Report Content"
        self.test_evaluation = "EXCELENTE"
        self.test_score = 85
        self.test_description = "Condições ideais para mergulho."

    @patch('smtplib.SMTP')
    def test_send_report_success(self, mock_smtp):
        """Testa o envio de email com sucesso"""
        # Configurar mock
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

        # Executar teste
        success = self.email_service.send_report(
            self.test_report,
            self.test_evaluation,
            self.test_score,
            self.test_description
        )

        self.assertTrue(success)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once()
        mock_smtp_instance.send_message.assert_called_once()

    @patch('smtplib.SMTP')
    def test_send_report_failure(self, mock_smtp):
        """Testa falha no envio de email"""
        # Configurar mock para falhar
        mock_smtp.side_effect = Exception("SMTP Error")

        # Executar teste
        success = self.email_service.send_report(
            self.test_report,
            self.test_evaluation,
            self.test_score,
            self.test_description
        )

        self.assertFalse(success)

    def test_generate_html_report(self):
        """Testa a geração do HTML do relatório"""
        # Dados de teste
        data_hora = "02/04/2024 10:00"
        fase_lunar = 0
        nome_fase = "Lua Nova"
        descricao_fase = "Descrição da fase lunar"
        vento = 10.0
        descricao_vento = "Vento moderado"
        impacto_vento = "Impacto moderado"
        precipitacao = 0.0
        descricao_precip = "Sem chuva"
        impacto_precip = "Sem impacto"
        mare = 1.2
        descricao_mare = "Maré média"
        impacto_mare = "Impacto baixo"
        velocidade_corrente = 1.0
        descricao_corrente = "Correntes Norte"
        impacto_corrente = "Impacto moderado"
        estacao = "Verão"
        avaliacao = "EXCELENTE"
        pontuacao = 85
        descricao = "Condições ideais"
        recomendacao = "Aproveite para mergulhar"
        
        # Criar fase lunar de teste
        fase_atual = MoonPhase({
            'phase': 'Lua Nova',
            'year': 2024,
            'month': 4,
            'day': 2
        })
        proximas_fases = [
            MoonPhase({
                'phase': 'Quarto Crescente',
                'year': 2024,
                'month': 4,
                'day': 9
            })
        ]

        # Gerar relatório
        report_html = self.email_service.generate_html_report(
            data_hora, fase_lunar, nome_fase, descricao_fase,
            vento, descricao_vento, impacto_vento,
            precipitacao, descricao_precip, impacto_precip,
            mare, descricao_mare, impacto_mare,
            velocidade_corrente, descricao_corrente, impacto_corrente,
            estacao, avaliacao, pontuacao, descricao, recomendacao,
            fase_atual, proximas_fases
        )

        # Verificar se o HTML contém elementos esperados
        self.assertIn('<html', report_html)
        self.assertIn('<head', report_html)
        self.assertIn('<body', report_html)
        self.assertIn('Mergulhmetro de Santos/SP', report_html)
        self.assertIn(str(pontuacao), report_html)
        self.assertIn(avaliacao, report_html)
        self.assertIn(descricao, report_html)

if __name__ == '__main__':
    unittest.main() 