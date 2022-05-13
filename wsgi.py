from app import init_app
from os import environ

app = init_app(environ.get('FLASK_CONFIG'))
