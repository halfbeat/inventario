import os
from logging.config import dictConfig

from flask import Flask
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker

from ..adapters.database import model
from ..adapters.view.mapper import SistemaViewModekMapper
from ..service_layer import unit_of_work

dictConfig({
    'version': 1,
    'root': {
        'level': 'DEBUG'
    }
})

settings_module = os.getenv("APP_SETTINGS_MODULE")

app = Flask(__name__, instance_relative_config=True)
# Carga los parámetros de configuración según el entorno
app.config.from_object(settings_module)
# Carga la configuración del directorio instance
app.config.from_pyfile("config.py", silent=True)


# Inicializa las extensiones
model.db.init_app(app)
migrate = Migrate(app, model.db)


@app.route("/sistemas", methods=["GET"])
def get_sistemas():
    mapper = SistemaViewModekMapper()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    with uow:
        sistema = uow.sistemas.get("AUTHZ")

    if not sistema:
        return "Not found", 404

    return mapper.to_view(sistema).model_dump(mode="json", exclude_none=True), 200
