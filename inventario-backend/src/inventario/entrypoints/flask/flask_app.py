import json

from flask import request, Response
from sqlalchemy.orm import sessionmaker

from .. import app
from .security import token_required
from ...adapters.database import model
from ...adapters.view import cqrs
from ...adapters.view.mapper import SistemaViewModekMapper, ComponenteViewModelMapper
from ...adapters.view.model import SistemaInformacionViewDto, ComponenteViewDto
from ...domain import commands
from ...service_layer import unit_of_work, messagebus

sistema_mapper = SistemaViewModekMapper()
componente_mapper = ComponenteViewModelMapper()


def _get_sistema(sistema_id: str):
    cmd = commands.ObtenerSistema(sistema_id)
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    results = messagebus.handle(cmd, uow)
    sistema = results.pop(0)
    return sistema

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return Response("OK", status=200, mimetype="text/plain")

@app.route("/api/v1/sistemas", methods=["GET"])
@token_required
def get_sistemas(jwt_token=None):
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
@token_required
def get_sistema(sistema_id: str, jwt_token=None):
    sistema = _get_sistema(sistema_id)
    if not sistema:
        return "Not found", 404
    return Response(
        json.dumps(sistema_mapper.to_view(sistema).model_dump(mode="json", exclude_none=True), sort_keys=False),
        status=200, mimetype='application/json')


@app.route("/api/v1/sistemas", methods=["POST"])
@token_required
def post_sistema(jwt_token=None):
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
@token_required
def put_sistema(sistema_id: str, jwt_token=None):
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
@token_required
def get_componentes_sistema(sistema_id: str, jwt_token=None):
    sistema = _get_sistema(sistema_id)
    if not sistema:
        return "Not found", 404

    return Response(
        json.dumps(
            [componente_mapper.to_view(componente).model_dump(mode="json") for componente in sistema.componentes]),
        status=200, mimetype='application/json')


@app.route("/api/v1/sistemas/<sistema_id>/componentes/<componente_id>", methods=["GET"])
@token_required
def get_componente_sistema(sistema_id: str, componente_id: str, jwt_token=None):
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

@app.route("/api/v1/sistemas/<sistema_id>/componentes/<componente_id>", methods=["PUT"])
@token_required
def put_componente_sistema(sistema_id: str, componente_id: str, jwt_token=None):
    json_componente = request.get_json()

    componente_view = ComponenteViewDto(**json_componente)
    sistema = _get_sistema(sistema_id)
    if not sistema:
        return "Not found", 404
    # componente = next(
    #     iter([componente for componente in sistema.componentes if componente.componente_id == componente_id]), None)
    # if not componente:
    #     return "Not found", 404

    cmd = commands.ModificarComponente(
        sistema_id,
        componente_id,
        componente_view.nombre,
        componente_view.tipo,
        componente_view.observaciones
    )
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    results = messagebus.handle(cmd, uow)
    componente = results.pop(0)

    if not componente:
        return "Not found", 404

    return Response(
        json.dumps(
            componente_mapper.to_view(componente).model_dump(mode="json")),
        status=200, mimetype='application/json')

@app.route("/api/v1/dir3/unidades", methods=["GET"])
@token_required
def get_unidades_dir3(jwt_token=None):
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
@token_required
def get_unidad_dir3(unidad_id, jwt_token=None):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    unidad = cqrs.unidad_dir3(unidad_id, uow)
    if unidad is None:
        return "Unidad no encontrada", 404
    return Response(
        json.dumps(unidad.model_dump(mode="json")),
        status=200, mimetype='application/json')

@app.route("/api/v1/tiposComponente", methods=["GET"])
@token_required
def get_tipos_componente(jwt_token=None):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sessionmaker(bind=model.db.engine))
    tipos_componente = cqrs.tipos_componente(uow)
    return Response(
        json.dumps(tipos_componente.model_dump(mode="json")),
        status=200, mimetype='application/json')