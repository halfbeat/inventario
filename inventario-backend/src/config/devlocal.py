# config/dev.py

from . import default

APP_ENV = default.APP_ENV_DEVELOPMENT

SQLALCHEMY_DATABASE_URI = 'postgresql://inventario:inventario@localhost:5432/inventario'
