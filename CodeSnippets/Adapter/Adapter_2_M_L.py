class Target:
    def __init__(self):
        self.name = "Target"

    def do_something(self):
        print("Doing something on the target...")

class Adapter:
    def __init__(self, target):
        self.target = target

    def do_something(self):
        print("Before doing something on the target...")
        self.target.do_something()
        print("After doing something on the target...")

if __name__ == "__main__":
    # Create an instance of the target class
    target = Target()

    # Create an instance of the adapter class, passing in the target
    adapter = Adapter(target)

    # Call the do_something method on the adapter
    adapter.do_something()