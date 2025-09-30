from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def fetch_records(self) -> list[dict]:
        pass

class LegacyCsvReader(DataProcessor):
    def __init__(self, filename: str):
        self.filename = filename
    
    def fetch_records(self) -> list[dict]:
        try:
            with open(self.filename, 'r') as f:
                lines = f.read().strip().split('\n')
                headers = lines[0].split(',')
                return [dict(zip(headers, line.split(','))) for line in lines[1:]]
        except FileNotFoundError:
            return []

class JsonApiClient:
    def __init__(self, url: str):
        self.url = url
    
    def get_json_data(self) -> dict:
        return {"users": [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]}

class JsonToProcessorBridge(DataProcessor):
    def __init__(self, api_client: JsonApiClient):
        self.api_client = api_client
    
    def fetch_records(self) -> list[dict]:
        raw_data = self.api_client.get_json_data()
        return raw_data.get("users", [])

def main():
    csv_reader = LegacyCsvReader("data.csv")
    print("CSV Records:", csv_reader.fetch_records())
    
    api_client = JsonApiClient("https://api.example.com/users")
    bridge = JsonToProcessorBridge(api_client)
    print("JSON Records:", bridge.fetch_records())

if __name__ == "__main__":
    main()