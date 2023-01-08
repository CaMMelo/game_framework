from dataclasses import dataclass, field
from typing import Callable, Hashable


@dataclass
class EventPublisher:
    _subscriptions: dict[str, dict[Hashable, Callable]] = field(
        init=False, default_factory=dict
    )

    def subscribe(self, event: str, listener: Hashable, callback: Callable):
        if event not in self._subscriptions:
            self._subscriptions[event] = {}
        self._subscriptions[event][listener] = callback

    def unsubscribe(self, listener: Hashable, events: list[str] = None):
        for event in events or self._subscriptions.keys():
            if listener in self._subscriptions[event]:
                del self._subscriptions[event][listener]

    def publish(self, event: str, *args, **kwargs):
        if event not in self._subscriptions:
            return
        for _, handler_method in list(self._subscriptions[event].items()):
            handler_method(*args, **kwargs)
