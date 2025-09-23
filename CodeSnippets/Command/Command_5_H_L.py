class Receiver:
    def do_something(self):
        print("Received command")

class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()

def main():
    receiver = Receiver()
    cmd = Command(receiver)
    cmd.execute()

if __name__ == "__main__":
    main()