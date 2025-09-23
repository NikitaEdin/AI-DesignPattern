class EuropeanPlug:
    def connect_220v(self):
        return "220V power"

class USPlug:
    def connect_110v(self):
        return "110V power"

class PowerConverter:
    def __init__(self, plug):
        self.plug = plug
    def connect_110v(self):
        return self.plug.connect_220v()

if __name__ == "__main__":
    eu_plug = EuropeanPlug()
    converter = PowerConverter(eu_plug)
    print(converter.connect_110v())