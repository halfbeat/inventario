from abc import ABC


class AbstractRoot(ABC):
    events = [] # type List[events.Event]

    def collect_new_events(self):
        while self.events:
            yield self.events.pop(0)
