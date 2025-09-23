import abc, time, json, sys

class ModeBase(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def on_enter(self, controller, event=None):
        pass

    @abc.abstractmethod
    def on_exit(self, controller, event=None):
        pass

    @abc.abstractmethod
    def handle(self, controller, event):
        pass

class IdleMode(ModeBase):
    @property
    def name(self): return "idle"
    def on_enter(self, controller, event=None): return
    def on_exit(self, controller, event=None): return
    def handle(self, controller, event):
        if event == "start":
            controller.request_mode_change("running", event)
        else:
            raise ValueError(f"idle cannot handle '{event}'")

class RunningMode(ModeBase):
    @property
    def name(self): return "running"
    def on_enter(self, controller, event=None): controller.counter = 0
    def on_exit(self, controller, event=None): return
    def handle(self, controller, event):
        if event == "pause":
            controller.request_mode_change("paused", event)
        elif event == "stop":
            controller.request_mode_change("idle", event)
        elif event == "tick":
            controller.counter += 1
        else:
            raise ValueError(f"running cannot handle '{event}'")

class PausedMode(ModeBase):
    @property
    def name(self): return "paused"
    def on_enter(self, controller, event=None): return
    def on_exit(self, controller, event=None): return
    def handle(self, controller, event):
        if event == "resume":
            controller.request_mode_change("running", event)
        elif event == "stop":
            controller.request_mode_change("idle", event)
        else:
            raise ValueError(f"paused cannot handle '{event}'")

class Controller:
    def __init__(self, modes, initial="idle"):
        self._registry = {m.name: m for m in modes}
        if initial not in self._registry:
            raise ValueError("initial mode not registered")
        self.current_mode = self._registry[initial]
        self.transitions = {
            "idle": {"running"},
            "running": {"paused", "idle"},
            "paused": {"running", "idle"},
        }
        self.log = []
        self.counter = 0
        self.current_mode.on_enter(self)

    def request_mode_change(self, new_name, event=None):
        if new_name not in self._registry:
            raise ValueError("unknown mode requested")
        allowed = self.transitions.get(self.current_mode.name, set())
        if new_name not in allowed:
            raise RuntimeError(f"transition from {self.current_mode.name} to {new_name} not allowed")
        from_name = self.current_mode.name
        self.current_mode.on_exit(self, event)
        self.current_mode = self._registry[new_name]
        self.current_mode.on_enter(self, event)
        entry = {"time": time.time(), "from": from_name, "to": new_name, "event": event}
        self.log.append(entry)

    def handle_event(self, event):
        try:
            self.current_mode.handle(self, event)
        except Exception as exc:
            raise

    def dump_log(self, filename):
        with open(filename, "w") as f:
            json.dump({"log": self.log, "counter": self.counter, "current": self.current_mode.name}, f, indent=2)

if __name__ == "__main__":
    controller = Controller([IdleMode(), RunningMode(), PausedMode()], initial="idle")
    events = ["start", "tick", "tick", "pause", "resume", "tick", "stop"]
    for ev in events:
        try:
            controller.handle_event(ev)
        except Exception as e:
            print("Error handling", ev, "->", e, file=sys.stderr)
    print("Final mode:", controller.current_mode.name)
    print("Counter:", controller.counter)
    print("Log entries:", len(controller.log))
    controller.dump_log("controller_log.json")