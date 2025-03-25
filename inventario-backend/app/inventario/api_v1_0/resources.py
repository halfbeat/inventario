from flask import request, Blueprint
from flask_restful import Api, Resource

from app.inventario.api_v1_0.logic import SistemaService
from app.security import token_required
from .schemas import (
    ListaPaginablePermisosAplicacionSchema,
    ListaPaginablePermisosRolSchema,
    ListaPaginableRolesAplicacionSchema,
)

api_v1_0_bp = Blueprint("api_v1_0_bp", __name__)

roles_aplicacion_schema = ListaPaginableRolesAplicacionSchema()
permisos_aplicacion_schema = ListaPaginablePermisosAplicacionSchema()
permisos_rol_schema = ListaPaginablePermisosRolSchema()

api = Api(api_v1_0_bp)

class SistemasInformacionResource(Resource):
    @token_required
    def get(self, jwt_token=None):
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("page_size", 25, type=int)

        return SistemaService.get_aplicaciones(page, page_size)

    @token_required
    def post(self, jwt_token=None):
        SistemaService.altaAplicacion(request.get_json())


class SistemaInformacionResource(Resource):
    @token_required
    def get(self, sistema_id, jwt_token=None):
        return SistemaService.get_sistema(sistema_id)


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

