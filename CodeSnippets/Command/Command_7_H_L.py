class MacroCommand:
    def __init__(self, *commands):
        self._commands = list(commands)
    
    def execute(self):
        for command in self._commands:
            command.execute()
            
class SimpleCommand:
    def __init__(self, receiver, action):
        self._receiver = receiver
        self._action = action
    
    def execute(self):
        getattr(self._receiver, self._action)()
        
class Receiver:
    def do_something(self):
        print("do something")
        
# Usage Example

command1 = SimpleCommand(Receiver(), "do_something")
command2 = MacroCommand(command1)
command2.execute()