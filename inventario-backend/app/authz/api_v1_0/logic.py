from flask import abort

from app.authz.api_v1_0.schemas import (
    AplicacionSchema,
    ListaPaginableAplicacionesSchema,
)
from app.authz.models import (
    SistemaInformacionModelDto,
)

aplicacion_schema = AplicacionSchema()
aplicaciones_schema = ListaPaginableAplicacionesSchema()


class AplicacionService:

    @staticmethod
    def altaAplicacion(aplicacion_json: dict):
        aplicacion_json = aplicacion_schema.load(aplicacion_json)
        aplicacion_existente = SistemaInformacionModelDto.get_by_id(
            aplicacion_json["aplicacion_id"]
        )
        if aplicacion_existente:
            abort(409, "La aplicación ya existe")
        aplicacion = SistemaInformacionModelDto(**aplicacion_json)
        aplicacion.save()

    @staticmethod
    def get_aplicaciones(page: int, page_size: int, limitar_a_aplicaciones: list = None):
        aplicaciones = SistemaInformacionModelDto.query_aplicaciones(page, page_size,
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
        aplicacion = SistemaInformacionModelDto.get_by_id(aplicacion_id=idAplicacion)
        if not aplicacion:
            abort(404, "Aplicación no encontrada")
        return aplicacion_schema.dump(aplicacion)
