class PlayerMode:
    def play(self, player):
        pass

    def pause(self, player):
        pass

    def stop(self, player):
        pass

class PlayMode(PlayerMode):
    def play(self, player):
        print("Already playing")

    def pause(self, player):
        print("Pausing...")
        player.current_mode = PauseMode()

    def stop(self, player):
        print("Stopping...")
        player.current_mode = StopMode()

class PauseMode(PlayerMode):
    def play(self, player):
        print("Resuming...")
        player.current_mode = PlayMode()

    def pause(self, player):
        print("Already paused")

    def stop(self, player):
        print("Stopping...")
        player.current_mode = StopMode()

class StopMode(PlayerMode):
    def play(self, player):
        print("Starting playback...")
        player.current_mode = PlayMode()

    def pause(self, player):
        print("Cannot pause when stopped")

    def stop(self, player):
        print("Already stopped")

class MediaPlayer:
    def __init__(self):
        self.current_mode = StopMode()

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
    player.play()
    player.stop()
    player.pause()