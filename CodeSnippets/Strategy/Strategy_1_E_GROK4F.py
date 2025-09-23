class DrivingCalculator:
    def estimate_time(self, distance):
        return distance / 60

class WalkingCalculator:
    def estimate_time(self, distance):
        return distance / 5

class TripPlanner:
    def __init__(self):
        self._calculator = None

    def set_transport(self, calculator):
        self._calculator = calculator

    def plan_trip(self, distance):
        return self._calculator.estimate_time(distance) if self._calculator else None

if __name__ == "__main__":
    planner = TripPlanner()
    planner.set_transport(DrivingCalculator())
    print(planner.plan_trip(60))
    planner.set_transport(WalkingCalculator())
    print(planner.plan_trip(5))