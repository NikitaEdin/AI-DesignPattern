class Player:
    def __init__(self):
        self._current_mode = StopMode(self)
        self._is_muted = False
        self._volume = 50
        self._track_position = 0

    def play(self):
        self._current_mode.play()

    def pause(self):
        self._current_mode.pause()

    def stop(self):
        self._current_mode.stop()

    def mute(self):
        self._is_muted = not self._is_muted

    def set_volume(self, level):
        if 0 <= level <= 100:
            self._volume = level
        else:
            raise ValueError("Volume must be between 0 and 100")

    def get_status(self):
        return {
            "mode": self._current_mode.__class__.__name__,
            "muted": self._is_muted,
            "volume": self._volume,
            "position": self._track_position
        }

    def _set_mode(self, mode):
        if not isinstance(mode, (PlayMode, PauseMode, StopMode)):
            raise ValueError("Invalid mode transition")
        self._current_mode = mode

    def advance_position(self, seconds):
        if isinstance(self._current_mode, PlayMode):
            self._track_position += seconds

class PlayMode:
    def __init__(self, player):
        self._player = player

    def play(self):
        pass  # Already playing

    def pause(self):
        self._player._set_mode(PauseMode(self._player))
        print("Paused")

    def stop(self):
        self._player._set_mode(StopMode(self._player))
        self._player._track_position = 0
        print("Stopped")

class PauseMode:
    def __init__(self, player):
        self._player = player

    def play(self):
        self._player._set_mode(PlayMode(self._player))
        print("Playing")

    def pause(self):
        pass  # Already paused

    def stop(self):
        self._player._set_mode(StopMode(self._player))
        self._player._track_position = 0
        print("Stopped")

class StopMode:
    def __init__(self, player):
        self._player = player

    def play(self):
        self._player._set_mode(PlayMode(self._player))
        print("Playing")

    def pause(self):
        pass  # Cannot pause from stop, remains stopped

    def stop(self):
        pass  # Already stopped

def main():
    player = Player()
    print("Initial status:", player.get_status())

    player.play()
    print("After play:", player.get_status())

    player.set_volume(75)
    player.advance_position(30)
    print("After volume and position:", player.get_status())

    player.pause()
    print("After pause:", player.get_status())

    player.pause()  # Edge case: pause when already paused
    print("After redundant pause:", player.get_status())

    player.play()
    player.stop()
    print("After stop:", player.get_status())

    try:
        player.set_volume(150)  # Edge case: invalid volume
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()