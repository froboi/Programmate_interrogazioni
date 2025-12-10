"""
Configurazione dell'applicazione Flask
Gestisce le configurazioni per diversi ambienti (development, production)
"""
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()


class Config:
    """
    Classe base di configurazione
    """
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database MySQL
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'interrogazioni_db')
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # TinyDB
    TINYDB_PATH = os.getenv('TINYDB_PATH', 'database/local_db.json')
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'csv', 'json'}
    
    # Esportazioni
    EXPORT_FOLDER = 'exports'


class DevelopmentConfig(Config):
    """
    Configurazione per ambiente di sviluppo
    """
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """
    Configurazione per ambiente di produzione
    """
    DEBUG = False
    TESTING = False


# Dizionario delle configurazioni disponibili
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name='default'):
    """
    Restituisce la configurazione richiesta
    
    Args:
        config_name (str): Nome della configurazione (development, production, default)
        
    Returns:
        Config: Oggetto di configurazione
    """
    return config_by_name.get(config_name, DevelopmentConfig)
