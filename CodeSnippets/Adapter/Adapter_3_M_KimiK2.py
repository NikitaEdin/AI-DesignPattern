class EuropeanSocket:
    def supply_power(self):
        return "230V European power"


class USDevice:
    def operate(self, power):
        if "110V" in power:
            print("Device running on US power")
        else:
            raise ValueError("Incorrect voltage")


class PowerConnector:
    def __init__(self, socket):
        self.socket = socket

    def provide_us_power(self):
        euro_power = self.socket.supply_power()
        if "230V" in euro_power:
            return "110V US power converted from " + euro_power
        raise ValueError("Unknown power source")


if __name__ == "__main__":
    socket = EuropeanSocket()
    connector = PowerConnector(socket)
    device = USDevice()
    try:
        us_power = connector.provide_us_power()
        device.operate(us_power)
    except ValueError as e:
        print("Error:", e)