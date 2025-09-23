from abc import ABC, abstractmethod

class Light:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def get_state(self):
        return self.is_on

class Thermostat:
    def __init__(self, temp=20):
        self.temp = temp

    def set_temp(self, t):
        if t < 0:
            raise ValueError("Temperature cannot be negative")
        self.temp = t

    def get_temp(self):
        return self.temp

class Action(ABC):
    @abstractmethod
    def perform(self):
        pass

    def undo(self):
        pass

class LightOn(Action):
    def __init__(self, light):
        self.light = light
        self.previous_state = light.get_state()

    def perform(self):
        self.light.turn_on()

    def undo(self):
        if self.previous_state:
            self.light.turn_on()
        else:
            self.light.turn_off()

class LightOff(Action):
    def __init__(self, light):
        self.light = light
        self.previous_state = light.get_state()

    def perform(self):
        self.light.turn_off()

    def undo(self):
        if self.previous_state:
            self.light.turn_on()
        else:
            self.light.turn_off()

class ThermostatSet(Action):
    def __init__(self, thermostat, new_temp):
        self.thermostat = thermostat
        self.previous_temp = thermostat.get_temp()
        self.new_temp = new_temp

    def perform(self):
        self.thermostat.set_temp(self.new_temp)

    def undo(self):
        self.thermostat.set_temp(self.previous_temp)

class CompositeAction(Action):
    def __init__(self, actions):
        self.actions = actions[:]

    def perform(self):
        for action in self.actions:
            action.perform()

    def undo(self):
        for action in reversed(self.actions):
            action.undo()

class Controller:
    def __init__(self):
        self.history = []

    def execute(self, action):
        try:
            action.perform()
            self.history.append(action)
        except Exception as e:
            raise RuntimeError(f"Failed to perform action: {e}")

    def undo_last(self):
        if self.history:
            last_action = self.history.pop()
            last_action.undo()
        else:
            raise RuntimeError("No actions to undo")

if __name__ == "__main__":
    light = Light()
    thermostat = Thermostat(72)
    turn_on = LightOn(light)
    adjust_temp = ThermostatSet(thermostat, 75)
    sequence = CompositeAction([turn_on, adjust_temp])
    ctrl = Controller()
    ctrl.execute(sequence)
    print(f"After sequence: Light {light.get_state()}, Temp {thermostat.get_temp()}")
    ctrl.undo_last()
    print(f"After undo: Light {light.get_state()}, Temp {thermostat.get_temp()}")
    try:
        invalid_adjust = ThermostatSet(thermostat, -5)
        ctrl.execute(invalid_adjust)
    except RuntimeError as e:
        print(f"Handled error: {e}")