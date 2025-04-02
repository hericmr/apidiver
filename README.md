# Mergulho Emailer

Sistema automatizado para verificação de condições de mergulho livre e envio de relatórios por email.

## Funcionalidades

- Consulta de fase lunar atual e próximas fases
- Monitoramento de condições meteorológicas
- Análise de correntes marítimas
- Geração de relatórios detalhados
- Envio automático de relatórios por email

## Requisitos

- Python 3.8 ou superior
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/mergulho-emailer.git
cd mergulho-emailer
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Configuração

As principais configurações podem ser ajustadas no arquivo `src/mergulho_emailer/config/settings.py`:

- Localização (latitude/longitude)
- Chaves de API
- Configurações de email

## Uso

Para executar o programa:

```bash
python -m src.mergulho_emailer
```

## Testes

Para executar os testes:

```bash
pytest tests/
```

Para executar os testes com cobertura:

```bash
pytest --cov=src tests/
```

## Estrutura do Projeto

```
mergulho-emailer/
├── src/
│   └── mergulho_emailer/
│       ├── config/
│       │   └── settings.py
│       ├── models/
│       │   ├── moon_phase.py
│       │   └── weather.py
│       ├── services/
│       │   ├── moon_service.py
│       │   ├── weather_service.py
│       │   └── email_service.py
│       ├── app.py
│       └── __main__.py
├── tests/
│   ├── test_moon_phase.py
│   ├── test_weather.py
│   └── test_app.py
├── requirements.txt
└── README.md
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 