from flask import abort

from app.inventario.api_v1_0.schemas import (
    SistemaSchema,
    ListaPaginableSistemasSchema, UnidadSchema, ListaPaginableUnidadesSchema,
)
from app.inventario.models import (
    SistemaInformacionModelDto, UnidadDir3ModelDo,
)

sistema_schema = SistemaSchema()
sistemas_schema = ListaPaginableSistemasSchema()
unidad_schema = UnidadSchema()
unidades_schema = ListaPaginableUnidadesSchema()


class SistemaInformacionService:

    @staticmethod
    def alta_sistema(sistema_json: dict):
        sistema_json = sistema_schema.load(sistema_json)
        sistema_existente = SistemaInformacionModelDto.get_by_id(
            sistema_id=sistema_json["sistema_id"]
        )
        if sistema_existente:
            abort(409, "El sistema ya existe")
        sistema = SistemaInformacionModelDto(**sistema_json)
        print(sistema)
        sistema.save()

    @staticmethod
    def modificar_sistema(sistema_id: str, sistema_json: dict):
        sistema_json["sistema_id"] = sistema_id
        sistema_json = sistema_schema.load(sistema_json)
        sistema_existente = SistemaInformacionModelDto.get_by_id(
            sistema_id=sistema_json["sistema_id"]
        )
        if not sistema_existente:
            abort(404, "El sistema no existe")
        sistema_existente.update(**sistema_json)
        sistema_existente.save()

    @staticmethod
    def get_sistemas(page: int, page_size: int, limitar_a_aplicaciones: list = None):
        sistemas = SistemaInformacionModelDto.query_sistemas(page, page_size,
                                                             limitar_a_aplicaciones=limitar_a_aplicaciones
                                                             )
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


class UnidadDir3Service:
    @staticmethod
    def buscar_unidades(unidad_id: str = None, nombre: str = None):
        print(unidad_id, nombre)
        unidades = UnidadDir3ModelDo.query(page=1, page_size=100, unidad_id=unidad_id, nombre=nombre)

        print(unidades)
        result = unidades_schema.dump(
            {
                "items": unidades.items,
                "total": unidades.total,
                "page": 1,
                "page_size": 100,
            },
            many=False,
        )
        print(result)
        return result
