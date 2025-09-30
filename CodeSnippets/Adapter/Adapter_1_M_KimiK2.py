import datetime

class EuropeanSocket:
    def plug_220v(self):
        return "220V AC"

class USASocket:
    def plug_110v(self):
        return "110V AC"

class SocketConverter:
    def __init__(self, european_socket):
        self._european_socket = european_socket

    def plug_110v(self):
        voltage = self._european_socket.plug_220v()
        if voltage != "220V AC":
            raise ValueError("Unsupported voltage")
        return "110V AC (converted from 220V)"

def main():
    eu_device = EuropeanSocket()
    converter = SocketConverter(eu_device)
    print("Device now provides:", converter.plug_110v())

if __name__ == "__main__":
    main()