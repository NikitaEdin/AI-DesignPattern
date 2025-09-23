# Command Pattern

class Receiver:
    def do_something(self):
        print("Receiver: Did something")

class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()

class ConcreteCommandA(Command):
    def execute(self):
        super().execute()
        print("ConcreteCommandA: Did something else")

class ConcreteCommandB(Command):
    def execute(self):
        super().execute()
        print("ConcreteCommandB: Did something other")

# Usage Example
def main():
    receiver = Receiver()
    command_a = ConcreteCommandA(receiver)
    command_b = ConcreteCommandB(receiver)

    command_a.execute()
    print("=" * 30)
    command_b.execute()

if __name__ == "__main__":
    main()