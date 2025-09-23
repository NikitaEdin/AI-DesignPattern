class Receiver:
    def action(self):
        print("Receiver action called")

class Command:
    def __init__(self, receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.action()

def main():
    receiver = Receiver()
    command = Command(receiver)
    command.execute()