class OldPrinter:
    def old_print(self, text):
        print(f"Old: {text}")

class ModernPrinter:
    def print(self, text):
        print(f"Modern: {text}")

class CompatibilityLayer:
    def __init__(self, old_device):
        self.old_device = old_device
    
    def print(self, text):
        self.old_device.old_print(text)

if __name__ == "__main__":
    old = OldPrinter()
    compatibility = CompatibilityLayer(old)
    
    modern = ModernPrinter()
    
    modern.print("Hello")
    compatibility.print("Hello")