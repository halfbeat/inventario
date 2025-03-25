from flask import abort

from app.inventario.api_v1_0.schemas import (
    SistemaSchema,
    ListaPaginableSistemasSchema,
)
from app.inventario.models import (
    SistemaInformacionModelDto,
)

sistema_schema = SistemaSchema()
sistemas_schema = ListaPaginableSistemasSchema()


class SistemaService:

    @staticmethod
    def altaAplicacion(aplicacion_json: dict):
        aplicacion_json = sistema_schema.load(aplicacion_json)
        aplicacion_existente = SistemaInformacionModelDto.get_by_id(
            aplicacion_json["sistema_id"]
        )
        if aplicacion_existente:
            abort(409, "El sistema ya existe")
        aplicacion = SistemaInformacionModelDto(**aplicacion_json)
        aplicacion.save()

    @staticmethod
    def get_aplicaciones(page: int, page_size: int, limitar_a_aplicaciones: list = None):
        sistemas = SistemaInformacionModelDto.query_sistemas(page, page_size,
                                                             limitar_a_aplicaciones=limitar_a_aplicaciones
                                                             )
        #aplicaciones = AplicacionModelDto.get_page(page , page_size)
        result = sistemas_schema.dump(
            {
                "items": sistemas.items,
                "total": sistemas.total,
                "page": page,
                "page_size": page_size,
            },
            many=False,
        )
        return result

    @staticmethod
    def get_sistema(sistema_id: str):
        sistema = SistemaInformacionModelDto.get_by_id(sistema_id=sistema_id)
        if not sistema:
            abort(404, "Sistema no encontrada")
        return sistema_schema.dump(sistema)
