import os

class VideoPlayer:
    def __init__(self):
        self.is_on = False

    def on(self):
        self.is_on = True
        print("Video Player is on")

    def off(self):
        self.is_on = False
        print("Video Player is off")

    def play(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        print(f"Playing video: {file_path}")

    def stop(self):
        print("Video stopped")

class AudioSystem:
    def __init__(self):
        self.is_on = False
        self.volume = 0

    def on(self):
        self.is_on = True
        print("Audio System is on")

    def off(self):
        self.is_on = False
        print("Audio System is off")

    def set_volume(self, level):
        if 0 <= level <= 100:
            self.volume = level
            print(f"Volume set to {level}")
        else:
            raise ValueError("Volume must be between 0 and 100")

class Screen:
    def __init__(self):
        self.is_on = False

    def on(self):
        self.is_on = True
        print("Screen is on")

    def off(self):
        self.is_on = False
        print("Screen is off")

class MediaControl:
    def __init__(self, video_player, audio_system, screen):
        self.video_player = video_player
        self.audio_system = audio_system
        self.screen = screen

    def watch_media(self, file_path):
        try:
            self.screen.on()
            self.audio_system.on()
            self.audio_system.set_volume(50)
            self.video_player.on()
            self.video_player.play(file_path)
            print("Enjoy your media!")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error during playback: {e}")
            self.end_session()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.end_session()

    def end_session(self):
        self.video_player.stop()
        self.video_player.off()
        self.audio_system.off()
        self.screen.off()
        print("Session ended")

if __name__ == "__main__":
    player = VideoPlayer()
    audio = AudioSystem()
    scr = Screen()
    controller = MediaControl(player, audio, scr)
    controller.watch_media("sample_video.mp4")
    controller.end_session()