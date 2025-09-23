from abc import ABC, abstractmethod
import json

class DataSource(ABC):
    @abstractmethod
    def fetch(self) -> dict:
        pass

class JsonApi:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def get_raw_json(self) -> str:
        if not self.endpoint.startswith("http"):
            raise ValueError("Invalid endpoint")
        return '{"user": "alice", "age": 30, "city": "Paris"}'

class XmlService:
    def __init__(self, url: str):
        self.url = url

    def pull_xml(self) -> str:
        if not self.url.startswith("http"):
            raise ValueError("Invalid url")
        return "<user><name>bob</name><age>25</age><city>Tokyo</city></user>"

class JsonToDictBridge(DataSource):
    def __init__(self, api: JsonApi):
        self.api = api

    def fetch(self) -> dict:
        raw = self.api.get_raw_json()
        return json.loads(raw)

class XmlToDictBridge(DataSource):
    def __init__(self, service: XmlService):
        self.service = service

    def fetch(self) -> dict:
        import xml.etree.ElementTree as ET
        xml_str = self.service.pull_xml()
        root = ET.fromstring(xml_str)
        return {child.tag: child.text for child in root}

def main():
    json_api = JsonApi("https://api.example.com/user")
    xml_service = XmlService("https://service.example.com/data")

    json_source = JsonToDictBridge(json_api)
    xml_source = XmlToDictBridge(xml_service)

    print(json_source.fetch())
    print(xml_source.fetch())

if __name__ == "__main__":
    main()