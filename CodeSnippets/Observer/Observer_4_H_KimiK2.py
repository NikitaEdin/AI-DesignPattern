import weakref
from typing import Set, Any, Callable

class _Notifier:
    __slots__ = ("_targets",)

    def __init__(self) -> None:
        self._targets: Set[weakref.ref] = set()

    def attach(self, target: Callable) -> None:
        ref = weakref.ref(target, self._targets.remove)
        self._targets.add(ref)

    def detach(self, target: Callable) -> None:
        for ref in list(self._targets):
            if ref() is target:
                self._targets.remove(ref)

    def _emit(self, *args, **kwargs) -> None:
        for ref in list(self._targets):
            callback = ref()
            if callback:
                try:
                    callback(*args, **kwargs)
                except Exception:
                    pass


class DataHub:
    def __init__(self) -> None:
        self._notifier = _Notifier()
        self._data: dict[str, Any] = {}

    def monitor(self, callback: Callable) -> None:
        self._notifier.attach(callback)

    def ignore(self, callback: Callable) -> None:
        self._notifier.detach(callback)

    def update(self, key: str, value: Any) -> None:
        if self._data.get(key) != value:
            self._data[key] = value
            self._notifier._emit(key, value)

    def get(self, key: str) -> Any:
        return self._data.get(key)


class Dashboard:
    def __init__(self, hub: DataHub) -> None:
        self.hub = hub
        self.cache: dict[str, Any] = {}

    def start(self) -> None:
        self.hub.monitor(self._sync)

    def stop(self) -> None:
        self.hub.ignore(self._sync)

    def _sync(self, key: str, value: Any) -> None:
        self.cache[key] = value
        self.display(key, value)

    def display(self, key: str, value: Any) -> None:
        print(f"[Dash] {key} -> {value}")


class Logger:
    def __init__(self, hub: DataHub) -> None:
        self.hub = hub

    def start(self) -> None:
        self.hub.monitor(self._log)

    def stop(self) -> None:
        self.hub.ignore(self._log)

    def _log(self, key: str, value: Any) -> None:
        print(f"[Log] {key} updated to {value}")


if __name__ == "__main__":
    hub = DataHub()
    dash = Dashboard(hub)
    logger = Logger(hub)

    dash.start()
    logger.start()

    hub.update("temp", 21.5)
    hub.update("temp", 22.0)
    hub.update("humi", 60)

    dash.stop()
    hub.update("temp", 23.0)