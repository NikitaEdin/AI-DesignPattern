class EuropeanSocket:
    def provide_230v(self):
        return 230

class UsbCharger:
    def charge(self, voltage):
        if voltage != 5:
            raise ValueError("Expected 5V")
        print("Charging at 5V")

class PowerConverter:
    def __init__(self, socket):
        self._socket = socket
    
    def charge(self, voltage=None):
        raw = self._socket.provide_230v()
        converted = raw // 46
        UsbCharger().charge(converted)

if __name__ == "__main__":
    socket = EuropeanSocket()
    converter = PowerConverter(socket)
    converter.charge()