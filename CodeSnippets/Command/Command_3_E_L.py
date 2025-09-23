# Command Pattern - Implementation in Python

class Receiver:
    def do_something(self):
        print("Receiver: Did something")

class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()

# Client
def main():
    receiver = Receiver()
    command = Command(receiver)
    command.execute()

if __name__ == "__main__":
    main()