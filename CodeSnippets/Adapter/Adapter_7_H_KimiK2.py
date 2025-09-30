import abc
from typing import Protocol


class JsonSource(Protocol):
    def provide(self) -> dict:
        ...


class XmlSource(Protocol):
    def fetch(self) -> str:
        ...


class LegacyXmlFeed:
    def fetch(self) -> str:
        return "<data><value>42</value><unit>C</unit></data>"


class ModernJsonApi:
    def provide(self) -> dict:
        return {"temperature": {"value": 42, "unit": "C"}}


class XmlToJsonBridge:
    def __init__(self, xml_feed: XmlSource) -> None:
        self._xml_feed = xml_feed

    def provide(self) -> dict:
        raw = self._xml_fetch()
        return self._transform(raw)

    def _xml_fetch(self) -> str:
        if not hasattr(self._xml_feed, "fetch"):
            raise RuntimeError("Underlying source lacks fetch()")
        return self._xml_feed.fetch()

    @staticmethod
    def _transform(xml: str) -> dict:
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml)
            value_node = root.find("value")
            unit_node = root.find("unit")
            if value_node is None or unit_node is None:
                raise ValueError("Invalid XML structure")
            return {"temperature": {"value": int(value_node.text), "unit": unit_node.text}}
        except Exception:
            return {"temperature": {"value": None, "unit": None}}


def main():
    legacy = LegacyXmlFeed()
    bridge = XmlToJsonBridge(legacy)

    modern: JsonSource = bridge
    print("Adapted payload:", modern.provide())


if __name__ == "__main__":
    main()