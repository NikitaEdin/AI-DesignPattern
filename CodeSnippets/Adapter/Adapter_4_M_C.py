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

class DocumentManager:
    def __init__(self):
        self.printers = []
    
    def add_printer(self, printer):
        self.printers.append(printer)
    
    def print_all(self, document):
        results = []
        for printer in self.printers:
            result = printer.print_document(document)
            results.append(result)
        return results

if __name__ == "__main__":
    legacy = LegacyPrinter()
    modern = ModernPrinter()
    
    bridge = PrinterBridge(legacy)
    
    manager = DocumentManager()
    manager.add_printer(modern)
    manager.add_printer(bridge)
    
    results = manager.print_all("Important Document")
    for result in results:
        print(result)
    
    print(f"Bridge errors: {bridge.get_error_count()}")
    
    bridge.print_document("")
    print(f"Bridge errors after invalid input: {bridge.get_error_count()}")