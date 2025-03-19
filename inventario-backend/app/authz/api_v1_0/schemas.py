from marshmallow import fields
from app.ext import ma


class AplicacionSchema(ma.Schema):
    aplicacion_id = fields.String()
    nombre = fields.String()
    
class RolAplicacionSchema(ma.Schema):
    aplicacion_id = fields.String(dump_only=True)
    rol_id = fields.String(dump_only=True)
    nombre = fields.String()    
    
class PermisoAplicacionSchema(ma.Schema):
    aplicacion_id = fields.String(dump_only=True)
    permiso_id = fields.String(dump_only=True)
    nombre = fields.String()     
    
class PermisoRolSchema(ma.Schema):
    permiso_id = fields.String(dump_only=True)


class ListaPaginable:
    def __init__(self, items, total, page, page_size):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size

class ListaPaginableAplicacionesSchema(ma.Schema):
    items = fields.List(fields.Nested(AplicacionSchema))
    total = fields.Integer()
    page = fields.Integer()
    page_size = fields.Integer()
    
class ListaPaginableRolesAplicacionSchema(ma.Schema):
    items = fields.List(fields.Nested(RolAplicacionSchema))
    total = fields.Integer()
    page = fields.Integer()
    page_size = fields.Integer()      
    
class ListaPaginableRolesSchema(ma.Schema):
    items = fields.List(fields.String())
    total = fields.Integer()
    page = fields.Integer()
    page_size = fields.Integer()    
    
class ListaPaginablePermisosAplicacionSchema(ma.Schema):
    items = fields.List(fields.Nested(PermisoAplicacionSchema))
    total = fields.Integer()
    page = fields.Integer()
    page_size = fields.Integer()    
        
    
class ListaPaginablePermisosRolSchema(ma.Schema):
    items = fields.List(fields.String())
    total = fields.Integer()
    page = fields.Integer()
    page_size = fields.Integer()    
    