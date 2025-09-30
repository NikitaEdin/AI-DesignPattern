class Task:
    def execute(self):
        raise NotImplementedError

class LightOn(Task):
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.turn_on()

class Light:
    def turn_on(self):
        print("Light turned on")

class Control:
    def __init__(self):
        self.history = []
    def invoke(self, task):
        self.history.append(task)
        task.execute()

if __name__ == "__main__":
    light = Light()
    control = Control()
    control.invoke(LightOn(light))