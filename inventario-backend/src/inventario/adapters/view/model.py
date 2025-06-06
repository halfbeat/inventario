from typing import Optional, List

from pydantic import BaseModel, Field, PositiveInt
from typing_extensions import Annotated


class EmpresaViewDto(BaseModel):
    empresa_id: PositiveInt
    cif: str
    nombre: str
    email: str


class EntidadDir3ViewDto(BaseModel):
    unidad_id: str
    nombre: str
    unidad_padre_id: Optional[str] = None,
    nombre_unidad_padre: Optional[str] = None

class ListadoPaginadoEntidadDir3ViewDto(BaseModel):
    items: List[EntidadDir3ViewDto]
    total: int
    page: int
    page_size: int

class TipoComponenteViewDto(BaseModel):
    tipo: str
    nombre: str

class PersonaViewDto(BaseModel):
    persona_id: PositiveInt
    nombre: str
    apellido1: str
    apellido2: str | None = None
    email: str | None = None
    empresa: Optional[EmpresaViewDto] = None


class ComponenteViewDto(BaseModel):
    sistema_id: str
    componente_id: str
    nombre: str
    tipo: str
    observaciones: Optional[str] = None
    git_repo: Optional[str] = None


class SistemaInformacionViewDto(BaseModel):
    sistema_id: str
    nombre: Annotated[str, Field(min_length=4, max_length=50)]
    unidad_responsable: Optional[str] = None
    tecnico_responsable: Optional[str] = None
    observaciones: Optional[str] = None
    # componentes: Optional[List[ComponenteViewDto]] = []


class ResumenSistemaInformacionViewDto(BaseModel):
    sistema_id: str
    nombre: Annotated[str, Field(min_length=4, max_length=50)]
    observaciones: Optional[str] = None
    entidad_responsable: Optional[str] = None


class ListadoPaginadoResumenSistemasViewDto(BaseModel):
    items: List[ResumenSistemaInformacionViewDto]
    total: int
    page: int
    page_size: int
