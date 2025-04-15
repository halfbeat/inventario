# pylint: disable=too-few-public-methods
from datetime import date
from typing import Optional
from dataclasses import dataclass


class Command:
    pass

@dataclass
class ObtenerSistema(Command):
    sistema_id: str