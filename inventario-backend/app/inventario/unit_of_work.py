from __future__ import annotations

import abc
from typing import Set

from app.inventario.asbtract_root import AbstractRoot


class AbstractUnitOfWork(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[AbstractRoot]

    def collect_new_events(self):
        for abstract_root in self.seen:
            while abstract_root.events:
                yield abstract_root.events.pop(0)
