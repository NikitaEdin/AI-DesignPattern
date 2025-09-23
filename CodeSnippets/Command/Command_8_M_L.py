class MyCommand(object):
    def __init__(self, receiver, args):
        self.receiver = receiver
        self.args = args

    def execute(self):
        return self.receiver.do_something(*self.args)

class Receiver(object):
    def do_something(self, arg1, arg2):
        # Do something with the arguments
        pass

def main():
    receiver = Receiver()
    command = MyCommand(receiver, ("arg1", "arg2"))
    result = command.execute()
    print("Result:", result)

if __name__ == "__main__":
    main()