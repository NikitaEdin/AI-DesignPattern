class LegacyPrinter:
    def old_print(self, text: str) -> str:
        return f"Legacy: {text}"

class ModernRenderer:
    def render(self, content: str) -> str:
        return f"Rendered: {content}"

class PrinterBridge:
    def __init__(self, renderer: ModernRenderer):
        self.renderer = renderer

    def old_print(self, text: str) -> str:
        try:
            return self.renderer.render(text)
        except Exception as e:
            return f"Error: {e}"

def main():
    legacy = LegacyPrinter()
    modern = ModernRenderer()
    bridge = PrinterBridge(modern)

    print(legacy.old_print("Hello"))
    print(bridge.old_print("Hello"))

if __name__ == "__main__":
    main()