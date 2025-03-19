# config/dev.py

from . import default
from .default import *

APP_ENV = default.APP_ENV_DEVELOPMENT

SQLALCHEMY_DATABASE_URI = 'postgresql://authz:authz@192.168.1.160:31801/authz'
