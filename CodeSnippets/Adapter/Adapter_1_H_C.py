from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol
import json
import xml.etree.ElementTree as ET


class DataTarget(ABC):
    @abstractmethod
    def process_data(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_format(self) -> str:
        pass


class LegacyXMLService:
    def __init__(self, xml_data: str):
        self.xml_content = xml_data
        self._root = None
    
    def parse_xml_content(self) -> ET.Element:
        if self._root is None:
            self._root = ET.fromstring(self.xml_content)
        return self._root
    
    def extract_node_value(self, xpath: str) -> str:
        root = self.parse_xml_content()
        element = root.find(xpath)
        return element.text if element is not None else ""
    
    def get_all_attributes(self, node_name: str) -> List[Dict[str, str]]:
        root = self.parse_xml_content()
        return [elem.attrib for elem in root.findall(f".//{node_name}")]


class OldCSVProcessor:
    def __init__(self, csv_content: str, delimiter: str = ","):
        self.raw_data = csv_content
        self.delimiter = delimiter
        self._parsed_rows = None
    
    def get_csv_rows(self) -> List[List[str]]:
        if self._parsed_rows is None:
            lines = self.raw_data.strip().split('\n')
            self._parsed_rows = [line.split(self.delimiter) for line in lines]
        return self._parsed_rows
    
    def fetch_column_data(self, column_index: int) -> List[str]:
        rows = self.get_csv_rows()
        return [row[column_index] if column_index < len(row) else "" for row in rows]


class XMLServiceBridge(DataTarget):
    def __init__(self, legacy_service: LegacyXMLService, field_mapping: Optional[Dict[str, str]] = None):
        self._service = legacy_service
        self._mapping = field_mapping or {}
        self._cached_result = None
    
    def process_data(self) -> Dict[str, Any]:
        if self._cached_result is not None:
            return self._cached_result
        
        try:
            result = {}
            root = self._service.parse_xml_content()
            
            for child in root:
                field_name = self._mapping.get(child.tag, child.tag)
                if child.text:
                    result[field_name] = self._convert_value(child.text)
                
                if child.attrib:
                    for attr_key, attr_value in child.attrib.items():
                        mapped_key = f"{field_name}_{attr_key}"
                        result[mapped_key] = self._convert_value(attr_value)
            
            self._cached_result = result
            return result
        except ET.ParseError:
            return {"error": "Invalid XML format"}
    
    def _convert_value(self, value: str) -> Any:
        value = value.strip()
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        try:
            return int(value) if '.' not in value else float(value)
        except ValueError:
            return value
    
    def get_format(self) -> str:
        return "xml"


class CSVProcessorBridge(DataTarget):
    def __init__(self, csv_processor: OldCSVProcessor, headers: Optional[List[str]] = None):
        self._processor = csv_processor
        self._headers = headers
        self._cached_result = None
    
    def process_data(self) -> Dict[str, Any]:
        if self._cached_result is not None:
            return self._cached_result
        
        try:
            rows = self._processor.get_csv_rows()
            if not rows:
                return {"error": "No data available"}
            
            headers = self._headers or [f"col_{i}" for i in range(len(rows[0]))]
            data_rows = rows[1:] if self._headers is None and len(rows) > 1 else rows
            
            result = {
                "records": [],
                "total_count": len(data_rows)
            }
            
            for row in data_rows:
                record = {}
                for i, header in enumerate(headers):
                    value = row[i] if i < len(row) else ""
                    record[header] = self._parse_csv_value(value)
                result["records"].append(record)
            
            self._cached_result = result
            return result
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}
    
    def _parse_csv_value(self, value: str) -> Any:
        value = value.strip().strip('"')
        if not value:
            return None
        try:
            return int(value) if '.' not in value else float(value)
        except ValueError:
            return value
    
    def get_format(self) -> str:
        return "csv"


class UnifiedDataProcessor:
    def __init__(self):
        self._processors: List[DataTarget] = []
    
    def add_source(self, processor: DataTarget):
        self._processors.append(processor)
    
    def process_all(self) -> Dict[str, Any]:
        results = {}
        for i, processor in enumerate(self._processors):
            format_type = processor.get_format()
            key = f"{format_type}_{i}" if format_type in results else format_type
            results[key] = processor.process_data()
        return results


if __name__ == "__main__":
    xml_data = """<root>
        <user id="123" active="true">John Doe</user>
        <age>30</age>
        <score>95.5</score>
    </root>"""
    
    csv_data = """name,age,city
John,25,New York
Jane,30,London
Bob,35,Paris"""
    
    legacy_xml = LegacyXMLService(xml_data)
    old_csv = OldCSVProcessor(csv_data)
    
    xml_bridge = XMLServiceBridge(legacy_xml, {"user": "full_name"})
    csv_bridge = CSVProcessorBridge(old_csv, ["name", "age", "city"])
    
    processor = UnifiedDataProcessor()
    processor.add_source(xml_bridge)
    processor.add_source(csv_bridge)
    
    results = processor.process_all()
    print(json.dumps(results, indent=2))