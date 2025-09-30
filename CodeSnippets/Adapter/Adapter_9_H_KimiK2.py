from abc import ABC, abstractmethod
from typing import Any, Dict, List
import json

class DataSource(ABC):
    @abstractmethod
    def fetch(self) -> Dict[str, Any]: ...

class LegacyXmlService:
    def get_xml_data(self) -> str:
        return "<root><user><id>1</id><name>Alice</name></user><user><id>2</id><name>Bob</name></user></root>"

class JsonApiService:
    def retrieve_json(self) -> Dict[str, Any]:
        return {"users": [{"id": 3, "name": "Charlie"}, {"id": 4, "name": "Diana"}]}

class XmlToJsonBridge(DataSource):
    def __init__(self, xml_service: LegacyXmlService):
        self._xml_service = xml_service
    
    def _parse_xml(self, xml: str) -> List[Dict[str, str]]:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml)
        return [{"id": user.find("id").text, "name": user.find("name").text} for user in root.findall("user")]
    
    def fetch(self) -> Dict[str, Any]:
        xml = self._xml_service.get_xml_data()
        users = self._parse_xml(xml)
        return {"users": users}

class JsonApiWrapper(DataSource):
    def __init__(self, json_service: JsonApiService):
        self._json_service = json_service
    
    def fetch(self) -> Dict[str, Any]:
        return self._json_service.retrieve_json()

class DataProcessor:
    def __init__(self, source: DataSource):
        self._source = source
    
    def process(self) -> str:
        data = self._source.fetch()
        users = data.get("users", [])
        return json.dumps({"processed": [{"uid": u["id"], "username": u["name"].upper()} for u in users]})

if __name__ == "__main__":
    xml_service = LegacyXmlService()
    json_service = JsonApiService()
    
    xml_bridge = XmlToJsonBridge(xml_service)
    json_wrapper = JsonApiWrapper(json_service)
    
    processor1 = DataProcessor(xml_bridge)
    processor2 = DataProcessor(json_wrapper)
    
    print(processor1.process())
    print(processor2.process())