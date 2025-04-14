from typing import Optional


class SistemaInformacion:
    def __init__(self, sistema_id: str, nombre: str, url_proyecto_git: Optional[str],
                 observaciones: Optional[str]) -> None:
        self.sistema_id = sistema_id
        self.nombre = nombre
        self.url_proyecto_git = url_proyecto_git
        self.observaciones = observaciones


if __name__ == "__main__":
    sistema_id = "sistema_id"