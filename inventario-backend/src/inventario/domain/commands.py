# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from typing import Optional


class Command:
    pass


@dataclass
class ObtenerSistema(Command):
    sistema_id: str


@dataclass
class RegistrarSistema(Command):
    sistema_id: str
    nombre: Optional[str] = None
    unidad_responsable: Optional[str] = None
    tecnico_responsable: Optional[str] = None
    observaciones: Optional[str] = None

@dataclass
class ModificarSistema(Command):
    sistema_id: str
    nombre: Optional[str] = None
    unidad_responsable: Optional[str] = None
    tecnico_responsable: Optional[str] = None
    observaciones: Optional[str] = None

@dataclass
class ModificarComponente(Command):
    sistema_id: str
    componente_id: str
    nombre: str
    tipo: str
    url_proyecto_git: Optional[str] = None
    observaciones: Optional[str] = None