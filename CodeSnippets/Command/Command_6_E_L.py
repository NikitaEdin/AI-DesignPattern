```python
class Receiver:
    def do_something(self):
        print("Receiver: Doing something")

class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()

class Invoker:
    def __init__(self, command):
        self.command = command

    def call(self):
        self.command.execute()

# Usage example
receiver = Receiver()
invoker = Invoker(Command(receiver))
invoker.call()
         ```