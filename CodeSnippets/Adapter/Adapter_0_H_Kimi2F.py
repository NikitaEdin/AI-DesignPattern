import abc
from typing import Protocol, runtime_checkable

@runtime_checkable
class JsonStream(Protocol):
    def fetch_json(self) -> dict:
        ...

class LegacyXmlEndpoint:
    def get_raw_xml(self) -> str:
        return "<root><item id='42'>legacy data</item></root>"

class YamlLogger:
    def read_yaml(self) -> str:
        return "records:\n  - code: 200\n    msg: ok"

class XmlToJsonBridge:
    def __init__(self, xml_source: LegacyXmlEndpoint):
        self._source = xml_source

    def fetch_json(self) -> dict:
        xml = self._source.get_raw_xml()
        item_start = xml.find("<item id='") + 10
        item_end = xml.find("'>", item_start)
        id_val = xml[item_start:item_end]
        content_start = xml.find("'>", item_end) + 2
        content_end = xml.find("</item>", content_start)
        text = xml[content_start:content_end]
        return {"id": int(id_val), "content": text}

class YamlToJsonBridge:
    def __init__(self, yaml_source: YamlLogger):
        self._source = yaml_source

    def fetch_json(self) -> dict:
        import yaml
        raw = self._source.read_yaml()
        data = yaml.safe_load(raw)
        return {"records": [{"code": rec["code"], "message": rec["msg"]} for rec in data.get("records", [])]}

def process_stream(stream: JsonStream) -> None:
    payload = stream.fetch_json()
    print("Processed JSON:", payload)

if __name__ == "__main__":
    xml_api = LegacyXmlEndpoint()
    yaml_api = YamlLogger()
    json_stream1 = XmlToJsonBridge(xml_api)
    json_stream2 = YamlToJsonBridge(yaml_api)
    process_stream(json_stream1)
    process_stream(json_stream2)