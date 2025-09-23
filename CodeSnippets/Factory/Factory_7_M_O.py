from abc import ABC, abstractmethod
import json

class ParserBase(ABC):
    def __init__(self, config=None):
        self.config = config or {}

    @abstractmethod
    def parse(self, text):
        pass

class JsonParser(ParserBase):
    def parse(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}") from e

class CsvParser(ParserBase):
    def parse(self, text):
        delimiter = self.config.get("delimiter", ",")
        lines = [line for line in text.splitlines() if line.strip()]
        if not lines:
            return []
        headers = [h.strip() for h in lines[0].split(delimiter)]
        rows = []
        for line in lines[1:]:
            parts = [p.strip() for p in line.split(delimiter)]
            if len(parts) != len(headers):
                raise ValueError("Row has incorrect number of columns")
            rows.append(dict(zip(headers, parts)))
        return rows

class ParserCreator:
    def __init__(self):
        self._registry = {}

    def register(self, key, cls):
        if not issubclass(cls, ParserBase):
            raise TypeError("Registered class must inherit from ParserBase")
        self._registry[key] = cls

    def create(self, key, config=None):
        cls = self._registry.get(key)
        if cls is None:
            raise ValueError(f"No parser registered for key: {key}")
        try:
            return cls(config=config)
        except Exception as e:
            raise RuntimeError(f"Failed to create parser '{key}': {e}") from e

if __name__ == "__main__":
    creator = ParserCreator()
    creator.register("json", JsonParser)
    creator.register("csv", CsvParser)

    json_text = '{"name": "Alice", "age": 30}'
    csv_text = "name,age\nBob,25\nCarol,40"

    json_parser = creator.create("json")
    print(json_parser.parse(json_text))

    csv_parser = creator.create("csv", config={"delimiter": ","})
    print(csv_parser.parse(csv_text))

    try:
        unknown = creator.create("xml")
    except Exception as e:
        print("Error:", e)