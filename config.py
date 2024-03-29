from os import environ, path
from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, '.env'))


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = 'Content-Type'

    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 86400
    JWT_COOKIE_SAMESITE = "Strict"
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1000)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=14)
    JWT_COOKIE_SECURE = True
    JWT_CSRF_IN_COOKIES = True
    JWT_COOKIE_CSRF_PROTECT = True


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')
    STRIPE_API_KEY = environ.get('STRIPE_PROD_API_KEY')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    CORS_ORIGINS = ["http://localhost:3000"]
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    STRIPE_API_KEY = environ.get('STRIPE_TEST_API_KEY')


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
}
