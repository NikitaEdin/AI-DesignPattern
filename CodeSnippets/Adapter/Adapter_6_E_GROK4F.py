class LegacyProcessor:
    def process_data(self, value):
        return f"Processed: {value.upper()}"

class ModernInterface:
    def handle_input(self, data):
        pass

class CompatibilityLayer(ModernInterface):
    def __init__(self, processor):
        self.processor = processor

    def handle_input(self, data):
        return self.processor.process_data(data)

if __name__ == "__main__":
    processor = LegacyProcessor()
    layer = CompatibilityLayer(processor)
    result = layer.handle_input("hello")
    print(result)