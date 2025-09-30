from abc import ABC, abstractmethod

class BaseMode(ABC):
    @abstractmethod
def press_play(self, player):
        pass
    
    @abstractmethod
    def press_pause(self, player):
        pass
    
    @abstractmethod
    def press_stop(self, player):
        pass

class IdleMode(BaseMode):
    def press_play(self, player):
        player.switch_mode(PlayingMode())
    def press_pause(self, player):
        pass
    def press_stop(self, player):
        pass

class PlayingMode(BaseMode):
    def press_play(self, player):
        pass
    def press_pause(self, player):
        player.switch_mode(PausedMode())
    def press_stop(self, player):
        player.switch_mode(IdleMode())

class PausedMode(BaseMode):
    def press_play(self, player):
        player.switch_mode(PlayingMode())
    def press_pause(self, player):
        pass
    def press_stop(self, player):
        player.switch_mode(IdleMode())

class MediaPlayer:
    def __init__(self):
        self._condition = IdleMode()
    
    def switch_mode(self, mode):
        self._condition = mode
    
    def press_play(self):
        self._condition.press_play(self)

    def press_pause(self):
        self._condition.press_pause(self)

    def press_stop(self):
        self._condition.press_stop(self)

if __name__ == "__main__":
    player = MediaPlayer()
    player.press_play()
    player.press_pause()
    player.press_play()
    player.press_stop()