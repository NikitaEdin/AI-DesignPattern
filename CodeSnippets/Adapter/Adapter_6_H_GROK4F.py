from abc import ABC, abstractmethod
import sys

class MediaPlayer(ABC):
    @abstractmethod
    def play(self, format_type, file_path):
        pass

class Mp4Handler:
    def handle_mp4(self, file_path):
        if not file_path or not isinstance(file_path, str) or len(file_path.strip()) == 0:
            raise ValueError("Invalid file path for MP4")
        print(f"Decoding and playing MP4: {file_path}")

class VlcHandler:
    def handle_vlc(self, file_path):
        if not file_path or not isinstance(file_path, str) or len(file_path.strip()) == 0:
            raise ValueError("Invalid file path for VLC")
        print(f"Decoding and playing VLC: {file_path}")

class UniversalPlayer(MediaPlayer):
    def __init__(self):
        self.format_handlers = {}
        self._initialize_handlers()

    def _initialize_handlers(self):
        try:
            self.format_handlers['mp4'] = Mp4Handler()
        except Exception as e:
            print(f"Warning: MP4 handler initialization failed - {e}", file=sys.stderr)
            self.format_handlers['mp4'] = None

        try:
            self.format_handlers['vlc'] = VlcHandler()
        except Exception as e:
            print(f"Warning: VLC handler initialization failed - {e}", file=sys.stderr)
            self.format_handlers['vlc'] = None

    def play(self, format_type, file_path):
        if format_type not in self.format_handlers:
            raise ValueError(f"Unsupported format: {format_type}. Available: {list(self.format_handlers.keys())}")

        handler = self.format_handlers[format_type]
        if handler is None:
            raise RuntimeError(f"Handler for {format_type} is unavailable")

        try:
            if format_type == 'mp4':
                handler.handle_mp4(file_path)
            elif format_type == 'vlc':
                handler.handle_vlc(file_path)
        except ValueError as ve:
            raise ValueError(f"Playback failed for {format_type}: {ve}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during playback of {format_type}: {e}")

    def get_supported_formats(self):
        return [fmt for fmt, handler in self.format_handlers.items() if handler is not None]

if __name__ == "__main__":
    try:
        player = UniversalPlayer()
        print("Supported formats:", player.get_supported_formats())

        player.play('mp4', 'sample.mp4')
        player.play('vlc', 'sample.vlc')

        player.play('mp4', '')  # Should raise ValueError
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except RuntimeError as re:
        print(f"RuntimeError: {re}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        player.play('wav', 'sample.wav')  # Unsupported format
    except ValueError as ve:
        print(f"ValueError for unsupported: {ve}")