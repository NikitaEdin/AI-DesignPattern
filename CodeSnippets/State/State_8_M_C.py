from abc import ABC, abstractmethod

class MusicPlayerMode(ABC):
    @abstractmethod
    def play(self, player):
        pass
    
    @abstractmethod
    def pause(self, player):
        pass
    
    @abstractmethod
    def stop(self, player):
        pass

class PlayingMode(MusicPlayerMode):
    def play(self, player):
        print("Already playing")
    
    def pause(self, player):
        print("Pausing music")
        player.change_mode(PausedMode())
    
    def stop(self, player):
        print("Stopping music")
        player.change_mode(StoppedMode())

class PausedMode(MusicPlayerMode):
    def play(self, player):
        print("Resuming music")
        player.change_mode(PlayingMode())
    
    def pause(self, player):
        print("Already paused")
    
    def stop(self, player):
        print("Stopping music")
        player.change_mode(StoppedMode())

class StoppedMode(MusicPlayerMode):
    def play(self, player):
        print("Starting music")
        player.change_mode(PlayingMode())
    
    def pause(self, player):
        print("Cannot pause - music is stopped")
    
    def stop(self, player):
        print("Already stopped")

class MusicPlayer:
    def __init__(self):
        self._current_mode = StoppedMode()
        self._track_position = 0
    
    def change_mode(self, new_mode):
        if isinstance(new_mode, StoppedMode):
            self._track_position = 0
        self._current_mode = new_mode
    
    def play(self):
        self._current_mode.play(self)
    
    def pause(self):
        self._current_mode.pause(self)
    
    def stop(self):
        self._current_mode.stop(self)
    
    def get_position(self):
        return self._track_position

if __name__ == "__main__":
    player = MusicPlayer()
    
    player.play()
    player.pause()
    player.play()
    player.stop()
    player.pause()