import abc

class TrafficLight:
    def __init__(self):
        self._current_phase = StopPhase()
        self._current_phase.set_controller(self)

    def advance(self):
        self._current_phase.advance(self)

    def display_status(self):
        self._current_phase.show_status()

    def switch_to(self, phase_class):
        current = self._current_phase.__class__
        if current == StopPhase and phase_class == CautionPhase:
            print("Invalid transition: Cannot switch directly from Stop to Caution")
            return False
        if current == CautionPhase and phase_class == GoPhase:
            print("Invalid transition: Cannot switch directly from Caution to Go")
            return False
        if current == GoPhase and phase_class == StopPhase:
            print("Invalid transition: Cannot switch directly from Go to Stop")
            return False
        self._current_phase = phase_class()
        self._current_phase.set_controller(self)
        return True

class Phase(abc.ABC):
    def __init__(self):
        self._controller = None

    def set_controller(self, controller):
        self._controller = controller

    @abc.abstractmethod
    def advance(self, controller):
        pass

    @abc.abstractmethod
    def show_status(self):
        pass

class StopPhase(Phase):
    def advance(self, controller):
        print("Advancing from Stop to Go")
        controller._current_phase = GoPhase()
        controller._current_phase.set_controller(controller)

    def show_status(self):
        print("Red light: Vehicles must stop")

class GoPhase(Phase):
    def advance(self, controller):
        print("Advancing from Go to Caution")
        controller._current_phase = CautionPhase()
        controller._current_phase.set_controller(controller)

    def show_status(self):
        print("Green light: Vehicles may proceed")

class CautionPhase(Phase):
    def advance(self, controller):
        print("Advancing from Caution to Stop")
        controller._current_phase = StopPhase()
        controller._current_phase.set_controller(controller)

    def show_status(self):
        print("Yellow light: Prepare to stop")

if __name__ == "__main__":
    controller = TrafficLight()
    print("Initial status:")
    controller.display_status()
    print("\nSimulating normal cycle:")
    for _ in range(3):
        controller.advance()
        controller.display_status()
    print("\nTesting invalid transition from Stop to Caution:")
    controller.switch_to(StopPhase)
    controller.switch_to(CautionPhase)
    print("\nAfter invalid attempt:")
    controller.display_status()
    print("\nValid switch from Stop to Go:")
    controller.switch_to(GoPhase)
    controller.display_status()