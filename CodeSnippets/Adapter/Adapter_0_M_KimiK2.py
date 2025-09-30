class EuropeanSocket:
    def plug_in_european(self):
        return "220V European power connected"

class USASocketInterface:
    def supply_power(self):
        raise NotImplementedError

class EuropeanToUSAPowerConnector(USASocketInterface):
    def __init__(self, european_socket):
        self._european_socket = european_socket
    
    def supply_power(self):
        power = self._european_socket.plug_in_european()
        return f"{power} → converted to 110V USA standard"

class USADevice:
    def __init__(self, socket):
        self._socket = socket
    
    def operate(self):
        try:
            power = self._socket.supply_power()
            print(f"Device running on: {power}")
        except Exception as e:
            print(f"Power connection failed: {e}")

if __name__ == "__main__":
    european_source = EuropeanSocket()
    connector = EuropeanToUSAPowerConnector(european_source)
    
    laptop = USADevice(connector)
    laptop.operate()