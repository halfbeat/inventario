# pylint: disable=too-few-public-methods
from dataclasses import dataclass


class Command:
    pass


@dataclass
class ObtenerSistema(Command):
    sistema_id: str

