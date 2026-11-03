import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'villetaneuse-corp-secret-key-2026')
    DEBUG = False
    TESTING = False
    APP_NAME = "Villetaneuse Corp - RecoCompare"
    VERSION = "0.1.0"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
