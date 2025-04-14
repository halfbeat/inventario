from typing import Optional


class Sistema:
    def __init__(self, sistema_id: str, nombre: str, url_proyecto_git: Optional[str],
                 observaciones: Optional[str]) -> None:
        self.sistema_id = sistema_id
        self.nombre = nombre
        self.url_proyecto_git = url_proyecto_git
        self.observaciones = observaciones
        self.events = [] # type List[Event]


class Componente:
    def __init__(self, sistema_id: str, componente_id: str, nombre: str, url_proyecto_git: Optional[str],
                 observaciones: Optional[str]) -> None:
        self.sistema_id = sistema_id
        self.componente_id = componente_id
        self.nombre = nombre
        self.url_proyecto_git = url_proyecto_git
        self.observaciones = observaciones
