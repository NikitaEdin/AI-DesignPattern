class LegacyPrinter:
    def old_print(self, text):
        return f"Legacy output: {text.upper()}"

class ModernPrinter:
    def print_document(self, content):
        return f"Modern print: {content}"

class PrinterBridge:
    def __init__(self, legacy_printer):
        self.legacy_system = legacy_printer
        self._error_count = 0
    
    def print_document(self, content):
        try:
            if not content or not isinstance(content, str):
                raise ValueError("Invalid content provided")
            result = self.legacy_system.old_print(content)
            self._error_count = 0
            return result
        except Exception as e:
            self._error_count += 1
            if self._error_count > 3:
                return "System temporarily unavailable"
            return f"Error: {str(e)}"
    
    def get_status(self):
        return f"Bridge active, errors: {self._error_count}"

def process_documents(printer, documents):
    results = []
    for doc in documents:
        results.append(printer.print_document(doc))
    return results

if __name__ == "__main__":
    legacy = LegacyPrinter()
    modern = ModernPrinter()
    bridge = PrinterBridge(legacy)
    
    documents = ["Hello World", "Python Code", "Design Patterns"]
    
    print("Modern printer:")
    for result in process_documents(modern, documents):
        print(result)
    
    print("\nLegacy printer via bridge:")
    for result in process_documents(bridge, documents):
        print(result)
    
    print(f"\nBridge status: {bridge.get_status()}")
    
    print(f"\nError handling test: {bridge.print_document('')}")