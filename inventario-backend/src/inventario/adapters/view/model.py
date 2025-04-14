from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt
from typing_extensions import Annotated


class EmpresaViewDto(BaseModel):
    empresa_id: PositiveInt
    cif: str
    nombre: str
    email: str


class EntidadDir3ViewDto(BaseModel):
    codigo_dir3: str
    nombre: str
    codigo_dir3_entidad_padre: Optional[str] = None


class PersonaViewDto(BaseModel):
    persona_id: PositiveInt
    nombre: str
    apellido1: str
    apellido2: str | None = None
    email: str | None = None
    empresa: Optional[EmpresaViewDto] = None


class SistemaInformacionViewDto(BaseModel):
    sistema_id: str
    nombre: Annotated[str, Field(min_length=4, max_length=50)]
    observaciones: Optional[str] = None
    entidad_responsable: Optional[EntidadDir3ViewDto] = None
    responsable_tecnico: Optional[PersonaViewDto] = None
    responsable_funcional: Optional[PersonaViewDto] = None
    fecha_entrada_produccion: Optional[date] = None
    fecha_salida_produccion: Optional[date] = None
