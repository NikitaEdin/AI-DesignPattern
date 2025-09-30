import abc
import threading
from typing import Dict, Type, Any


class DataReader(abc.ABC):
    @abc.abstractmethod
    def read(self, source: str) -> Any:
        pass

    @abc.abstractmethod
    def supported_extensions(self) -> list:
        pass


class CsvHandler(DataReader):
    def read(self, source: str) -> Any:
        if not source.endswith('.csv'):
            raise ValueError("Invalid CSV file")
        return f"CSV data from {source}"

    def supported_extensions(self) -> list:
        return ['.csv']


class JsonHandler(DataReader):
    def read(self, source: str) -> Any:
        if not source.endswith('.json'):
            raise ValueError("Invalid JSON file")
        return f"JSON data from {source}"

    def supported_extensions(self) -> list:
        return ['.json']


class XmlHandler(DataReader):
    def read(self, source: str) -> Any:
        if not source.endswith('.xml'):
            raise ValueError("Invalid XML file")
        return f"XML data from {source}"

    def supported_extensions(self) -> list:
        return ['.xml']


class HandlerManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(HandlerManager, cls).__new__(cls)
                    cls._instance._handlers: Dict[str, Type[DataReader]] = {}
                    cls._instance._register_default_handlers()
        return cls._instance

    def _register_default_handlers(self):
        self.register('.csv', CsvHandler)
        self.register('.json', JsonHandler)
        self.register('.xml', XmlHandler)

    def register(self, extension: str, handler_cls: Type[DataReader]):
        self._handlers[extension.lower()] = handler_cls

    def get_handler(self, extension: str) -> DataReader:
        handler_cls = self._handlers.get(extension.lower())
        if not handler_cls:
            raise ValueError(f"No handler for extension {extension}")
        return handler_cls()

    def list_handlers(self):
        return list(self._handlers.keys())


class DataProcessor:
    def __init__(self):
        self.manager = HandlerManager()

    def process(self, filepath: str) -> Any:
        extension = '.' + filepath.split('.')[-1].lower()
        handler = self.manager.get_handler(extension)
        return handler.read(filepath)


if __name__ == "__main__":
    processor = DataProcessor()
    print(processor.process("data.csv"))
    print(processor.process("config.json"))
    print(processor.process("metadata.xml"))