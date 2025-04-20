from logging.config import dictConfig

from flask import Flask
from flask_migrate import Migrate
from ..adapters.database import model

dictConfig({
    'version': 1,
    'root': {
        'level': 'DEBUG'
    }
})

app = Flask(__name__, instance_relative_config=True)
# Carga los parámetros de configuración desde variables de entorno
app.config.from_prefixed_env()

# Inicializa las extensiones
model.db.init_app(app)
migrate = Migrate(app, model.db)

from .flask import flask_app
