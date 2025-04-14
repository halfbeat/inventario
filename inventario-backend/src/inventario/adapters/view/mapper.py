import abc

from ..view.model import SistemaInformacionViewDto


class DomainViewMapper(abc.ABC):

    @abc.abstractmethod
    def to_view(self, domain_entity):
        raise NotImplementedError


class SistemaViewModekMapper(DomainViewMapper):
    def to_view(self, domain_entity):
        return SistemaInformacionViewDto(
            sistema_id=domain_entity.sistema_id,
            nombre=domain_entity.nombre,
        )
