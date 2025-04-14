import os
from datetime import datetime
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, Column, String, Text
from sqlalchemy.orm import sessionmaker
from ..adapters import orm



settings_module = os.getenv("APP_SETTINGS_MODULE")

app = Flask(__name__, instance_relative_config=True)
# Carga los parámetros de configuración según el entorno
app.config.from_object(settings_module)
# Carga la configuración del directorio instance
app.config.from_pyfile("config.py", silent=True)

# Inicializa las extensiones
orm.db.init_app(app)
migrate = Migrate(app, orm.db)

@app.route("/add_batch", methods=["GET"])
def add_batch():
    pass