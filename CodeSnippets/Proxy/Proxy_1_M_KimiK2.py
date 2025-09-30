import time
from abc import ABC, abstractmethod

class FileInterface(ABC):
    @abstractmethod
    def read(self) -> str: ...

class RealFile(FileInterface):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        time.sleep(1)
        self.content = f"Content of {self.filename}"

    def read(self) -> str:
        return self.content

class FileWrapper(FileInterface):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._file: RealFile | None = None

    def read(self) -> str:
        if self._file is None:
            self._file = RealFile(self.filename)
        return self._file.read()

if __file__ == "__main__":
    wrapper = FileWrapper("example.txt")
    print("File accessed:", wrapper.read())