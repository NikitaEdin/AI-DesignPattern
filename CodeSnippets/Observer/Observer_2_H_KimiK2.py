from __future__ import annotations
import weakref
from typing import Protocol, Any, List, Dict, Set


class _Listener(Protocol):
    def update(self, source: object, event: str, data: Any) -> None: ...


class _Subject:
    def __init__(self):
        self._listeners: Dict[str, Set[weakref.ref]] = {}

    def attach(self, listener: _Listener, events: List[str] | None = None) -> None:
        ref = weakref.ref(listener, lambda _: self._cleanup(listener))
        if events is None:
            events = ["*"]
        for ev in events:
            self._listeners.setdefault(ev, set()).add(ref)

    def detach(self, listener: _Listener, events: List[str] | None = None) -> None:
        if events is None:
            events = list(self._listeners)
        for ev in events:
            self._listeners.get(ev, set()).discard(weakref.ref(listener))

    def _notify(self, event: str, data: Any = None) -> None:
        for ref in list(self._listeners.get(event, set()) | self._listeners.get("*", set())):
            if (obj := ref()) is not None:
                try:
                    obj.update(self, event, data)
                except Exception:
                    pass

    def _cleanup(self, dead_ref: _Listener) -> None:
        for ev, refs in self._listeners.items():
            refs.discard(weakref.ref(dead_ref))


class Engine(_Subject):
    def __init__(self):
        super().__init__()
        self._speed = 0

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value: int) -> None:
        old, self._speed = self._speed, max(0, value)
        if old != self._speed:
            self._notify("speed_change", {"old": old, "new": self._speed})


class Dashboard:
    def __init__(self, engine: Engine):
        self.engine = engine
        engine.attach(self, ["speed_change"])

    def update(self, source: object, event: str, data: Any) -> None:
        if event == "speed_change":
            print(f"Dashboard shows {data['new']} km/h")


class Logger:
    def update(self, source: object, event: str, data: Any) -> None:
        print(f"[LOG] {event}: {data}")


if __name__ == "__main__":
    e = Engine()
    d = Dashboard(e)
    l = Logger()
    e.attach(l)
    e.speed = 50
    e.speed = 60
    e.detach(l)
    e.speed = 70