# config/local.py

from . import default
from .default import *

APP_ENV = default.APP_ENV_LOCAL
SQLALCHEMY_DATABASE_URI = 'sqlite:///authz.sqlite'
