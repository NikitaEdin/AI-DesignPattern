class Command(object):
    def execute(self):
        raise NotImplementedError()

class ConcreteCommand(Command):
    def __init__(self, receiver):
        self._receiver = receiver

    def execute(self):
        self._receiver.do_something()

class Invoker(object):
    def __init__(self, command):
        self._command = command

    def call_execute(self):
        self._command.execute()

if __name__ == "__main__":
    receiver = Receiver()
    concrete_command = ConcreteCommand(receiver)
    invoker = Invoker(concrete_command)
    invoker.call_execute()