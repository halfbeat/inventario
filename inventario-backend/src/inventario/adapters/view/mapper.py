import abc

from ..view.model import SistemaInformacionViewDto, ComponenteViewDto


class DomainViewMapper(abc.ABC):

    @abc.abstractmethod
    def to_view(self, domain_entity):
        raise NotImplementedError


class ComponenteViewModekMapper(DomainViewMapper):
    def to_view(self, domain_entity):
        return ComponenteViewDto(
            sistema_id=domain_entity.sistema.sistema_id,
            componente_id=domain_entity.componente_id,
            nombre=domain_entity.nombre,
            observaciones=domain_entity.observaciones,
            git_repo=domain_entity.url_proyecto_git
        )


class SistemaViewModekMapper(DomainViewMapper):
    def __init__(self):
        self.mapper_componente = ComponenteViewModekMapper()

    def to_view(self, domain_entity):
        return SistemaInformacionViewDto(
            sistema_id=domain_entity.sistema_id,
            nombre=domain_entity.nombre,
            observaciones=domain_entity.observaciones,
            componentes=[self.mapper_componente.to_view(c) for c in domain_entity.componentes],
        )
