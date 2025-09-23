from abc import ABC, abstractmethod
class Action(ABC):
    @abstractmethod
    def execute(self): pass
class Device:
    def __init__(self): self.state='off'
    def turn_on(self): self.state='on'
    def turn_off(self): self.state='off'
class TurnOnAction(Action):
    def __init__(self, device): self.device=device
    def execute(self): self.device.turn_on()
class TurnOffAction(Action):
    def __init__(self, device): self.device=device
    def execute(self): self.device.turn_off()
class Controller:
    def __init__(self): self._action=None
    def set(self, action): self._action=action
    def trigger(self):
        if self._action: self._action.execute()
if __name__=='__main__':
    d=Device(); on=TurnOnAction(d); off=TurnOffAction(d); c=Controller()
    c.set(on); c.trigger(); print(d.state)
    c.set(off); c.trigger(); print(d.state)