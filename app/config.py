import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'villetaneuse-corp-secret-key-2026')
    DEBUG = False
    TESTING = False
    APP_NAME = "Villetaneuse Corp - RecoCompare"
    VERSION = "0.1.0"
    
    # Configuration Base de Données SQLite
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH",
        os.path.join(BASE_DIR, "data", "players.db")
    )
    CSV_PATH = os.environ.get(
        "CSV_PATH",
        os.path.join(BASE_DIR, "data", "FC26_db.csv")
    )

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    # Base de données de test en mémoire ou fichier de test
    DATABASE_PATH = os.environ.get(
        "TEST_DATABASE_PATH",
        os.path.join(BASE_DIR, "data", "test_players.db")
    )

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
