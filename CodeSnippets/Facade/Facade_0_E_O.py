class SubsystemOne:
    def action(self):
        return "SubsystemOne action"

class SubsystemTwo:
    def operation(self):
        return "SubsystemTwo operation"

class SystemCoordinator:
    def __init__(self):
        self.part1 = SubsystemOne()
        self.part2 = SubsystemTwo()
    def run(self):
        r1 = self.part1.action()
        r2 = self.part2.operation()
        return f"Coordinated result: {r1} | {r2}"

if __name__ == "__main__":
    coordinator = SystemCoordinator()
    print(coordinator.run())