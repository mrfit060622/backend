import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Carregar variáveis do .env
load_dotenv()

# Configuração do ambiente
ENV = os.getenv('FLASK_ENV', 'SQLITE')  # Agora assume 'development' como padrão

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

# Banco de Dados - Configurações por Ambiente (Desenvolvimento, Produção, SQLite)
class DatabaseConfig(Config):
    if ENV == 'development':
        DB_HOST = os.getenv('DB_HOST_DEV')
        DB_PORT = os.getenv('DB_PORT_DEV')
        DB_USER = os.getenv('DB_USER_DEV')
        DB_PASSWORD = os.getenv('DB_PASSWORD_DEV')
        DB_NAME = os.getenv('DB_NAME_DEV')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    elif ENV == 'production':
        DB_HOST = os.getenv('DB_HOST_PROD')
        DB_PORT = os.getenv('DB_PORT_PROD')
        DB_USER = os.getenv('DB_USER_PROD')
        DB_PASSWORD = os.getenv('DB_PASSWORD_PROD')
        DB_NAME = os.getenv('DB_NAME_PROD')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    else:  # Caso seja SQLite
        DB_URI = os.getenv('DB_URI', 'sqlite:///database.db')
        SQLALCHEMY_DATABASE_URI = DB_URI
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Criando engine e sessão local corretamente dentro da classe
    engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False} if 'sqlite' in SQLALCHEMY_DATABASE_URI else {})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Agora, exportando a SessionLocal corretamente
SessionLocal = DatabaseConfig.SessionLocal
