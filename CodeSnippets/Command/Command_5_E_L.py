class Command:
    def execute(self):
        pass

class ConcreteCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()

class Receiver:
    def do_something(self):
        print("Received command!")

def main():
    # Create a concrete command and receiver
    command = ConcreteCommand(Receiver())

    # Execute the command
    command.execute()

if __name__ == "__main__":
    main()