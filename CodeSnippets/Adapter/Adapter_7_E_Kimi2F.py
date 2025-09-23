class EuropeanPlug:
    def power_240v(self):
        return "240V power"

class USASocket:
    def power_120v(self):
        return "120V power"

class SocketWrapper:
    def __init__(self, plug):
        self.plug = plug
    def power_120v(self):
        return self.plug.power_240v() + " adapted to 120V"

if __name__ == "__main__":
    eu_plug = EuropeanPlug()
    wrapper = SocketWrapper(eu_plug)
    print(wrapper.power_120v())