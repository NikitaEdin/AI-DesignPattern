class TrafficLightController:
    def __init__(self):
        self.current_phase = RedPhase(self)
        self.cycle_count = 0

    def change_phase(self):
        self.current_phase.next_phase()
        self.cycle_count += 1
        if self.cycle_count % 5 == 0:
            print(f"Completed {self.cycle_count} cycles")

    def display_status(self):
        self.current_phase.show()

    def get_phase_name(self):
        return self.current_phase.__class__.__name__

class LightPhase:
    def __init__(self, controller):
        self.controller = controller

    def next_phase(self):
        pass

    def show(self):
        pass

class RedPhase(LightPhase):
    def next_phase(self):
        self.controller.current_phase = GreenPhase(self.controller)

    def show(self):
        print("Red light: Stop")

class GreenPhase(LightPhase):
    def next_phase(self):
        self.controller.current_phase = YellowPhase(self.controller)

    def show(self):
        print("Green light: Go")

class YellowPhase(LightPhase):
    def next_phase(self):
        self.controller.current_phase = RedPhase(self.controller)

    def show(self):
        print("Yellow light: Caution")

if __name__ == "__main__":
    controller = TrafficLightController()
    for _ in range(6):
        controller.display_status()
        controller.change_phase()
    print(f"Final phase: {controller.get_phase_name()}")