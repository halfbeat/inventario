import json
import os
from logging.config import dictConfig

from flask import Flask, request, Response
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker

from ..adapters.database import model
from ..adapters.view import cqrs
from ..adapters.view.mapper import SistemaViewModekMapper, ComponenteViewModelMapper
from ..adapters.view.model import SistemaInformacionViewDto
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
# Carga los parámetros de configuración desde variables de entorno
app.config.from_prefixed_env()

# Inicializa las extensiones
model.db.init_app(app)
migrate = Migrate(app, model.db)

sistema_mapper = SistemaViewModekMapper()
componente_mapper = ComponenteViewModelMapper()


def _get_sistema(sistema_id: str):
    cmd = commands.ObtenerSistema(sistema_id)
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    results = messagebus.handle(cmd, uow)
    sistema = results.pop(0)
    return sistema


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
    sistema = _get_sistema(sistema_id)
    if not sistema:
        return "Not found", 404
    return Response(
        json.dumps(sistema_mapper.to_view(sistema).model_dump(mode="json", exclude_none=True), sort_keys=False),
        status=200, mimetype='application/json')

@app.route("/api/v1/sistemas", methods=["POST"])
def post_sistema():
    json_sistema = request.get_json()

    sistema_view = SistemaInformacionViewDto(**json_sistema)
    cmd = commands.RegistrarSistema(
        sistema_view.sistema_id,
        sistema_view.nombre,
        sistema_view.unidad_responsable,
        sistema_view.tecnico_responsable,
        sistema_view.observaciones
    )
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    results = messagebus.handle(cmd, uow)
    sistema = results.pop(0)
    if not sistema:
        return "Not found", 404
    return Response(
        json.dumps(sistema_mapper.to_view(sistema).model_dump(mode="json", exclude_none=True), sort_keys=False),
        status=200, mimetype='application/json')

@app.route("/api/v1/sistemas/<sistema_id>", methods=["PUT"])
def put_sistema(sistema_id: str):
    json_sistema = request.get_json()

    sistema_view = SistemaInformacionViewDto(**json_sistema)
    cmd = commands.ModificarSistema(
        sistema_id,
        sistema_view.nombre,
        sistema_view.unidad_responsable,
        sistema_view.tecnico_responsable,
        sistema_view.observaciones
    )
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    results = messagebus.handle(cmd, uow)
    sistema = results.pop(0)
    if not sistema:
        return "Not found", 404
    return Response(
        json.dumps(sistema_mapper.to_view(sistema).model_dump(mode="json", exclude_none=True), sort_keys=False),
        status=200, mimetype='application/json')


@app.route("/api/v1/sistemas/<sistema_id>/componentes", methods=["GET"])
def get_componentes_sistema(sistema_id: str):
    sistema = _get_sistema(sistema_id)
    if not sistema:
        return "Not found", 404

    return Response(
        json.dumps(
            [componente_mapper.to_view(componente).model_dump(mode="json") for componente in sistema.componentes]),
        status=200, mimetype='application/json')


@app.route("/api/v1/sistemas/<sistema_id>/componentes/<componente_id>", methods=["GET"])
def get_componente_sistema(sistema_id: str, componente_id: str):
    sistema = _get_sistema(sistema_id)
    if not sistema:
        return "Not found", 404
    componente = next(
        iter([componente for componente in sistema.componentes if componente.componente_id == componente_id]), None)
    if not componente:
        return "Not found", 404

    return Response(
        json.dumps(
            componente_mapper.to_view(componente).model_dump(mode="json")),
        status=200, mimetype='application/json')


@app.route("/api/v1/dir3/unidades", methods=["GET"])
def get_unidades_dir3():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 300, type=int)
    if page < 1:
        return "El número de página no puede ser menor que 1", 400
    if page_size < 0:
        return "El número de página no puede ser negativo", 400
    id_unidad = request.args.get("id", None)
    nombre_unidad = request.args.get("nombre", None)

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    listado_unidades = cqrs.unidades_dir3(id_unidad, nombre_unidad, page, page_size, uow)
    return listado_unidades.model_dump(mode="json", exclude_none=True), 200


@app.route("/api/v1/dir3/unidades/<unidad_id>", methods=["GET"])
def get_unidad_dir3(unidad_id):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    unidad = cqrs.unidad_dir3(unidad_id, uow)
    if unidad is None:
        return "Unidad no encontrada", 404
    return Response(
        json.dumps(unidad.model_dump(mode="json")),
        status=200, mimetype='application/json')
