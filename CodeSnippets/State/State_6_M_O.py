from abc import ABC, abstractmethod

class ModeBase(ABC):
    @abstractmethod
    def handle(self, engine, command):
        pass

class Idle(ModeBase):
    def handle(self, engine, command):
        if command == "start":
            engine.set_mode(Running())
            return "Transitioned to running."
        if command == "status":
            return "Idle: ready."
        raise ValueError(f"Unsupported command '{command}' in idle.")

class Running(ModeBase):
    def handle(self, engine, command):
        if command == "pause":
            engine.set_mode(Paused())
            return "Paused."
        if command == "stop":
            engine.set_mode(Idle())
            return "Stopped and idling."
        if command == "status":
            return "Running: processing."
        raise ValueError(f"Unsupported command '{command}' while running.")

class Paused(ModeBase):
    def handle(self, engine, command):
        if command == "resume":
            engine.set_mode(Running())
            return "Resumed running."
        if command == "stop":
            engine.set_mode(Idle())
            return "Stopped from paused."
        if command == "status":
            return "Paused: waiting."
        raise ValueError(f"Unsupported command '{command}' while paused.")

class Engine:
    def __init__(self, initial=None):
        self._history = []
        self.current = initial or Idle()
    def set_mode(self, new_mode):
        if not isinstance(new_mode, ModeBase):
            raise TypeError("new_mode must implement ModeBase")
        self._history.append(self.current)
        self.current = new_mode
    def revert_mode(self):
        if not self._history:
            raise RuntimeError("No previous mode to revert to")
        self.current = self._history.pop()
    def request(self, command):
        try:
            return self.current.handle(self, command)
        except Exception as exc:
            raise

if __name__ == "__main__":
    engine = Engine()
    print(engine.request("status"))
    print(engine.request("start"))
    print(engine.request("status"))
    print(engine.request("pause"))
    print(engine.request("status"))
    try:
        print(engine.request("invalid"))
    except Exception as e:
        print("Error handled:", e)
    engine.revert_mode()
    print("Reverted. Current status:", engine.request("status"))
    print(engine.request("stop"))