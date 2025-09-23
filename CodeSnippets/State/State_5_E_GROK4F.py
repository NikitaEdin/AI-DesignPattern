from abc import ABC, abstractmethod

class PlayMode(ABC):
    @abstractmethod
    def play(self, player):
        pass

    @abstractmethod
    def pause(self, player):
        pass

    @abstractmethod
    def stop(self, player):
        pass

class ActiveMode(PlayMode):
    def play(self, player):
        print("Already playing")

    def pause(self, player):
        print("Paused")
        player.current_mode = PausedMode()

    def stop(self, player):
        print("Stopped")
        player.current_mode = StoppedMode()

class PausedMode(PlayMode):
    def play(self, player):
        print("Playing")
        player.current_mode = ActiveMode()

    def pause(self, player):
        print("Already paused")

    def stop(self, player):
        print("Stopped")
        player.current_mode = StoppedMode()

class StoppedMode(PlayMode):
    def play(self, player):
        print("Playing")
        player.current_mode = ActiveMode()

    def pause(self, player):
        print("Stopped")

    def stop(self, player):
        print("Already stopped")

class MediaPlayer:
    def __init__(self):
        self.current_mode = StoppedMode()

    def play(self):
        self.current_mode.play(self)

    def pause(self):
        self.current_mode.pause(self)

    def stop(self):
        self.current_mode.stop(self)

if __name__ == "__main__":
    player = MediaPlayer()
    player.play()
    player.pause()
    player.stop()