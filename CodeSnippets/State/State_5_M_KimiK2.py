class AudioPlayer:
    def __init__(self):
        self.playback = StoppedMode(self)
        self.track = "Silence"
    
    def change_mode(self, new_mode):
        self.playback = new_mode
    
    def press_play(self, track):
        self.track = track
        self.playback.play()
    
    def press_pause(self):
        self.playback.pause()
    
    def press_stop(self):
        self.playback.stop()


class Mode:
    def __init__(self, player):
        self.player = player
    
    def play(self):
        raise NotImplementedError
    
    def pause(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError


class StoppedMode(Mode):
    def play(self):
        print(f"Starting playback of '{self.player.track}'")
        self.player.change_mode(PlayingMode(self.player))
    
    def pause(self):
        print("Cannot pause while stopped")
    
    def stop(self):
        print("Already stopped")


class PlayingMode(Mode):
    def play(self):
        print("Already playing")
    
    def pause(self):
        print("Pausing playback")
        self.player.change_mode(PausedMode(self.player))
    
    def stop(self):
        print("Stopping playback")
        self.player.change_mode(StoppedMode(self.player))


class PausedMode(Mode):
    def play(self):
        print(f"Resuming playback of '{self.player.track}'")
        self.player.change_mode(PlayingMode(self.player))
    
    def pause(self):
        print("Already paused")
    
    def stop(self):
        print("Stopping playback")
        self.player.change_mode(StoppedMode(self.player))


if __name__ == "__main__":
    player = AudioPlayer()
    player.press_play("Bohemian Rhapsody")
    player.press_pause()
    player.press_play("Bohemian Rhapsody")
    player.press_stop()
    player.press_pause()