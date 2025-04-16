import abc

from sqlalchemy import Double

from ...domain import model
from ...adapters.database import model as dbmodel

class DomainModelMapper(abc.ABC):

    @abc.abstractmethod
    def to_domain(self, model_entity):
        raise NotImplementedError

    @abc.abstractmethod
    def to_model(self, domain_entity):
        raise NotImplementedError


class ComponenteModelMapper(DomainModelMapper):
    def to_domain(self, model_entity):
        if model_entity is None:
            return None

        return model.Componente(
            sistema=None,
            componente_id=model_entity.componente_id,
            nombre=model_entity.nombre,
            url_proyecto_git=model_entity.url_proyecto_git,
            observaciones=model_entity.observaciones
        )

    def to_model(self, domain_entity):
        raise NotImplementedError


class SistemaInformaciomDomainModelMapper(DomainModelMapper):
    def __init__(self):
        self.componenete_mapper = ComponenteModelMapper()

    def to_domain(self, model_entity):
        if model_entity is None:
            return None
        sistema = model.Sistema(
            sistema_id=model_entity.sistema_id,
            nombre=model_entity.nombre,
            unidad_responsable=model_entity.unidad_responsable,
            tecnico_responsable=model_entity.tecnico_responsable,
            observaciones=model_entity.observaciones,
            componentes=[self.componenete_mapper.to_domain(componente_model_entity) for componente_model_entity in
                         model_entity.componentes]
        )

        for componente in sistema.componentes:
            componente.sistema = sistema

        return sistema

    def to_model(self, domain_entity):
        if domain_entity is None:
            return None

        model_dto = dbmodel.SistemaInformacionModelDto(
            sistema_id=domain_entity.sistema_id,
            nombre=domain_entity.nombre,
            unidad_responsable=domain_entity.unidad_responsable,
            tecnico_responsable=domain_entity.tecnico_responsable,
            observaciones=domain_entity.observaciones
        )

        return model_dto
