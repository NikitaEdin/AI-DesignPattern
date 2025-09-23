class TravelMethod:
    def travel(self, distance):
        pass

class CarTravel(TravelMethod):
    def travel(self, distance):
        return f"Driving {distance} km by car"

class BikeTravel(TravelMethod):
    def travel(self, distance):
        return f"Cycling {distance} km by bike"

class TripPlanner:
    def __init__(self):
        self.method = None

    def set_method(self, method):
        self.method = method

    def plan_trip(self, distance):
        if self.method:
            return self.method.travel(distance)
        return "No travel method set"

if __name__ == "__main__":
    planner = TripPlanner()
    planner.set_method(CarTravel())
    print(planner.plan_trip(100))
    planner.set_method(BikeTravel())
    print(planner.plan_trip(100))