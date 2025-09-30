import subprocess
import os

class VideoProcessor:
    def extract_audio(self, input_file, output_file):
        if not os.path.exists(input_file):
            raise FileNotFoundError("Input video file not found")
        subprocess.run(["ffmpeg", "-y", "-i", input_file, "-vn", output_file], check=True)

class AudioNormalizer:
    def normalize(self, input_file, output_file):
        subprocess.run(["ffmpeg", "-y", "-i", input_file, "-af", "loudnorm", output_file], check=True)

class ThumbnailGenerator:
    def create_thumbnail(self, input_file, output_file, timestamp="00:00:01"):
        subprocess.run(["ffmpeg", "-y", "-ss", timestamp, "-i", audio_file, "-vframes", "1", output_file], check=True)

class MediaWorkflow:
    def __init__(self):
        self.video_processor = VideoProcessor()
        self.audio_normalizer = AudioNormalizer()
        self.thumbnail_generator = ThumbnailGenerator()
    
    def process_video(self, input_video, base_name):
        audio_file = f"{base_name}_audio.wav"
        normalized_audio = f"{base_name}_normalized.wav"
        thumbnail = f"{base_name}_thumbnail.jpg"
        
        self.video_processor.extract_audio(input_video, audio_file)
        self.audio_normalizer.normalize(audio_file, normalized_audio)
        self.thumbnail_generator.create_thumbnail(input_video, thumbnail)
        
        return {"audio": normalized_audio, "thumbnail": thumbnail}

if __name__ == "__main__":
    workflow = MediaWorkflow()
    results = workflow.process_video("sample.mp4", "output")
    print(results)