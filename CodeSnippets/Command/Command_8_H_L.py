class Receiver:
    def do_something(self):
        print("Receiver: Something done")

class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()

class Invoker:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def run_all(self):
        for command in self.commands:
            command.execute()

if __name__ == "__main__":
    receiver = Receiver()
    command1 = Command(receiver)
    invoker = Invoker()
    invoker.add_command(command1)
    invoker.run_all()