class DataReader:
    def read(self, source):
        return f"Data from {source}"

class DataProcessor:
    def process(self, data):
        return data.upper()

class DataWriter:
    def write(self, processed_data, destination):
        print(f"Writing to {destination}: {processed_data}")

class FileHandler:
    def __init__(self):
        self.reader = DataReader()
        self.processor = DataProcessor()
        self.writer = DataWriter()

    def handle_file(self, source, destination):
        data = self.reader.read(source)
        processed = self.processor.process(data)
        self.writer.write(processed, destination)

if __name__ == "__main__":
    handler = FileHandler()
    handler.handle_file("input.txt", "output.txt")