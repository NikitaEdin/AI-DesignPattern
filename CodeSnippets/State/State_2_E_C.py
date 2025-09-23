class Playing:
    def press_play(self, player):
        print("Already playing")
    
    def press_pause(self, player):
        print("Pausing")
        player.current = Paused()

class Paused:
    def press_play(self, player):
        print("Resuming")
        player.current = Playing()
    
    def press_pause(self, player):
        print("Already paused")

class MusicPlayer:
    def __init__(self):
        self.current = Paused()
    
    def play(self):
        self.current.press_play(self)
    
    def pause(self):
        self.current.press_pause(self)

if __name__ == "__main__":
    player = MusicPlayer()
    player.play()
    player.pause()
    player.pause()
    player.play()