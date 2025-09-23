from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json
import xml.etree.ElementTree as ET

class DataProcessor(ABC):
    @abstractmethod
    def process_data(self, data: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_format(self) -> str:
        pass

class JSONProcessor(DataProcessor):
    def process_data(self, data: str) -> Dict[str, Any]:
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
    
    def get_format(self) -> str:
        return "JSON"

class LegacyXMLService:
    def parse_xml_string(self, xml_data: str) -> ET.Element:
        try:
            return ET.fromstring(xml_data)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {e}")
    
    def xml_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        result = {}
        if element.text and element.text.strip():
            if len(element) == 0:
                return element.text.strip()
        
        for child in element:
            child_data = self.xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        for attr_name, attr_value in element.attrib.items():
            result[f"@{attr_name}"] = attr_value
        
        return result

class XMLBridge(DataProcessor):
    def __init__(self, xml_service: Optional[LegacyXMLService] = None):
        self._xml_service = xml_service or LegacyXMLService()
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def process_data(self, data: str) -> Dict[str, Any]:
        data_hash = hash(data)
        
        if data_hash in self._cache:
            return self._cache[data_hash]
        
        try:
            xml_element = self._xml_service.parse_xml_string(data)
            result = self._xml_service.xml_to_dict(xml_element)
            
            if not isinstance(result, dict):
                result = {xml_element.tag: result}
            
            self._cache[data_hash] = result
            return result
            
        except Exception as e:
            raise ValueError(f"XML processing failed: {e}")
    
    def get_format(self) -> str:
        return "XML"
    
    def clear_cache(self) -> None:
        self._cache.clear()

class DataProcessingManager:
    def __init__(self):
        self._processors: List[DataProcessor] = []
    
    def add_processor(self, processor: DataProcessor) -> None:
        self._processors.append(processor)
    
    def process_all(self, data_sources: List[tuple]) -> Dict[str, Dict[str, Any]]:
        results = {}
        
        for data, expected_format in data_sources:
            for processor in self._processors:
                if processor.get_format().lower() == expected_format.lower():
                    try:
                        results[f"{expected_format}_data"] = processor.process_data(data)
                        break
                    except ValueError as e:
                        results[f"{expected_format}_error"] = str(e)
        
        return results

if __name__ == "__main__":
    json_data = '{"name": "John", "age": 30, "city": "New York"}'
    xml_data = '''<person id="123">
        <name>Jane</name>
        <age>25</age>
        <city>Boston</city>
    </person>'''
    
    manager = DataProcessingManager()
    manager.add_processor(JSONProcessor())
    manager.add_processor(XMLBridge())
    
    data_sources = [
        (json_data, "JSON"),
        (xml_data, "XML")
    ]
    
    results = manager.process_all(data_sources)
    
    for key, value in results.items():
        print(f"{key}: {value}")
    
    xml_bridge = XMLBridge()
    xml_bridge.clear_cache()