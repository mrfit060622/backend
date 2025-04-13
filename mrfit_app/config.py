import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# Carregar variáveis do .env
load_dotenv()

# Configuração do ambiente
ENV = os.getenv('FLASK_ENV', 'development')  # Agora assume 'development' como padrão

# Configuração base comum para todos os ambientes
class Config:
    """Configuração base comum para todos os ambientes"""
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Configuração de sessão
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() in ['true', '1']
    SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY', 'True').lower() in ['true', '1']
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')

    # Configuração de e-mail
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # Verificação das configurações de e-mail
    if not all([MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER]):
        raise ValueError("⚠️ ERRO: Variáveis de ambiente para configuração de e-mail não foram carregadas corretamente.")
    
    # Configuração de API
    API_HOST = os.getenv('API_HOST', 'https://api.exemplo.com')
    
    # Configuração do banco de dados
    DB_HOST = os.getenv('DB_HOST_DEV', 'localhost')
    DB_PORT = os.getenv('DB_PORT_DEV', 3306)
    DB_USER = os.getenv('DB_USER_DEV', 'root')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD_DEV'))  # Escapar caracteres especiais
    DB_NAME = os.getenv('DB_NAME_DEV', 'mrfit_db')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Criação do engine do banco de dados
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    # Criando a sessionmaker para a sessão local
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Exportando a SessionLocal corretamente
SessionLocal = Config.SessionLocal
