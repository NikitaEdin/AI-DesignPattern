from __future__ import annotations
from abc import ABC, abstractmethod
import logging

class MediaPlayer:
    def __init__(self):
        self._behavior = StoppedBehavior(self)
        self._playlist = []
        self._current = 0
        self._logger = logging.getLogger(self.__class__.__name__)

    def transition(self, new_behavior):
        self._logger.info(f"Switching from {self._behavior.__class__.__name__} to {new_behavior.__class__.__name__}")
        self._behavior = new_behavior

    def press_play(self): self._behavior.press_play()
    def press_pause(self): self._behavior.press_pause()
    def press_stop(self): self._behavior.press_stop()
    def next_track(self): self._behavior.next_track()
    def prev_track(self): self._behavior.prev_track()
    def get_status(self): return self._behavior.get_status()

    def load_playlist(self, tracks):
        self._playlist = tracks
        self._current = 0

    def current_track(self):
        return self._playlist[self._current] if self._playlist else "No track"

class Behavior(ABC):
    def __init__(self, player):
        self._player = player

    @abstractmethod
    def press_play(self): pass
    @abstractmethod
    def press_pause(self): pass
    @abstractmethod
    def press_stop(self): pass
    def next_track(self):
        if self._player._playlist:
            self._player._current = (self._player._current + 1) % len(self._player._playlist)
            self._player._logger.info(f"Track changed to: {self._player.current_track()}")
    def prev_track(self):
        if self._player._playlist:
            self._player._current = (self._player._current - 1) % len(self._player._playlist)
            self._player._logger.info(f"Track changed to: {self._player.current_track()}")
    @abstractmethod
    def get_status(self): pass

class PlayingBehavior(Behavior):
    def press_play(self):
        self._player._logger.warning("Already playing")
    def press_pause(self):
        self._player.transition(PausedBehavior(self._player))
    def press_stop(self):
        self._player.transition(StoppedBehavior(self._player))
    def get_status(self):
        return f"Playing: {self._player.current_track()}"

class PausedBehavior(Behavior):
    def press_play(self):
        self._player.transition(PlayingBehavior(self._player))
    def press_pause(self):
        self._player._logger.warning("Already paused")
    def press_stop(self):
        self._player.transition(StoppedBehavior(self._player))
    def get_status(self):
        return f"Paused: {self._player.current_track()}"

class StoppedBehavior(Behavior):
    def press_play(self):
        if self._player._playlist:
            self._player.transition(PlayingBehavior(self._player))
        else:
            self._player._logger.error("No playlist loaded")
    def press_pause(self):
        self._player._logger.warning("Cannot pause when stopped")
    def press_stop(self):
        self._player._logger.warning("Already stopped")
    def get_status(self):
        return f"Stopped: {self._player.current_track()}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    player = MediaPlayer()
    player.load_playlist(["Song 1", "Song 2", "Song 3"])
    
    print(player.get_status())
    player.press_play()
    print(player.get_status())
    player.next_track()
    print(player.get_status())
    player.press_pause()
    print(player.get_status())
    player.press_stop()
    print(player.get_status())
    player.press_play()
    print(player.get_status())