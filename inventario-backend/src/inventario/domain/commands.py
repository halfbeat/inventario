# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from typing import Optional


class Command:
    pass


@dataclass
class ObtenerSistema(Command):
    sistema_id: str


@dataclass
class BuscarUnidadesDir3(Command):
    id: Optional[str] = None
    nombre: Optional[str] = None
