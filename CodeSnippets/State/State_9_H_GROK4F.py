from abc import ABC, abstractmethod

class InvalidTransition(Exception):
    pass

class PlayerController:
    def __init__(self):
        self._current_mode = None
        self._transition_to(StoppedPlayback(self))

    def _transition_to(self, mode):
        self._current_mode = mode
        mode._attach_controller(self)

    def initiate_play(self):
        self._current_mode.initiate_play()

    def toggle_pause(self):
        self._current_mode.toggle_pause()

    def halt_playback(self):
        self._current_mode.halt_playback()

    def get_status(self):
        return self._current_mode.__class__.__name__

class PlaybackHandler(ABC):
    def __init__(self, controller=None):
        self._controller = controller

    def _attach_controller(self, controller):
        self._controller = controller

    @abstractmethod
    def initiate_play(self):
        pass

    @abstractmethod
    def toggle_pause(self):
        pass

    @abstractmethod
    def halt_playback(self):
        pass

class StoppedPlayback(PlaybackHandler):
    def initiate_play(self):
        if self._controller is None:
            raise InvalidTransition("Controller not attached")
        print("Initiating playback from stopped.")
        self._controller._transition_to(ActivePlayback(self._controller))

    def toggle_pause(self):
        raise InvalidTransition("Cannot pause from stopped position.")

    def halt_playback(self):
        print("Already in stopped position.")

class ActivePlayback(PlaybackHandler):
    def initiate_play(self):
        print("Already actively playing.")

    def toggle_pause(self):
        if self._controller is None:
            raise InvalidTransition("Controller not attached")
        print("Switching to paused.")
        self._controller._transition_to(PausedPlayback(self._controller))

    def halt_playback(self):
        if self._controller is None:
            raise InvalidTransition("Controller not attached")
        print("Halting from active playback.")
        self._controller._transition_to(StoppedPlayback(self._controller))

class PausedPlayback(PlaybackHandler):
    def initiate_play(self):
        if self._controller is None:
            raise InvalidTransition("Controller not attached")
        print("Resuming from paused.")
        self._controller._transition_to(ActivePlayback(self._controller))

    def toggle_pause(self):
        print("Already paused.")

    def halt_playback(self):
        if self._controller is None:
            raise InvalidTransition("Controller not attached")
        print("Halting from paused.")
        self._controller._transition_to(StoppedPlayback(self._controller))

if __name__ == "__main__":
    controller = PlayerController()
    print(f"Initial status: {controller.get_status()}")
    controller.initiate_play()
    print(f"Status after play: {controller.get_status()}")
    controller.toggle_pause()
    print(f"Status after pause: {controller.get_status()}")
    controller.initiate_play()
    print(f"Status after resume: {controller.get_status()}")
    controller.halt_playback()
    print(f"Status after halt: {controller.get_status()}")
    try:
        controller.toggle_pause()
    except InvalidTransition as e:
        print(f"Handled edge case: {e}")
    print(f"Final status: {controller.get_status()}")