class AudioMixer:
    def mix(self, audio_tracks):
        return f"Mixed audio: {', '.join(audio_tracks)}"

class VideoEncoder:
    def encode(self, video_file):
        return f"Encoded video: {video_file}"

class SubtitleHandler:
    def add_subtitles(self, subtitles):
        return f"Added subtitles: {', '.join(subtitles)}"

class StreamingService:
    def stream(self, content):
        return f"Streaming content: {content}"

class MediaProcessor:
    def __init__(self):
        self.mixer = AudioMixer()
        self.encoder = VideoEncoder()
        self.subtitle_handler = SubtitleHandler()
        self.streamer = StreamingService()

    def prepare_and_stream(self, video_file, audio_tracks, subtitles):
        try:
            encoded_video = self.encoder.encode(video_file)
            mixed_audio = self.mixer.mix(audio_tracks)
            subtitle_text = self.subtitle_handler.add_subtitles(subtitles)
            final_content = f"{encoded_video} | {mixed_audio} | {subtitle_text}"
            return self.streamer.stream(final_content)
        except Exception as e:
            return f"Error processing media: {e}"

if __name__ == "__main__":
    processor = MediaProcessor()
    result = processor.prepare_and_stream(
        "movie.mp4", 
        ["track1.mp3", "track2.mp3"], 
        ["English", "Spanish"]
    )
    print(result)