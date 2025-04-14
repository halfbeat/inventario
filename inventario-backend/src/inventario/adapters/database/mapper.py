import abc

from ...domain import model


class DaomainModelMapper(abc.ABC):

    @abc.abstractmethod
    def to_domain(self, model_entity):
        raise NotImplementedError


class ComponenteModelMapper(DaomainModelMapper):
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


class SistemaInformaciomDomainModelMapper:
    def __init__(self):
        self.componenete_mapper = ComponenteModelMapper()

    def to_domain(self, model_entity):
        if model_entity is None:
            return None
        sistema = model.Sistema(
            sistema_id=model_entity.sistema_id,
            nombre=model_entity.nombre,
            observaciones=model_entity.observaciones,
            componentes=[self.componenete_mapper.to_domain(componente_model_entity) for componente_model_entity in
                         model_entity.componentes]
        )

        for componente in sistema.componentes:
            componente.sistema = sistema

        return sistema
