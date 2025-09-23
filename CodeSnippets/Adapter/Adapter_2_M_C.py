class LegacyPrinter:
    def old_print(self, text):
        return f"[LEGACY] {text}"

class ModernPrinter:
    def print_document(self, content):
        return f"Modern Print: {content}"

class PrinterBridge:
    def __init__(self, legacy_printer):
        self._legacy_printer = legacy_printer
        self._error_count = 0
    
    def print_document(self, content):
        try:
            if not content or not isinstance(content, str):
                raise ValueError("Invalid content provided")
            result = self._legacy_printer.old_print(content)
            return result
        except Exception as e:
            self._error_count += 1
            return f"Error occurred: {str(e)}"
    
    def get_error_count(self):
        return self._error_count

class DocumentProcessor:
    def __init__(self, printer):
        self.printer = printer
    
    def process_documents(self, documents):
        results = []
        for doc in documents:
            result = self.printer.print_document(doc)
            results.append(result)
        return results

if __name__ == "__main__":
    legacy_system = LegacyPrinter()
    modern_system = ModernPrinter()
    
    bridge = PrinterBridge(legacy_system)
    
    processor1 = DocumentProcessor(modern_system)
    processor2 = DocumentProcessor(bridge)
    
    docs = ["Report 1", "Invoice 2", ""]
    
    modern_results = processor1.process_documents(docs)
    legacy_results = processor2.process_documents(docs)
    
    print("Modern printer results:")
    for result in modern_results:
        print(f"  {result}")
    
    print("\nLegacy printer results:")
    for result in legacy_results:
        print(f"  {result}")
    
    print(f"\nErrors encountered: {bridge.get_error_count()}")