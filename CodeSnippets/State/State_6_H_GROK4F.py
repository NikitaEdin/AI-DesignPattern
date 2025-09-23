from abc import ABC, abstractmethod

class SignalPhase(ABC):
    def __init__(self, controller):
        self.controller = controller

    def entry_action(self):
        pass

    def exit_action(self):
        pass

    @abstractmethod
    def advance(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class StopPhase(SignalPhase):
    def entry_action(self):
        print("Red light: Vehicles must stop.")

    def advance(self):
        self.controller.change_to(CautionPhase)

    def stop(self):
        self.controller.change_to(StopPhase)

class CautionPhase(SignalPhase):
    def entry_action(self):
        print("Yellow light: Prepare to stop.")

    def exit_action(self):
        print("Exiting yellow phase.")

    def advance(self):
        self.controller.change_to(GoPhase)

    def stop(self):
        self.controller.change_to(StopPhase)

class GoPhase(SignalPhase):
    def entry_action(self):
        print("Green light: Proceed with caution.")

    def advance(self):
        self.controller.change_to(StopPhase)

    def stop(self):
        self.controller.change_to(StopPhase)

class TrafficController:
    def __init__(self):
        self._current_phase = None
        self.change_to(StopPhase)

    def change_to(self, phase_class):
        if self._current_phase and phase_class == type(self._current_phase):
            print("Already in this phase. No change.")
            return
        if self._current_phase:
            self._current_phase.exit_action()
        new_phase = phase_class(self)
        new_phase.entry_action()
        self._current_phase = new_phase

    def advance(self):
        self._current_phase.advance()

    def stop(self):
        self._current_phase.stop()

if __name__ == "__main__":
    ctrl = TrafficController()
    ctrl.advance()  # Changes to yellow
    ctrl.advance()  # Changes to green
    ctrl.stop()     # Emergency stop to red
    ctrl.advance()  # To yellow
    ctrl.stop()     # Already red, no change
    ctrl.advance()  # To green
    ctrl.advance()  # To red