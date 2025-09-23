from abc import ABC, abstractmethod

class Mode(ABC):
    @abstractmethod
    def activate(self, player):
        pass

    @abstractmethod
    def deactivate(self, player):
        pass

    @abstractmethod
    def play_action(self, player):
        pass

    @abstractmethod
    def pause_action(self, player):
        pass

    @abstractmethod
    def stop_action(self, player):
        pass

class Playing(Mode):
    def activate(self, player):
        player.is_playing = True
        print("Now playing")

    def deactivate(self, player):
        player.is_playing = False

    def play_action(self, player):
        raise ValueError("Cannot play while already playing")

    def pause_action(self, player):
        player.set_mode(Paused())

    def stop_action(self, player):
        player.set_mode(Stopped())

class Paused(Mode):
    def activate(self, player):
        print("Paused")

    def deactivate(self, player):
        pass

    def play_action(self, player):
        player.set_mode(Playing())

    def pause_action(self, player):
        raise ValueError("Cannot pause while already paused")

    def stop_action(self, player):
        player.set_mode(Stopped())

class Stopped(Mode):
    def activate(self, player):
        player.is_playing = False
        print("Stopped")

    def deactivate(self, player):
        pass

    def play_action(self, player):
        player.set_mode(Playing())

    def pause_action(self, player):
        raise ValueError("Cannot pause while stopped")

    def stop_action(self, player):
        print("Already stopped")

class Player:
    def __init__(self):
        self.current_mode = Stopped()
        self.current_mode.activate(self)
        self.is_playing = False

    def set_mode(self, mode):
        if hasattr(self.current_mode, 'deactivate'):
            self.current_mode.deactivate(self)
        self.current_mode = mode
        self.current_mode.activate(self)

    def play(self):
        try:
            self.current_mode.play_action(self)
        except ValueError as e:
            print(f"Error: {e}")

    def pause(self):
        try:
            self.current_mode.pause_action(self)
        except ValueError as e:
            print(f"Error: {e}")

    def stop(self):
        try:
            self.current_mode.stop_action(self)
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    player = Player()
    player.play()
    player.pause()
    player.play()
    player.stop()
    player.play()
    player.pause()  # Should error