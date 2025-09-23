class Receiver:
    def do_something(self):
        print("Receiver: Doing something...")

class CommandBase:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        raise NotImplementedError

class ConcreteCommandA(CommandBase):
    def execute(self):
        print("ConcreteCommandA: Executing...")
        self.receiver.do_something()

class ConcreteCommandB(CommandBase):
    def execute(self):
        print("ConcreteCommandB: Executing...")
        self.receiver.do_something()

class Invoker:
    def __init__(self, command):
        self.command = command

    def invoke(self):
        self.command.execute()

if __name__ == "__main__":
    receiver = Receiver()
    command1 = ConcreteCommandA(receiver)
    command2 = ConcreteCommandB(receiver)

    invoker1 = Invoker(command1)
    invoker1.invoke()

    invoker2 = Invoker(command2)
    invoker2.invoke()