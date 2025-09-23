from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union
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

class XMLProcessor(DataProcessor):
    def process_data(self, data: str) -> Dict[str, Any]:
        try:
            root = ET.fromstring(data)
            return self._xml_to_dict(root)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {e}")
    
    def get_format(self) -> str:
        return "XML"
    
    def _xml_to_dict(self, element) -> Dict[str, Any]:
        result = {}
        if element.text and element.text.strip():
            result['text'] = element.text.strip()
        
        for child in element:
            child_data = self._xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        result.update(element.attrib)
        return result

class LegacyCSVParser:
    def parse_csv_string(self, csv_data: str, delimiter: str = ',') -> List[List[str]]:
        lines = csv_data.strip().split('\n')
        return [line.split(delimiter) for line in lines]
    
    def get_parser_info(self) -> str:
        return "Legacy CSV Parser v1.0"

class CSVProcessorBridge(DataProcessor):
    def __init__(self, csv_parser: LegacyCSVParser, has_header: bool = True):
        self._parser = csv_parser
        self._has_header = has_header
        self._delimiter_map = {';': 'semicolon', ',': 'comma', '\t': 'tab'}
    
    def process_data(self, data: str) -> Dict[str, Any]:
        delimiter = self._detect_delimiter(data)
        try:
            rows = self._parser.parse_csv_string(data, delimiter)
            if not rows:
                return {"data": [], "metadata": {"rows": 0, "delimiter": delimiter}}
            
            if self._has_header and len(rows) > 1:
                headers = rows[0]
                data_rows = rows[1:]
                processed_data = [dict(zip(headers, row)) for row in data_rows]
            else:
                processed_data = [{"column_" + str(i): val for i, val in enumerate(row)} 
                                for row in rows]
            
            return {
                "data": processed_data,
                "metadata": {
                    "rows": len(processed_data),
                    "delimiter": self._delimiter_map.get(delimiter, delimiter),
                    "has_header": self._has_header
                }
            }
        except Exception as e:
            raise ValueError(f"CSV processing failed: {e}")
    
    def get_format(self) -> str:
        return f"CSV ({self._parser.get_parser_info()})"
    
    def _detect_delimiter(self, data: str) -> str:
        first_line = data.split('\n')[0] if data else ""
        delimiters = [',', ';', '\t']
        return max(delimiters, key=lambda d: first_line.count(d))

class UniversalDataProcessor:
    def __init__(self):
        self._processors: Dict[str, DataProcessor] = {}
    
    def register_processor(self, format_type: str, processor: DataProcessor):
        self._processors[format_type.upper()] = processor
    
    def process(self, data: str, format_type: str) -> Dict[str, Any]:
        processor = self._processors.get(format_type.upper())
        if not processor:
            raise ValueError(f"Unsupported format: {format_type}")
        
        result = processor.process_data(data)
        result["source_format"] = processor.get_format()
        return result

if __name__ == "__main__":
    universal_processor = UniversalDataProcessor()
    
    universal_processor.register_processor("JSON", JSONProcessor())
    universal_processor.register_processor("XML", XMLProcessor())
    universal_processor.register_processor("CSV", CSVProcessorBridge(LegacyCSVParser()))
    
    json_data = '{"name": "John", "age": 30, "skills": ["Python", "Java"]}'
    xml_data = '<person name="Alice"><age>25</age><city>NYC</city></person>'
    csv_data = 'name,age,role\nBob,35,Developer\nCarol,28,Designer'
    
    formats_and_data = [("JSON", json_data), ("XML", xml_data), ("CSV", csv_data)]
    
    for format_type, data in formats_and_data:
        try:
            result = universal_processor.process(data, format_type)
            print(f"{format_type} Result: {result}")
        except Exception as e:
            print(f"Error processing {format_type}: {e}")