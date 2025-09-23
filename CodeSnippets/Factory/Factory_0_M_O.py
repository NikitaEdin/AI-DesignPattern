from __future__ import annotations
import json
import csv
import io
import threading
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, List


class ParserError(Exception):
    pass


class UnknownParserError(Exception):
    pass


class ParserBase(ABC):
    @abstractmethod
    def parse(self, data: str) -> dict:
        raise NotImplementedError


class JsonParser(ParserBase):
    def parse(self, data: str) -> dict:
        try:
            result = json.loads(data)
            if not isinstance(result, dict):
                return {"value": result}
            return result
        except json.JSONDecodeError as exc:
            raise ParserError(f"Invalid JSON: {exc}") from exc


class CsvParser(ParserBase):
    def __init__(self, delimiter: str = ","):
        self.delimiter = delimiter

    def parse(self, data: str) -> dict:
        try:
            stream = io.StringIO(data.strip())
            reader = csv.DictReader(stream, delimiter=self.delimiter)
            rows: List[dict] = [row for row in reader]
            return {"rows": rows}
        except Exception as exc:
            raise ParserError(f"CSV parsing failed: {exc}") from exc


class XmlParser(ParserBase):
    def parse(self, data: str) -> dict:
        try:
            root = ET.fromstring(data)
            return {root.tag: self._element_to_dict(root)}
        except ET.ParseError as exc:
            raise ParserError(f"XML parsing failed: {exc}") from exc

    def _element_to_dict(self, element: ET.Element) -> dict:
        children = list(element)
        if not children and (element.text is None or element.text.strip() == ""):
            return {}
        if not children:
            return element.text.strip() if element.text else ""
        result: Dict[str, List] = {}
        for child in children:
            child_dict = self._element_to_dict(child)
            result.setdefault(child.tag, []).append(child_dict)
        return result


class ParserProvider:
    def __init__(self):
        self._registry: Dict[str, Type[ParserBase]] = {}
        self._singletons: Dict[str, ParserBase] = {}
        self._singleton_flags: Dict[str, bool] = {}
        self._lock = threading.RLock()
        self._register_default_parsers()

    def _register_default_parsers(self) -> None:
        self.register_parser("json", JsonParser, singleton=True, allow_override=False)
        self.register_parser("csv", CsvParser, singleton=False, allow_override=False)
        self.register_parser("xml", XmlParser, singleton=False, allow_override=False)

    def register_parser(
        self,
        key: str,
        parser_cls: Type[ParserBase],
        singleton: bool = False,
        allow_override: bool = True,
    ) -> None:
        if not isinstance(key, str) or not key:
            raise ValueError("Parser key must be a non-empty string")
        if not issubclass(parser_cls, ParserBase):
            raise TypeError("parser_cls must be a subclass of ParserBase")
        with self._lock:
            if key in self._registry and not allow_override:
                raise ValueError(f"Parser for key '{key}' is already registered")
            self._registry[key] = parser_cls
            self._singleton_flags[key] = bool(singleton)
            if not self._singleton_flags[key]:
                self._singletons.pop(key, None)

    def list_parsers(self) -> List[str]:
        with self._lock:
            return sorted(self._registry.keys())

    def get_parser(self, key: str, **kwargs) -> ParserBase:
        with self._lock:
            parser_cls = self._registry.get(key)
            if parser_cls is None:
                raise UnknownParserError(f"No parser registered under key '{key}'")
            if self._singleton_flags.get(key, False):
                if key not in self._singletons:
                    instance = self._instantiate(parser_cls, **kwargs)
                    self._singletons[key] = instance
                return self._singletons[key]
            return self._instantiate(parser_cls, **kwargs)

    def _instantiate(self, parser_cls: Type[ParserBase], **kwargs) -> ParserBase:
        try:
            instance = parser_cls(**kwargs)
            if not isinstance(instance, ParserBase):
                raise TypeError("Instantiated object is not a ParserBase")
            return instance
        except TypeError as exc:
            raise ParserError(f"Failed to instantiate parser: {exc}") from exc


def main() -> None:
    provider = ParserProvider()

    json_data = '{"name": "Alice", "age": 30}'
    csv_data = "name,age\nAlice,30\nBob,25"
    xml_data = "<person><name>Alice</name><age>30</age></person>"

    try:
        parser = provider.get_parser("json")
        print("JSON parsed:", parser.parse(json_data))
    except (UnknownParserError, ParserError) as exc:
        print("Error with JSON parser:", exc)

    try:
        parser = provider.get_parser("csv", delimiter=",")
        print("CSV parsed:", parser.parse(csv_data))
    except (UnknownParserError, ParserError) as exc:
        print("Error with CSV parser:", exc)

    try:
        parser = provider.get_parser("xml")
        print("XML parsed:", parser.parse(xml_data))
    except (UnknownParserError, ParserError) as exc:
        print("Error with XML parser:", exc)

    try:
        provider.get_parser("yaml")
    except UnknownParserError as exc:
        print("Expected error for unknown parser:", exc)

    class UppercaseParser(ParserBase):
        def parse(self, data: str) -> dict:
            if not isinstance(data, str):
                raise ParserError("UppercaseParser expects a string")
            return {"uppercase": data.upper()}

    provider.register_parser("upper", UppercaseParser, singleton=False)
    parser = provider.get_parser("upper")
    print("Upper parsed:", parser.parse("hello"))

    try:
        provider.register_parser("json", JsonParser, allow_override=False)
    except ValueError as exc:
        print("Expected registration error:", exc)

    print("Available parsers:", provider.list_parsers())


if __name__ == "__main__":
    main()