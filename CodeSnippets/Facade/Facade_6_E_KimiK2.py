class VideoFile:
    def __init__(self, name):
        self.name = name


class CompressionCodec:
    def compress(self, video):
        return f"Compressed {video.name}"


class AudioEnhancer:
    def enhance(self, video):
        return f"Enhanced audio for {video.name}"


class VideoConverter:
    def convert(self, name):
        video = VideoFile(name)
        compressor = CompressionCodec()
        enhancer = AudioEnhancer()
        compressed = compressor.compress(video)
        enhanced = enhancer.enhance(video)
        return f"{compressed} - {enhanced}"


if __name__ == "__main__":
    converter = VideoConverter()
    result = converter.convert("example.mp4")
    print(result)