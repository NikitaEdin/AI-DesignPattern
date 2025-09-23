class LightController:
    def __init__(self):
        self.current = RedLight()
    def transition(self):
        self.current.transition(self)
    def show(self):
        print(self.current.color)

class RedLight:
    color = "Red"
    def transition(self, ctrl):
        ctrl.current = GreenLight()

class GreenLight:
    color = "Green"
    def transition(self, ctrl):
        ctrl.current = YellowLight()

class YellowLight:
    color = "Yellow"
    def transition(self, ctrl):
        ctrl.current = RedLight()

if __name__ == "__main__":
    ctrl = LightController()
    for _ in range(6):
        ctrl.show()
        ctrl.transition()