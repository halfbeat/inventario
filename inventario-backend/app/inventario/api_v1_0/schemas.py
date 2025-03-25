from marshmallow import fields

from app.ext import ma


class SistemaSchema(ma.Schema):
    sistema_id = fields.String()
    nombre = fields.String()
    
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
    
