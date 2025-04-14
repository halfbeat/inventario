from datetime import date
from typing import Optional
from dataclasses import dataclass


class Command:
    pass

@dataclass
class RegistrarSistemaInformacion(Command):
    sistema_id: str
    nombre: str
    url_proyecto_git: str
    observaciones: str