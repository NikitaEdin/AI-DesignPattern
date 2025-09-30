class Mode:
    def execute(self, context): pass

class Walk(Mode):
    def execute(self, context):
        print("Walking")
        context.current = Run()

class Run(Mode):
    def execute(self, context):
        print("Running")
        context.current = Walk()

class Robot:
    def __init__(self):
        self.current = Walk()
    
    def action(self):
        self.current.execute(self)

if __name__ == "__main__":
    bot = Robot()
    for _ in range(4):
        bot.action()