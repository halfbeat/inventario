from flask import request, Blueprint
from flask_restful import Api, Resource

from app.inventario.api_v1_0.logic import SistemaInformacionService, UnidadDir3Service
from app.security import token_required

api_v1_0_bp = Blueprint("api_v1_0_bp", __name__)

api = Api(api_v1_0_bp)

class SistemasInformacionResource(Resource):
    @token_required
    def get(self, jwt_token=None):
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("page_size", 25, type=int)

        return SistemaInformacionService.get_sistemas(page, page_size)

    @token_required
    def post(self, jwt_token=None):
        sistema_id = request.get_json().get("sistema_id")
        SistemaInformacionService.alta_sistema(request.get_json())
        return SistemaInformacionService.get_sistema(sistema_id)


class SistemaInformacionResource(Resource):
    @token_required
    def get(self, sistema_id, jwt_token=None):
        return SistemaInformacionService.get_sistema(sistema_id)

    @token_required
    def put(self, sistema_id, jwt_token=None):
        SistemaInformacionService.modificar_sistema(sistema_id, request.get_json())
        return SistemaInformacionService.get_sistema(sistema_id)


class UnidadesDir3Resource(Resource):
    @token_required
    def get(self, jwt_token=None):
        return UnidadDir3Service.buscar_unidades(unidad_id=request.args.get('id'), nombre=request.args.get('nombre'))

class UnidadDir3Resource(Resource):
    @token_required
    def get(self, unidad_id, jwt_token=None):
        return UnidadDir3Service.obtener_unidad(unidad_id=unidad_id)

api.add_resource(
    SistemasInformacionResource,
    "/api/v1/sistemas/",
    endpoint="sistemas_resource",
)

api.add_resource(
    SistemaInformacionResource,
    "/api/v1/sistemas/<sistema_id>",
    endpoint="sistema_resource",
)

api.add_resource(
    UnidadesDir3Resource,
    '/api/v1/dir3/unidades/',
    endpoint="unidades_resource",
)

api.add_resource(
    UnidadDir3Resource,
    '/api/v1/dir3/unidades/<unidad_id>',
    endpoint="unidad_resource",
)
