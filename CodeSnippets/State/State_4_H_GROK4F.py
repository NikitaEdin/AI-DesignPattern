from abc import ABC, abstractmethod

class Mode(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def play(self, controller):
        pass

    @abstractmethod
    def pause(self, controller):
        pass

    @abstractmethod
    def stop(self, controller):
        pass

    @abstractmethod
    def next_track(self, controller):
        pass

    @abstractmethod
    def previous_track(self, controller):
        pass

    @abstractmethod
    def forward(self, controller, seconds):
        pass

    @abstractmethod
    def rewind(self, controller, seconds):
        pass

class StoppedMode(Mode):
    def get_description(self):
        return "Stopped"

    def play(self, controller):
        controller.current_mode = PlayingMode()

    def pause(self, controller):
        pass

    def stop(self, controller):
        pass

    def next_track(self, controller):
        controller.current_track = (controller.current_track + 1) % len(controller.playlist)
        controller.position = 0.0

    def previous_track(self, controller):
        controller.current_track = (controller.current_track - 1) % len(controller.playlist)
        controller.position = 0.0

    def forward(self, controller, seconds):
        pass

    def rewind(self, controller, seconds):
        pass

class PlayingMode(Mode):
    def get_description(self):
        return "Playing"

    def play(self, controller):
        pass

    def pause(self, controller):
        controller.current_mode = PausedMode()

    def stop(self, controller):
        controller.current_mode = StoppedMode()

    def next_track(self, controller):
        controller.current_track = (controller.current_track + 1) % len(controller.playlist)
        controller.position = 0.0

    def previous_track(self, controller):
        controller.current_track = (controller.current_track - 1) % len(controller.playlist)
        controller.position = 0.0

    def forward(self, controller, seconds):
        controller.position += seconds

    def rewind(self, controller, seconds):
        controller.position = max(0.0, controller.position - seconds)

class PausedMode(Mode):
    def get_description(self):
        return "Paused"

    def play(self, controller):
        controller.current_mode = PlayingMode()

    def pause(self, controller):
        pass

    def stop(self, controller):
        controller.current_mode = StoppedMode()

    def next_track(self, controller):
        controller.current_track = (controller.current_track + 1) % len(controller.playlist)
        controller.position = 0.0

    def previous_track(self, controller):
        controller.current_track = (controller.current_track - 1) % len(controller.playlist)
        controller.position = 0.0

    def forward(self, controller, seconds):
        controller.position += seconds

    def rewind(self, controller, seconds):
        controller.position = max(0.0, controller.position - seconds)

class MediaController:
    def __init__(self):
        self.playlist = ["Track 1", "Track 2", "Track 3"]
        self.current_track = 0
        self.position = 0.0
        self.current_mode = StoppedMode()

    def play(self):
        self.current_mode.play(self)

    def pause(self):
        self.current_mode.pause(self)

    def stop(self):
        self.current_mode.stop(self)

    def next_track(self):
        self.current_mode.next_track(self)

    def previous_track(self):
        self.current_mode.previous_track(self)

    def forward(self, seconds):
        self.current_mode.forward(self, seconds)

    def rewind(self, seconds):
        self.current_mode.rewind(self, seconds)

    def get_status(self):
        track_name = self.playlist[self.current_track]
        return f"{self.current_mode.get_description()} - {track_name} at {self.position:.1f}s"

if __name__ == "__main__":
    controller = MediaController()
    print(controller.get_status())
    controller.next_track()
    print(controller.get_status())
    controller.play()
    print(controller.get_status())
    controller.forward(30)
    print(controller.get_status())
    controller.pause()
    print(controller.get_status())
    controller.rewind(40)
    print(controller.get_status())
    controller.next_track()
    print(controller.get_status())
    controller.play()
    print(controller.get_status())
    controller.forward(5)
    print(controller.get_status())
    controller.stop()
    print(controller.get_status())
    controller.play()
    print(controller.get_status())