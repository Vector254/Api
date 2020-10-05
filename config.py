import os

class Config:

    SECRET_KEY="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://vector:12345q@localhost/quotes"

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}