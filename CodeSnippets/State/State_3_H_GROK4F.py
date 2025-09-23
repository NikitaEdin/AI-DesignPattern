from abc import ABC, abstractmethod

class PlaybackMode(ABC):
    @abstractmethod
    def play(self, player):
        pass

    @abstractmethod
    def pause(self, player):
        pass

    @abstractmethod
    def stop(self, player):
        pass

    @abstractmethod
    def get_name(self):
        pass

class PlayingMode(PlaybackMode):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PlayingMode, cls).__new__(cls)
            cls._instance.name = "Playing"
        return cls._instance

    def play(self, player):
        print("Already in playback.")

    def pause(self, player):
        player.current_mode = PausedMode()
        print("Transitioned to pause.")

    def stop(self, player):
        player.current_mode = StoppedMode()
        print("Transitioned to stop.")

    def get_name(self):
        return self.name

class PausedMode(PlaybackMode):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PausedMode, cls).__new__(cls)
            cls._instance.name = "Paused"
        return cls._instance

    def play(self, player):
        player.current_mode = PlayingMode()
        print("Resumed playback.")

    def pause(self, player):
        print("Already paused.")

    def stop(self, player):
        player.current_mode = StoppedMode()
        print("Transitioned to stop from pause.")

    def get_name(self):
        return self.name

class StoppedMode(PlaybackMode):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StoppedMode, cls).__new__(cls)
            cls._instance.name = "Stopped"
        return cls._instance

    def play(self, player):
        player.current_mode = PlayingMode()
        print("Initiated playback.")

    def pause(self, player):
        print("Cannot pause when stopped.")

    def stop(self, player):
        print("Already stopped.")

    def get_name(self):
        return self.name

class MediaPlayer:
    def __init__(self):
        self.current_mode = StoppedMode()
        self.is_muted = False

    def play(self):
        try:
            self.current_mode.play(self)
        except Exception:
            print("Error during play action.")

    def pause(self):
        try:
            self.current_mode.pause(self)
        except Exception:
            print("Error during pause action.")

    def stop(self):
        try:
            self.current_mode.stop(self)
        except Exception:
            print("Error during stop action.")

    def get_status(self):
        return self.current_mode.get_name()

    def toggle_mute(self):
        if self.current_mode == StoppedMode():
            print("Cannot mute when stopped.")
            return
        self.is_muted = not self.is_muted
        status = "muted" if self.is_muted else "unmuted"
        print(f"Audio toggled to {status}.")

if __name__ == "__main__":
    player = MediaPlayer()
    print(f"Initial status: {player.get_status()}")
    player.play()
    print(f"Status: {player.get_status()}")
    player.toggle_mute()
    player.pause()
    print(f"Status: {player.get_status()}")
    player.pause()
    player.play()
    print(f"Status: {player.get_status()}")
    player.stop()
    print(f"Status: {player.get_status()}")
    player.toggle_mute()
    player.play()
    player.stop()
    print(f"Final status: {player.get_status()}")