import abc
from typing import Set, Optional

from .database.mapper import SistemaInformaciomDomainModelMapper
from .database.model import SistemaInformacionModelDto
from ..domain import model


class SistemaRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Sistema]

    def add(self, product: model.Sistema):
        self._add(product)
        self.seen.add(product)

    def get(self, sistema_id) -> model.Sistema:
        sistema = self._get(sistema_id)
        if sistema:
            self.seen.add(sistema)
        return sistema

    @abc.abstractmethod
    def _add(self, product: model.Sistema):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sistema_id) -> model.Sistema:
        raise NotImplementedError


class SqlAlchemyRepository(SistemaRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.mapper = SistemaInformaciomDomainModelMapper()

    def _add(self, product):
        self.session.add(product)

    def _get(self, sistema_id):
        model_dto: Optional[SistemaInformacionModelDto] = self.session.query(SistemaInformacionModelDto).filter_by(
            sistema_id=sistema_id).first()
        return self.mapper.to_domain(model_dto)
