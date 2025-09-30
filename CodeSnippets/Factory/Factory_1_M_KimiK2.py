from abc import ABC, abstractmethod

class Transport(ABC):
    @abstractmethod
    def deliver(self):
        pass

class Truck(Transport):
    def deliver(self):
        return "Delivering by land"

class Ship(Transport):
    def deliver(self):
        return "Delivering by sea"

class Drone(Transport):
    def deliver(self):
        return "Delivering by air"

class LogisticsCenter:
    def create_transport(self, transport_type):
        if transport_type == "truck":
            return Truck()
        elif transport_type == "ship":
            return Ship()
        elif transport_type == "drone":
            return Drone()
        else:
            raise ValueError("Unknown transport type")

class OverseasLogisticsCenter(LogisticsCenter):
    def create_transport(self, transport_type):
        if transport_type == "truck":
            raise ValueError("Truck not supported for overseas")
        return super().create_transport(transport_type)

if __name__ == "__main__":
    center = LogisticsCenter()
    overseas = OverseasLogisticsCenter()

    for t in ["truck", "ship", "drone"]:
        trans = center.create_transport(t)
        print(f"{t}: {trans.deliver()}")

    print("Overseas center:")
    for t in ["ship", "drone"]:
        trans = overseas.create_transport(t)
        print(f"{t}: {trans.deliver()}")