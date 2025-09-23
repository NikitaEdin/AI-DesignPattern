class MediaPlayer:
    def __init__(self):
        self._current_mode = StoppedMode(self)
        self._volume = 50
    
    def set_mode(self, mode):
        self._current_mode = mode
    
    def play(self):
        return self._current_mode.play()
    
    def pause(self):
        return self._current_mode.pause()
    
    def stop(self):
        return self._current_mode.stop()
    
    def get_volume(self):
        return self._volume
    
    def set_volume(self, volume):
        if 0 <= volume <= 100:
            self._volume = volume

class PlaybackMode:
    def __init__(self, player):
        self._player = player
    
    def play(self):
        raise NotImplementedError
    
    def pause(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError

class StoppedMode(PlaybackMode):
    def play(self):
        self._player.set_mode(PlayingMode(self._player))
        return "Started playing"
    
    def pause(self):
        return "Cannot pause - not playing"
    
    def stop(self):
        return "Already stopped"

class PlayingMode(PlaybackMode):
    def play(self):
        return "Already playing"
    
    def pause(self):
        self._player.set_mode(PausedMode(self._player))
        return "Paused playback"
    
    def stop(self):
        self._player.set_mode(StoppedMode(self._player))
        return "Stopped playback"

class PausedMode(PlaybackMode):
    def play(self):
        self._player.set_mode(PlayingMode(self._player))
        return "Resumed playing"
    
    def pause(self):
        return "Already paused"
    
    def stop(self):
        self._player.set_mode(StoppedMode(self._player))
        return "Stopped playback"

if __name__ == "__main__":
    player = MediaPlayer()
    print(player.play())
    print(player.pause())
    print(player.play())
    print(player.stop())
    print(player.pause())