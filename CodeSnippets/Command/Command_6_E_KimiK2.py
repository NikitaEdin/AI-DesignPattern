class Light:
    def turn_on(self):
        print("Light is on")
    
    def turn_off(self):
        print("Light is off")

class Action:
    def execute(self):
        pass

class TurnOnAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()

class TurnOffAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()

class Controller:
    def __init__(self):
        self.actions = []
    
    def add_action(self, action):
        self.actions.append(action)
    
    def run(self):
        for action in self.actions:
            action.execute()

if __name__ == "__main__":
    light = Light()
    controller = Controller()
    controller.add_action(TurnOnAction(light))
    controller.add_action(TurnOffAction(light))
    controller.run()