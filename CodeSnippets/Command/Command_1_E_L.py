class Invoker:
    def __init__(self):
        self.commands = []
    
    def add_command(self, command):
        self.commands.append(command)
    
    def execute_all(self):
        for command in self.commands:
            command.execute()
    
class Receiver:
    def __init__(self):
        self.state = 0
    
    def do_something(self):
        print("I've done something!")
    
    def get_state(self):
        return self.state

class Command:
    def __init__(self, receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.do_something()

if __name__ == "__main__":
    # Create a receiver and an invoker
    receiver = Receiver()
    invoker = Invoker()
    
    # Create a command and add it to the invoker's list of commands
    command = Command(receiver)
    invoker.add_command(command)
    
    # Execute all the commands in the invoker's list
    invoker.execute_all()
    
    # Print the receiver's state
    print(receiver.get_state())