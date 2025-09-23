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
    
    def do_something(self, arg1, arg2):
        self.state += 1
        print(f"Receiver: state updated to {self.state}")
        
class ConcreteCommand(object):
    def __init__(self, receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.do_something("arg1", "arg2")

if __name__ == "__main__":
    receiver = Receiver()
    command = ConcreteCommand(receiver)
    invoker = Invoker()
    invoker.add_command(command)
    invoker.execute_all()