# Command Pattern in Python
# The Command pattern allows an object to encapsulate all information needed to perform an action or trigger an event.

class Receiver:
    def do_something(self):
        print("Receiver: Working...")

class Command:
    def __init__(self, receiver):
        self._receiver = receiver
    
    def execute(self):
        self._receiver.do_something()

# The Invoker class is responsible for executing the command
class Invoker:
    def __init__(self, command):
        self._command = command
    
    def do_something(self):
        self._command.execute()

# Example usage
def main():
    receiver = Receiver()
    invoker = Invoker(Command(receiver))
    invoker.do_something()

if __name__ == "__main__":
    main()