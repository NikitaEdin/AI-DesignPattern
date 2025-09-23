class UndoableCommand:
    def execute(self):
        raise NotImplementedError()

    def undo(self):
        raise NotImplementedError()

class ConcreteUndoableCommand1(UndoableCommand):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()

    def undo(self):
        self.receiver.undo_something()

class ConcreteUndoableCommand2(UndoableCommand):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_another_thing()

    def undo(self):
        self.receiver.undo_another_thing()

class Receiver:
    def do_something(self):
        print("Doing something...")

    def undo_something(self):
        print("Undoing something...")

    def do_another_thing(self):
        print("Doing another thing...")

    def undo_another_thing(self):
        print("Undoing another thing...")

if __name__ == "__main__":
    receiver = Receiver()
    command1 = ConcreteUndoableCommand1(receiver)
    command2 = ConcreteUndoableCommand2(receiver)
    command1.execute()
    command2.execute()
    command1.undo()
    command2.undo()