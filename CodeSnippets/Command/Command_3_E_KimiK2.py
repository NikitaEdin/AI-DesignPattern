class Action:
    def execute(self): pass

class PrintAction(Action):
    def __init__(self, text):
        self.text = text
    def execute(self):
        print(self.text)

class Invoker:
    def __init__(self):
        self.actions = []
    def add(self, action):
        self.actions.append(action)
    def run(self):
        for action in self.actions:
            action.execute()

if __name__ == "__main__":
    invoker = Invoker()
    invoker.add(PrintAction("Hello"))
    invoker.add(PrintAction("World"))
    invoker.run()