"""
Configuration for different environments
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///data/api_monitor.db'
    
    # Heroku uses postgres:// but SQLAlchemy needs postgresql://
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Monitoring settings
    DEFAULT_CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', 300))
    DEFAULT_TIMEOUT = int(os.environ.get('DEFAULT_TIMEOUT', 30))
    
    # Flask settings
    DEBUG = os.environ.get('FLASK_ENV') == 'development'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
