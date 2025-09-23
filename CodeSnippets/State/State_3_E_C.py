class Playing:
    def press_button(self, player):
        print("Pausing music")
        player.current_mode = Paused()

class Paused:
    def press_button(self, player):
        print("Resuming music")
        player.current_mode = Playing()

class Stopped:
    def press_button(self, player):
        print("Starting music")
        player.current_mode = Playing()

class MusicPlayer:
    def __init__(self):
        self.current_mode = Stopped()
    
    def press_button(self):
        self.current_mode.press_button(self)

if __name__ == "__main__":
    player = MusicPlayer()
    player.press_button()
    player.press_button()
    player.press_button()
    player.press_button()