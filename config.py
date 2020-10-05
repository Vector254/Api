import os

class Config:

    SECRET_KEY="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://vector:12345q@localhost/quotes"

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}