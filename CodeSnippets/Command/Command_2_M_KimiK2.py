import time

class Task:
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

class LightOn(Task):
    def __init__(self, device):
        self.device = device
    def execute(self):
        self.device.switch(True)
    def undo(self):
        self.device.switch(False)

class HeaterOn(Task):
    def __init__(self, device):
        self.device = device
    def execute(self):
        self.device.set_temp(22)
    def undo(self):
        self.device.set_temp(16)

class AutomationManager:
    def __init__(self):
        self.history = []
    def schedule(self, task):
        try:
            task.execute()
            self.history.append(task)
        except:
            pass
    def revert_last(self):
        if self.history:
            self.history.pop().undo()

class Light:
    def __init__(self):
        self.is_on = False
    def switch(self, on):
        self.is_on = on
        print(f'Light {"on" if on else "off"}')
class Heater:
    def __init__(self):
        self.temp = 16
    def set_temp(self, t):
        self.temp = t
        print(f'Heater set to {t}°C')

if __name__ == '__main__':
    m = AutomationManager()
    light = Light()
    heater = Heater()
    m.schedule(LightOn(light))
    m.schedule(HeaterOn(heater))
    m.revert_last()