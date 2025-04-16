# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from typing import Optional

from ..adapters.view.model import SistemaInformacionViewDto


class Command:
    pass


@dataclass
class ObtenerSistema(Command):
    sistema_id: str


@dataclass
class ModificarSistema(Command):
    sistema_id: str
    nombre: Optional[str] = None
    unidad_responsable: Optional[str] = None
    tecnico_responsable: Optional[str] = None
    observaciones: Optional[str] = None
