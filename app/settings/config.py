"""Project base settings."""
import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
RQ_DEFAULT_HOST = 'localhost'
RQ_DEFAULT_PORT = 6379
RQ_DEFAULT_PASSWORD = None
RQ_DEFAULT_DB = 0
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = '587'
EMAIL_FROM = 'somefakeuser@mail.com'
MAIL_USERNAME = 'somefakeuser@mail.com'
MAIL_PASSWORD = ''
MAIL_USE_TLS = True
MAIL_NO_REPLY = 'somefakeuser@mail.com'
MAIL_DEFAULT_SENDER = ''
LOG_FILENAME = 'parser.log'
COMPRESS_FILE = False
HOST_PARSING = 'http://yell.ru'
DEBUG = False

try:
    from app.settings.config_local import *  # noqa
except ImportError:
    pass
