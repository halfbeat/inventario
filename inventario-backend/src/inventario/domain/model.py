from typing import Optional, List


class Sistema:
    def __init__(self, sistema_id: str, nombre: str,
                 observaciones: Optional[str], componentes: List["Componente"] = None) -> None:
        if componentes is None:
            componentes = []
        self.sistema_id = sistema_id
        self.nombre = nombre
        self.observaciones = observaciones
        self.events = []  # type List[Event]
        self.componentes = componentes  # type List[Componente]


class Componente:
    def __init__(self, sistema: Optional[Sistema], componente_id: str, nombre: str, url_proyecto_git: Optional[str],
                 observaciones: Optional[str]) -> None:
        self.sistema = sistema
        self.componente_id = componente_id
        self.nombre = nombre
        self.url_proyecto_git = url_proyecto_git
        self.observaciones = observaciones
