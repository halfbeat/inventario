from typing import Optional, List

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


class ComponenteViewDto(BaseModel):
    sistema_id: str
    componente_id: str
    nombre: str
    observaciones: Optional[str] = None
    git_repo: Optional[str] = None


class SistemaInformacionViewDto(BaseModel):
    sistema_id: str
    nombre: Annotated[str, Field(min_length=4, max_length=50)]
    unidad_responsable: Optional[str] = None
    tecnico_responsable: Optional[str] = None
    observaciones: Optional[str] = None
    componentes: Optional[List[ComponenteViewDto]] = []


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
