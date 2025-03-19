from flask import abort
from app.authz.api_v1_0.schemas import (
    AplicacionSchema,
    ListaPaginableAplicacionesSchema,
)
from app.authz.models import (
    AplicacionModelDto,
    AsignacionRolModelDto,
    PermisosRolModelDto,
)

aplicacion_schema = AplicacionSchema()
aplicaciones_schema = ListaPaginableAplicacionesSchema()


class AplicacionService:

    @staticmethod
    def altaAplicacion(aplicacion_json: dict):
        aplicacion_json = aplicacion_schema.load(aplicacion_json)
        aplicacion_existente = AplicacionModelDto.get_by_id(
            aplicacion_json["aplicacion_id"]
        )
        if aplicacion_existente:
            abort(409, "La aplicación ya existe")
        aplicacion = AplicacionModelDto(**aplicacion_json)
        aplicacion.save()

    @staticmethod
    def get_aplicaciones(page: int, page_size: int, limitar_a_aplicaciones: list = None):
        aplicaciones = AplicacionModelDto.query_aplicaciones(page, page_size,
            limitar_a_aplicaciones=limitar_a_aplicaciones
        )
        #aplicaciones = AplicacionModelDto.get_page(page , page_size)
        result = aplicaciones_schema.dump(
            {
                "items": aplicaciones.items,
                "total": aplicaciones.total,
                "page": page,
                "page_size": page_size,
            },
            many=False,
        )
        return result

    @staticmethod
    def get_aplicacion(idAplicacion: str):
        aplicacion = AplicacionModelDto.get_by_id(aplicacion_id = idAplicacion)
        if not aplicacion:
            abort(404, "Aplicación no encontrada")
        return aplicacion_schema.dump(aplicacion)


class SecurityService:
    @staticmethod
    def has_permission(
        principal: str, aplicacion: str, permiso: str, ambito: str = None
    ) -> bool:
        # busco todos los permisos del principal para la aplicación
        asignaciones = AsignacionRolModelDto.filter(aplicacion, principal)
        permisos = []
        for asignacion in asignaciones:
            if asignacion.ambito is None or asignacion.ambito == ambito:
                permisos.extend(
                    [
                        permiso.permiso_id
                        for permiso in PermisosRolModelDto.simple_filter(
                            rol_id=asignacion.rol_id, aplicacion_id=aplicacion
                        )
                    ]
                )

        return permiso in permisos
    
    @staticmethod
    def get_ambitos(aplicacion: str, principal: str) -> list[str]:
        asignaciones = AsignacionRolModelDto.filter(aplicacion, principal)
        ambitos = [a.ambito for a in asignaciones if a.ambito is not None]
        return ambitos

        
