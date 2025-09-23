class OldPrinter:
    def __init__(self, name):
        self.name = name
    
    def print_document(self, text):
        return f"[{self.name}] Printing: {text}"

class ModernDevice:
    def __init__(self, model):
        self.model = model
    
    def send_to_device(self, content, format_type="PDF"):
        if not content:
            raise ValueError("Content cannot be empty")
        return f"Device {self.model} processing {format_type}: {content}"

class PrinterBridge:
    def __init__(self, old_printer):
        self._old_printer = old_printer
        self._print_count = 0
    
    def send_to_device(self, content, format_type="TXT"):
        if not content:
            raise ValueError("Content cannot be empty")
        
        self._print_count += 1
        converted_content = f"[{format_type}] {content}"
        result = self._old_printer.print_document(converted_content)
        return f"{result} (Job #{self._print_count})"
    
    def get_job_count(self):
        return self._print_count

def process_documents(devices, document):
    results = []
    for device in devices:
        try:
            result = device.send_to_device(document, "PDF")
            results.append(result)
        except ValueError as e:
            results.append(f"Error: {e}")
    return results

if __name__ == "__main__":
    legacy_printer = OldPrinter("HP LaserJet 1990")
    modern_printer = ModernDevice("Canon MX920")
    bridged_printer = PrinterBridge(legacy_printer)
    
    devices = [modern_printer, bridged_printer]
    document = "Important business report"
    
    results = process_documents(devices, document)
    for result in results:
        print(result)
    
    print(f"Legacy printer jobs processed: {bridged_printer.get_job_count()}")