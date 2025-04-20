from typing import Optional, List

from . import events

class ComponenteNoEncontrado(Exception):
    pass

class ComponenteExistente(Exception):
    pass

class NombreSistemaRequerido(Exception):
    pass


class IdComponenteRequerido(Exception):
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

    def agregar_componente(self, componente_id, nombre, tipo, url_proyecto_git = None, observaciones = None):
        if componente_id is None:
            raise IdComponenteRequerido()
        if nombre is None:
            raise NombreSistemaRequerido()
        componente_existente = next(
            iter([componente for componente in self.componentes if componente.componente_id == componente_id]), None)
        if componente_existente is not None:
            raise ComponenteExistente()
        nuevo_componente = Componente(self, componente_id, nombre, tipo, url_proyecto_git, observaciones)
        self.componentes.append(nuevo_componente)
        self.events.append(events.SistemaModificado(self.sistema_id))

        return nuevo_componente


class Componente:
    def __init__(self, sistema: Optional[Sistema], componente_id: str, nombre: str, tipo: str,
                 url_proyecto_git: Optional[str],
                 observaciones: Optional[str]) -> None:
        self.sistema = sistema
        self.componente_id = componente_id
        self.nombre = nombre
        self.tipo = tipo
        self.url_proyecto_git = url_proyecto_git
        self.observaciones = observaciones

    def modificar(self, nombre, tipo, url_proyecto_git = None, observaciones = None ):
        if nombre is None:
            raise NombreSistemaRequerido()

        self.nombre = nombre
        self.tipo = tipo
        self.url_proyecto_git = url_proyecto_git
        self.observaciones = observaciones

        self.sistema.events.append(events.SistemaModificado(self.sistema.sistema_id))
