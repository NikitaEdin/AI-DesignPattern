from abc import ABC, abstractmethod

class Device:
    def __init__(self):
        self._active = False

    def activate(self):
        if not self._active:
            print("Device activated")
            self._active = True
        else:
            print("Device already active")

    def deactivate(self):
        if self._active:
            print("Device deactivated")
            self._active = False
        else:
            print("Device already inactive")

    def is_active(self):
        return self._active

class Executable(ABC):
    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def reverse(self):
        pass

class ActivateAction(Executable):
    def __init__(self, device):
        self.device = device

    def perform(self):
        self.device.activate()

    def reverse(self):
        if self.device.is_active():
            self.device.deactivate()
        else:
            print("Cannot reverse: device inactive")

class DeactivateAction(Executable):
    def __init__(self, device):
        self.device = device

    def perform(self):
        self.device.deactivate()

    def reverse(self):
        if not self.device.is_active():
            self.device.activate()
        else:
            print("Cannot reverse: device active")

class RemoteControl:
    def __init__(self):
        self._history = []
        self._pending = None

    def assign_action(self, action):
        self._pending = action

    def execute(self):
        if self._pending:
            self._pending.perform()
            self._history.append(self._pending)
            self._pending = None
        else:
            print("No action assigned")

    def reverse_last(self):
        if self._history:
            last = self._history.pop()
            last.reverse()
        else:
            print("No actions to reverse")

if __name__ == "__main__":
    device = Device()
    remote = RemoteControl()
    activate = ActivateAction(device)
    deactivate = DeactivateAction(device)
    remote.assign_action(activate)
    remote.execute()
    remote.assign_action(deactivate)
    remote.execute()
    remote.reverse_last()
    remote.reverse_last()