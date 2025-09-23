class EuroPlug:
    def get_230v(self):
        return 230

class UsPlug:
    def use_110v(self):
        raise NotImplementedError

class VoltageConverter(UsPlug):
    def __init__(self, euro_source):
        self.euro_source = euro_source
    
    def use_110v(self):
        voltage = self.euro_source.get_230v()
        return voltage * 110 / 230

if __name__ == "__main__":
    european = EuroPlug()
    converter = VoltageConverter(european)
    print(f"US device receives: {converter.use_110v():.1f}V")