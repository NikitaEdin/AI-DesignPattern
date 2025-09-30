class EuropeanSocket:
    def plug_220v(self):
        return "220V power supplied"


class USDevice:
    def operate(self, power):
        if power != "110V power supplied":
            raise ValueError("Device requires 110V")
        return "Device running on 110V"


class PowerConnector:
    def __init__(self, socket):
        self.socket = socket

    def provide_110v(self):
        raw_power = self.socket.plug_220v()
        if raw_power == "220V power supplied":
            return "110V power supplied"
        raise RuntimeError("Unsupported power")


if __name__ == "__main__":
    socket = EuropeanSocket()
    connector = PowerConnector(socket)
    device = USDevice()

    try:
        power = connector.provide_110v()
        result = device.operate(power)
        print(result)
    except Exception as e:
        print(f"Error: {e}")