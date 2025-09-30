class OldPrinter:
    def old_print(self, text):
        return f"Old: {text}"

class ModernPrinter:
    def print(self, text):
        return f"Modern: {text}"

class Bridge:
    def __init__(self, old):
        self.old = old
    
    def print(self, text):
        return self.old.old_print(text)

if __name__ == "__main__":
    old = OldPrinter()
    bridge = Bridge(old)
    print(bridge.print("Hello"))