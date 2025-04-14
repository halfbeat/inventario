import abc
from typing import Set

from ..domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Sistema]

    def add(self, product: model.Sistema):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Sistema:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Sistema):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sistema_id) -> model.Sistema:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, sistema_id):
        return self.session.query(model.Sistema).filter_by(sistema_id=sistema_id).first()
