import os
import abc
import tempfile

class CompressionMethod(abc.ABC):
    @abc.abstractmethod
    def compress(self, input_path: str, output_path: str) -> str:
        pass

    @abc.abstractmethod
    def extension(self) -> str:
        pass

class ZipCompressor(CompressionMethod):
    def compress(self, input_path: str, output_path: str) -> str:
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input not found: {input_path}")
        try:
            with open(input_path, "rb") as src, open(output_path, "wb") as dst:
                data = src.read()
                dst.write(b"ZIPHDR")
                dst.write(len(data).to_bytes(8, "big"))
                dst.write(data)
            return output_path
        except OSError as e:
            raise IOError(f"Failed to write archive: {e}") from e

    def extension(self) -> str:
        return ".zip"

class TarGzCompressor(CompressionMethod):
    def compress(self, input_path: str, output_path: str) -> str:
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input not found: {input_path}")
        try:
            with open(input_path, "rb") as src, open(output_path, "wb") as dst:
                data = src.read()
                dst.write(b"TARGZ")
                dst.write(len(data).to_bytes(8, "big"))
                dst.write(data)
            return output_path
        except OSError as e:
            raise IOError(f"Failed to write archive: {e}") from e

    def extension(self) -> str:
        return ".tar.gz"

class NoOpCompressor(CompressionMethod):
    def compress(self, input_path: str, output_path: str) -> str:
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input not found: {input_path}")
        try:
            with open(input_path, "rb") as src, open(output_path, "wb") as dst:
                dst.write(src.read())
            return output_path
        except OSError as e:
            raise IOError(f"Failed to write copy: {e}") from e

    def extension(self) -> str:
        return ".bin"

class FileArchiver:
    def __init__(self, method: CompressionMethod):
        if not isinstance(method, CompressionMethod):
            raise TypeError("method must implement CompressionMethod")
        self._method = method

    def set_method(self, method: CompressionMethod):
        if not isinstance(method, CompressionMethod):
            raise TypeError("method must implement CompressionMethod")
        self._method = method

    def archive(self, input_path: str, output_path: str = None) -> str:
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input file missing: {input_path}")
        ext = self._method.extension()
        if output_path is None:
            base = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(os.path.dirname(input_path), base + ext)
        return self._method.compress(input_path, output_path)

if __name__ == "__main__":
    tmp_dir = tempfile.mkdtemp()
    sample = os.path.join(tmp_dir, "sample.txt")
    with open(sample, "w") as f:
        f.write("Example content for archiving.")
    archiver = FileArchiver(NoOpCompressor())
    out1 = archiver.archive(sample)
    print("Created:", out1)
    archiver.set_method(ZipCompressor())
    out2 = archiver.archive(sample)
    print("Created:", out2)
    archiver.set_method(TarGzCompressor())
    out3 = archiver.archive(sample)
    print("Created:", out3)
    try:
        archiver.set_method(object())
    except TypeError as e:
        print("Error setting method:", e)