class EuropeanSocket:
    def plug_220v(self):
        return "220 volts AC"

class UsDevice:
    def plug_110v(self):
        return "110 volts AC"

class PowerBridge:
    def __init__(self, euro_socket):
        self._euro_socket = euro_socket
    
    def plug_110v(self):
        try:
            power = self._euro_socket.plug_220v()
            return power.replace("220", "110")
        except Exception as e:
            return f"Power failure: {e}"

if __name__ == "__main__":
    euro = EuropeanSocket()
    blender = UsDevice()
    print("Direct device:", blender.plug_110v())
    
    bridge = PowerBridge(euro)
    print("Via bridge:", bridge.plug_110v())