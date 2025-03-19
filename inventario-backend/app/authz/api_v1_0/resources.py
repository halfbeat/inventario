import traceback
from flask import abort, request, Blueprint
from flask_restful import Api, Resource

from app.authz.api_v1_0.logic import AplicacionService, SecurityService
from app.security import token_required

from app.authz.models import (
    AplicacionModelDto,
    PermisoModelDto,
    RolModelDto,
    PermisosRolModelDto,
)
from .schemas import (
    ListaPaginablePermisosAplicacionSchema,
    ListaPaginablePermisosRolSchema,
    ListaPaginableRolesAplicacionSchema,
)

authz_v1_0_bp = Blueprint("api_v1_0_bp", __name__)

roles_aplicacion_schema = ListaPaginableRolesAplicacionSchema()
permisos_aplicacion_schema = ListaPaginablePermisosAplicacionSchema()
permisos_rol_schema = ListaPaginablePermisosRolSchema()

api = Api(authz_v1_0_bp)


class AplicacionesResource(Resource):
    @token_required
    def get(self, jwt_token=None):
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("page_size", 25, type=int)

        if not SecurityService.has_permission(
                jwt_token["principal"], "AUTHZ", "aplicaciones:read"
        ):
            abort(403, "No tiene permisos para realizar esta operación")
        return AplicacionService.get_aplicaciones(page, page_size)

    @token_required
    def post(self, jwt_token=None):
        AplicacionService.altaAplicacion(request.get_json())


class AplicacionResource(Resource):
    @token_required
    def get(self, idAplicacion, jwt_token=None):
        return AplicacionService.get_aplicacion(idAplicacion)


class RolesAplicacionResource(Resource):
    @token_required
    def get(self, idAplicacion, jwt_token=None):
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("page_size", 25, type=int)
        aplicacion = AplicacionModelDto.get_by_id(aplicacion_id=idAplicacion)
        if not aplicacion:
            abort(404, "Aplicación no encontrada")
        try:
            roles = RolModelDto.simple_page_filter(
                page, page_size, aplicacion_id=idAplicacion
            )
            result = roles_aplicacion_schema.dump(
                {
                    "items": roles.items,
                    "total": roles.total,
                    "page": page,
                    "page_size": page_size,
                },
                many=False,
            )
            return result
        except Exception as e:
            print(traceback.format_exc())
            abort(400, "Revise los parámetros de la consulta")


class PermisosAplicacionResource(Resource):
    @token_required
    def get(self, idAplicacion, jwt_token=None):
        page = request.args.get("page", 0, type=int)
        page_size = request.args.get("page_size", 25, type=int)
        aplicacion = AplicacionModelDto.get_by_id(aplicacion_id=idAplicacion)
        if not aplicacion:
            abort(404, "Aplicación no encontrada")
        try:
            permisos = PermisoModelDto.simple_page_filter(
                page, page_size, aplicacion_id=idAplicacion
            )
            result = permisos_aplicacion_schema.dump(
                {
                    "items": permisos.items,
                    "total": permisos.total,
                    "page": page,
                    "page_size": page_size,
                },
                many=False,
            )
            return result
        except Exception as e:
            print(traceback.format_exc())
            abort(400, "Revise los parámetros de la consulta")


class PermisosRolResource(Resource):
    @token_required
    def get(self, idAplicacion, idRol, jwt_token=None):
        page = request.args.get("page", 0, type=int)
        page_size = request.args.get("page_size", 25, type=int)
        aplicacion = AplicacionModelDto.get_by_id(idAplicacion)
        if not aplicacion:
            abort(404, "Aplicación no encontrada")
        rol = RolModelDto.get_by_id((idAplicacion, idRol))
        if not rol:
            abort(404, "Rol no encontrado")
        try:
            permisosRol = PermisosRolModelDto.simple_page_filter(
                page, page_size, aplicacion_id=idAplicacion, rol_id=idRol
            )
            result = permisos_rol_schema.dump(
                {
                    "items": [permiso.permiso_id for permiso in permisosRol.items],
                    "total": permisosRol.total,
                    "page": page,
                    "page_size": page_size,
                },
                many=False,
            )
            return result
        except Exception as e:
            print(traceback.format_exc())
            abort(400, "Revise los parámetros de la consulta")


api.add_resource(
    AplicacionesResource,
    "/api/v1/aplicaciones/",
    endpoint="aplicaciones_resource",
)

api.add_resource(
    AplicacionResource,
    "/api/v1/aplicaciones/<idAplicacion>",
    endpoint="aplicacion_resource",
)

api.add_resource(
    RolesAplicacionResource,
    "/api/v1/aplicaciones/<idAplicacion>/roles/",
    endpoint="roles_aplicacion_resource",
)

api.add_resource(
    PermisosAplicacionResource,
    "/api/v1/aplicaciones/<idAplicacion>/permisos/",
    endpoint="permisos_aplicacion_resource",
)

api.add_resource(
    PermisosRolResource,
    "/api/v1/aplicaciones/<idAplicacion>/roles/<idRol>/permisos/",
    endpoint="permisos_rol_resource",
)
