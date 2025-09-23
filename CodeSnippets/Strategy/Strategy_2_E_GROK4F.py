from abc import ABC, abstractmethod

class RoutingApproach(ABC):
    @abstractmethod
    def compute_route(self, origin, destination):
        pass

class DirectApproach(RoutingApproach):
    def compute_route(self, origin, destination):
        return ord(destination) - ord(origin)

class CyclingApproach(RoutingApproach):
    def compute_route(self, origin, destination):
        return (ord(destination) - ord(origin)) * 2

class RoutingCoordinator:
    def __init__(self, approach: RoutingApproach):
        self.approach = approach

    def get_route_length(self, origin, destination):
        return self.approach.compute_route(origin, destination)

if __name__ == "__main__":
    coord = RoutingCoordinator(DirectApproach())
    print(coord.get_route_length('A', 'D'))  # 3
    coord = RoutingCoordinator(CyclingApproach())
    print(coord.get_route_length('A', 'D'))  # 6