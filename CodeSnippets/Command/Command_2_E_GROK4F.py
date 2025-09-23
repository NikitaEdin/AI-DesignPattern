class Door:
    def open(self):
        print("Door opened")

class OpenOperation:
    def __init__(self, door):
        self.door = door

    def execute(self):
        self.door.open()

class Switch:
    def __init__(self):
        self.current_operation = None

    def set_operation(self, operation):
        self.current_operation = operation

    def activate(self):
        self.current_operation.execute()

if __name__ == "__main__":
    door = Door()
    switch = Switch()
    switch.set_operation(OpenOperation(door))
    switch.activate()