from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET

class DataSource(ABC):
    @abstractmethod
    def fetch(self) -> dict:
        pass

class JsonService:
    def get_json(self) -> str:
        return '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}'

class XmlService:
    def get_xml(self) -> str:
        return '<users><user><id>3</id><name>Charlie</name></user><user><id>4</id><name>Diana</name></user></users>'

class JsonConnector(DataSource):
    def __init__(self, service: JsonService):
        self._service = service
    
    def fetch(self) -> dict:
        raw = self._service.get_json()
        return json.loads(raw)

class XmlConnector(DataSource):
    def __init__(self, service: XmlService):
        self._service = service
    
    def fetch(self) -> dict:
        raw = self._service.get_xml()
        root = ET.fromstring(raw)
        users = []
        for user in root.findall('user'):
            users.append({
                'id': int(user.find('id').text),
                'name': user.find('name').text
            })
        return {'users': users}

class DataProcessor:
    def __init__(self, source: DataSource):
        self._source = source
    
    def process(self) -> list:
        data = self._source.fetch()
        return [f"{u['id']}: {u['name']}" for u in data['users']]

if __name__ == "__main__":
    json_service = JsonService()
    xml_service = XmlService()
    
    json_connector = JsonConnector(json_service)
    xml_connector = XmlConnector(xml_service)
    
    processor1 = DataProcessor(json_connector)
    processor2 = DataProcessor(xml_connector)
    
    print("JSON results:", processor1.process())
    print("XML results:", processor2.process())