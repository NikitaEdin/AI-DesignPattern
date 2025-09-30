class DataReader:
    def fetch(self, source):
        return f"Data from {source}"

class DataDeveloper:
    def transform(self, data):
        return data.upper()

class DataWriter:
    def write(self, data, destination):
        return f"Wrote {data} to {destination}"

class DataManager:
    def __init__(self):
        self._reader = DataReader()
        self._developer = DataDeveloper()
        self._writer = DataWriter()
    
    def process(self, source, destination):
        try:
            data = self._reader.fetch(source)
            data = self._developer.transform(data)
            return self._writer.write(data, destination)
        except Exception as e:
            raise RuntimeError(f"Processing failed: {e}")

if __name__ == "__main__":
    manager = DataManager()
    print(manager.process("file.txt", "report.txt"))