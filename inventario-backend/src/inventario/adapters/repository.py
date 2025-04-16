import abc
from typing import Set, Optional

from .database.mapper import SistemaInformaciomDomainModelMapper
from .database.model import SistemaInformacionModelDto
from ..domain import model


class SistemaRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Sistema]

    def add(self, sistema: model.Sistema):
        self._add(sistema)
        self.seen.add(sistema)

    def get(self, sistema_id) -> model.Sistema:
        sistema = self._get(sistema_id)
        if sistema:
            self.seen.add(sistema)
        return sistema

    def update(self, sistema: model.Sistema):
        self._update(sistema)
        self.seen.add(sistema)

    @abc.abstractmethod
    def _add(self, sistema: model.Sistema):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sistema_id) -> model.Sistema:
        raise NotImplementedError

    @abc.abstractmethod
    def _update(self, sistema: model.Sistema):
        raise NotImplementedError


class SqlAlchemyRepository(SistemaRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.mapper = SistemaInformaciomDomainModelMapper()

    def _add(self, sistema):
        self.session.add(sistema)

    def _get(self, sistema_id):
        model_dto: Optional[SistemaInformacionModelDto] = self.session.query(SistemaInformacionModelDto).filter_by(
            sistema_id=sistema_id).first()
        return self.mapper.to_domain(model_dto)

    def _update(self, sistema: model.Sistema):
        model_dto = self.mapper.to_model(sistema)
        self.session.merge(model_dto)
