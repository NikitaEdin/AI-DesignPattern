class MusicPlayer:
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
        
    def adjust_volume(self, change):
        self._volume = max(0, min(100, self._volume + change))

class PlayerMode:
    def __init__(self, player):
        self.player = player
        
    def play(self):
        raise NotImplementedError
        
    def pause(self):
        raise NotImplementedError
        
    def stop(self):
        raise NotImplementedError

class PlayingMode(PlayerMode):
    def play(self):
        return "Already playing"
        
    def pause(self):
        self.player.set_mode(PausedMode(self.player))
        return "Music paused"
        
    def stop(self):
        self.player.set_mode(StoppedMode(self.player))
        return "Music stopped"

class PausedMode(PlayerMode):
    def play(self):
        self.player.set_mode(PlayingMode(self.player))
        return "Resuming playback"
        
    def pause(self):
        return "Already paused"
        
    def stop(self):
        self.player.set_mode(StoppedMode(self.player))
        return "Music stopped"

class StoppedMode(PlayerMode):
    def play(self):
        self.player.set_mode(PlayingMode(self.player))
        return "Starting playback"
        
    def pause(self):
        return "Cannot pause - not playing"
        
    def stop(self):
        return "Already stopped"

if __name__ == "__main__":
    player = MusicPlayer()
    print(player.play())
    print(player.pause())
    print(player.play())
    print(player.stop())
    print(player.pause())