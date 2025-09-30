class EuropeanSocket:
    def plug_in_220v(self):
        return "220V power connected"

class USDevice:
    def connect_110v(self):
        return "110V device working"

class PowerConnector:
    def __init__(self, european_socket):
        self.european_socket = european_socket
    
    def connect_110v(self):
        power = self.european_socket.plug_in_220v()
        return f"Converted: {power} -> 110V device powered"

if __name__ == "__main__":
    socket = EuropeanSocket()
    connector = PowerConnector(socket)
    device = USDevice()
    
    print(device.connect_110v())
    print(connector.connect_110v())