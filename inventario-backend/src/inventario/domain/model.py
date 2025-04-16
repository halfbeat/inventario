from typing import Optional, List

from . import events


class NombreSistemaRequerido(Exception):
    pass


class Sistema:
    def __init__(self, sistema_id: str, nombre: str,
                 unidad_responsable: Optional[str], tecnico_responsable: Optional[str],
                 observaciones: Optional[str], componentes: List["Componente"] = None) -> None:
        if componentes is None:
            componentes = []
        self.sistema_id = sistema_id
        self.nombre = nombre
        self.unidad_responsable = unidad_responsable
        self.tecnico_responsable = tecnico_responsable
        self.observaciones = observaciones
        self.events = []  # type List[Event]
        self.componentes = componentes  # type List[Componente]

    def modificar(self, nombre, unidad_responsable, tecnico_responsable, observaciones):
        if nombre is None:
            raise NombreSistemaRequerido()

        self.nombre = nombre
        self.unidad_responsable = unidad_responsable
        self.tecnico_responsable = tecnico_responsable
        self.observaciones = observaciones

        self.events.append(events.SistemaModificado(self.sistema_id))


class Componente:
    def __init__(self, sistema: Optional[Sistema], componente_id: str, nombre: str, url_proyecto_git: Optional[str],
                 observaciones: Optional[str]) -> None:
        self.sistema = sistema
        self.componente_id = componente_id
        self.nombre = nombre
        self.url_proyecto_git = url_proyecto_git
        self.observaciones = observaciones
