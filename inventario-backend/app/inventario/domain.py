from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt
from typing_extensions import Annotated


class Empresa(BaseModel):
    empresa_id: PositiveInt
    cif: str
    nombre: str
    email: str


class EntidadDIR3(BaseModel):
    codigo_dir3: str
    nombre: str
    codigo_dir3_entidad_padre: Optional[str]


class Persona(BaseModel):
    persona_id: PositiveInt
    nombre: str
    apellido1: str
    apellido2: str | None = None
    email: str | None = None
    empresa: Optional[Empresa] = None


class SistemaInformacion(BaseModel):
    sistema_id: str
    nombre: Annotated[str, Field(min_length=4, max_length=50)]
    observaciones: Optional[str] = None
    entidad_responsable: EntidadDIR3
    responsable_tecnico: Optional[Persona] = None
    responsable_funcional: Optional[Persona] = None
    fecha_entrada_produccion: Optional[date] = None
    fecha_salida_produccion: Optional[date] = None


if __name__ == '__main__':
    test_data = {
        'sistema_id': 'ADNA',
        'nombre': 'Ayudas al nacimiento',
        'observaciones': '<p>No me gusta nada</p>',
        'entidad_responsable': {

        }
    }

    sistema = SistemaInformacion(**test_data)
    print(sistema.model_dump())
