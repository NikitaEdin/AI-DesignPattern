class OldPrinter:
    def old_print(self, text):
        return f"[OLD FORMAT] {text}"

class ModernPrinter:
    def print_document(self, content):
        return f"Modern Print: {content}"

class PrinterBridge:
    def __init__(self, old_printer):
        self._old_printer = old_printer
        self._error_count = 0
    
    def print_document(self, content):
        try:
            if not content or not isinstance(content, str):
                raise ValueError("Invalid content provided")
            result = self._old_printer.old_print(content)
            return result
        except Exception as e:
            self._error_count += 1
            return f"Error: {str(e)}"
    
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
    old_system = OldPrinter()
    bridge = PrinterBridge(old_system)
    modern_system = ModernPrinter()
    
    processor_old = DocumentProcessor(bridge)
    processor_modern = DocumentProcessor(modern_system)
    
    documents = ["Report 1", "Invoice 2", ""]
    
    print("Using bridged old system:")
    old_results = processor_old.process_documents(documents)
    for result in old_results:
        print(result)
    
    print(f"Errors encountered: {bridge.get_error_count()}")
    
    print("\nUsing modern system:")
    modern_results = processor_modern.process_documents(documents[:2])
    for result in modern_results:
        print(result)