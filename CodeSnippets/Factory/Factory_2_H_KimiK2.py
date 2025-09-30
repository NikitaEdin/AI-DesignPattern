from abc import ABC, abstractmethod
from typing import Dict, Type
import logging

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: str) -> str:
        pass

class CsvHandler(DataProcessor):
    def process(self, data: str) -> str:
        return f"CSV: {data.upper()}"

class JsonHandler(DataProcessor):
    def process(self, data: str) -> str:
        return f"JSON: {data.lower()}"

class XmlHandler(DataProcessor):
    def process(self, data: str) -> str:
        return f"XML: <root>{data}</root>"

class HandlerRegistry:
    def __init__(self):
        self._handlers: Dict[str, Type[DataProcessor]] = {}
        self._logger = logging.getLogger(self.__class__.__name__)

    def register(self, key: str, handler_class: Type[DataProcessor]) -> None:
        if not issubclass(handler_class, DataProcessor):
            raise TypeError("Handler must inherit from DataProcessor")
        self._handlers[key] = handler_class
        self._logger.debug(f"Registered {handler_class.__name__} for {key}")

    def get(self, key: str) -> DataProcessor:
        try:
            handler_class = self._handlers[key]
            return handler_class()
        except KeyError:
            raise ValueError(f"No handler for {key}")

    def list_available(self) -> list:
        return list(self._handlers.keys())

class ProcessingEngine:
    def __init__(self):
        self.registry = HandlerRegistry()
        self._initialize_defaults()

    def _initialize_defaults(self):
        self.registry.register("csv", CsvHandler)
        self.registry.register("json", JsonHandler)
        self.registry.register("xml", XmlHandler)

    def execute(self, format_type: str, data: str) -> str:
        handler = self.registry.get(format_type)
        return handler.process(data)

if __name__ == "__main__":
    engine = ProcessingEngine()
    
    result1 = engine.execute("csv", "user,data,123")
    result2 = engine.execute("json", "{'name':'test'}")
    result3 = engine.execute("xml", "content")
    
    print(result1)
    print(result2)
    print(result3)