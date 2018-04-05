"""Application package."""
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

app.config.from_pyfile('settings/config.py')

mail = Mail(app)

handler = RotatingFileHandler(app.config['LOG_FILENAME'], maxBytes=10000, backupCount=1)
logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

from app import views  # noqa
