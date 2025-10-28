from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from mrfit_app.config import DatabaseConfig  # Agora importa a configuração correta
from flask_sslify import SSLify
# Instâncias globais das extensões
db = SQLAlchemy()
mail = Mail()

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    sslify = SSLify(app)  # Força HTTPS
    # Carrega as configurações da classe DatabaseConfig
    app.config.from_object(DatabaseConfig)
     
    
    api_host = app.config.get('API_HOST', 'https://api.exemplo.com')
    print (f"API Host configurado: {api_host}")
    # Inicializa as extensões
    db.init_app(app)
    mail.init_app(app)

    # Configuração do CORS
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    # Importação das rotas dentro da função para evitar importação circular
    from mrfit_app.rotas.cadastros import bp_usuario
    from mrfit_app.rotas.calculos_rota import bp_calculo
    from mrfit_app.rotas.pdf import pdf_bp

    # Registro dos blueprints
    app.register_blueprint(bp_usuario, url_prefix='/usuario')
    app.register_blueprint(bp_calculo, url_prefix='/calculo')
    app.register_blueprint(pdf_bp, url_prefix='/pdf')

    return app
