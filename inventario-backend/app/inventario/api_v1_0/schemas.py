from marshmallow import fields

from app.ext import ma


class SistemaSchema(ma.Schema):
    sistema_id = fields.String()
    nombre = fields.String()
    observaciones = fields.String(required=False, missing=None)
    unidad_responsable = fields.String(required=False, missing=None)


class ListaPaginable:
    def __init__(self, items, total, page, page_size):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size


class ListaPaginableSistemasSchema(ma.Schema):
    items = fields.List(fields.Nested(SistemaSchema))
    total = fields.Integer()
    page = fields.Integer()
    page_size = fields.Integer()


class UnidadSchema(ma.Schema):
    unidad_id = fields.String(attribute="C_ID_UD_ORGANICA")
    unidad_padre_id = fields.String(attribute="C_ID_DEP_UD_SUPERIOR")
    nombre = fields.String(attribute="C_DNM_UD_ORGANICA")
    nombre_unidad_padre = fields.String(attribute="C_DNM_UD_ORGANICA_SUPERIOR")


class ListaPaginableUnidadesSchema(ma.Schema):
    items = fields.List(fields.Nested(UnidadSchema))
    total = fields.Integer()
    page = fields.Integer()
    page_size = fields.Integer()


class ComponenteSchema(ma.Schema):
    sistema_id = fields.String()
    componente_id = fields.String()
    tipo = fields.String()
    nombre = fields.String()
    observaciones = fields.String(required=False, missing=None)
    git_repo = fields.String(required=False, missing=None)
    tags = fields.List(fields.String(), required=False, missing=[])
