import os


class Config:
    """
    Base configuration.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get("REDIS_URL")
    KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")


class DevelopmentConfig(Config):
    """
    Development configuration.
    """

    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration.
    """

    DEBUG = False


config = {"development": DevelopmentConfig, "production": ProductionConfig, "default": DevelopmentConfig}
