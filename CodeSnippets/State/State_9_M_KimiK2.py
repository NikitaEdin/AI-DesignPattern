class TrafficLightController:
    def __init__(self):
        self.current_mode = GreenMode()
    
    def change_mode(self):
        self.current_mode = self.current_mode.next()
    
    def show_signal(self):
        return self.current_mode.signal()

class GreenMode:
    def signal(self):
        return "GO"
    
    def next(self):
        return YellowMode()

class YellowMode:
    def signal(self):
        return "CAUTION"
    
    def next(self):
        return RedMode()

class RedMode:
    def signal(self):
        return "STOP"
    
    def next(self):
        return GreenMode()

if __name__ == "__main__":
    controller = TrafficLightController()
    
    for _ in range(6):
        print(controller.show_signal())
        controller.change_mode()