import json
import os
from logging.config import dictConfig

from flask import Flask, request, Response
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker

from ..adapters.database import model
from ..adapters.view import cqrs
from ..adapters.view.mapper import SistemaViewModekMapper, ComponenteViewModekMapper
from ..domain import commands
from ..service_layer import unit_of_work, messagebus

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


@app.route("/api/v1/sistemas", methods=["GET"])
def get_sistemas():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    if page < 1:
        return "El número de página no puede ser menor que 1", 400
    if page_size < 0:
        return "El número de página no puede ser negativo", 400
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    listado_sistemas = cqrs.sistemas(page, page_size, uow)
    return listado_sistemas.model_dump(mode="json", exclude_none=True), 200


@app.route("/api/v1/sistemas/<sistema_id>", methods=["GET"])
def get_sistema(sistema_id: str):
    mapper = SistemaViewModekMapper()

    cmd = commands.ObtenerSistema(
        sistema_id
    )
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    results = messagebus.handle(cmd, uow)
    sistema = results.pop(0)
    if not sistema:
        return "Not found", 404
    return Response(json.dumps(mapper.to_view(sistema).model_dump(mode="json", exclude_none=True), sort_keys=False),
                    status=200, mimetype='application/json')


@app.route("/api/v1/sistemas/<sistema_id>/componentes", methods=["GET"])
def get_componentes_sistema(sistema_id: str):
    mapper = ComponenteViewModekMapper()

    cmd = commands.ObtenerSistema(sistema_id)
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    results = messagebus.handle(cmd, uow)
    sistema = results.pop(0)
    if not sistema:
        return "Not found", 404

    return Response(
        json.dumps([mapper.to_view(componente).model_dump(mode="json") for componente in sistema.componentes]),
        status=200, mimetype='application/json')


@app.route("/api/v1/dir3/unidades", methods=["GET"])
def get_unidades_dir3():
    id_unidad = request.args.get("id", None)
    nombre_unidad = request.args.get("nombre", None)

    cmd = commands.BuscarUnidadesDir3(id_unidad, nombre_unidad)
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    results = messagebus.handle(cmd, uow)
    unidades = results.pop(0)
    if not unidades:
        unidades = []

    return Response(json.dumps(unidades), status=200, mimetype='application/json')
