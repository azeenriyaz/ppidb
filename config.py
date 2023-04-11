"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    SERVER_NAME = 'localhost:' + environ.get('PORT')
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'
    SESSION_COOKIE_DOMAIN = 'localhost.localdomain'
    SECRET_KEY = environ.get('SECRET_KEY')
    RECAPTCHA_PUBLIC_KEY = environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = environ.get("RECAPTCHA_PRIVATE_KEY")
    PORT = environ.get('PORT')
    STATIC_FOLDER = basedir + environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = basedir + environ.get('TEMPLATES_FOLDER')
    INSTANCE_PATH = environ.get('INSTANCE_PATH')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True