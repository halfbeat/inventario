from flask import abort

from app.inventario.api_v1_0.schemas import (
    SistemaSchema,
    ListaPaginableSistemasSchema, UnidadSchema, ListaPaginableUnidadesSchema, ComponenteSchema,
)
from app.inventario.models import (
    SistemaInformacionModelDto, UnidadDir3ModelDto, ComponenteModelDto,
)

sistema_schema = SistemaSchema()
sistemas_schema = ListaPaginableSistemasSchema()
unidad_schema = UnidadSchema()
unidades_schema = ListaPaginableUnidadesSchema()
componentes_schema = ComponenteSchema(many=True)
componente_schema = ComponenteSchema()

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

    @classmethod
    def get_componentes_sistema(cls, sistema_id):
        sistema = SistemaInformacionModelDto.get_by_id(sistema_id=sistema_id)
        if not sistema:
            abort(404, "Sistema no encontrada")
        return componentes_schema.dump(sistema.componentes)

    @classmethod
    def get_componente_sistema(cls, sistema_id, componente_id):
        componente = ComponenteModelDto.get_by_id(sistema_id=sistema_id, componente_id=componente_id)
        if not componente:
            abort(404, "Componente no encontrada")
        return componente_schema.dump(componente)


class UnidadDir3Service:
    @staticmethod
    def buscar_unidades(unidad_id: str = None, nombre: str = None):
        print(unidad_id, nombre)
        unidades = UnidadDir3ModelDto.query(page=1, page_size=100, unidad_id=unidad_id, nombre=nombre)

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

    @classmethod
    def obtener_unidad(cls, unidad_id):
        unidad = UnidadDir3ModelDto.get_by_id(C_ID_UD_ORGANICA=unidad_id)
        if not unidad:
            abort(404, "Unidad no encontrada")
        return unidad_schema.dump(unidad)
