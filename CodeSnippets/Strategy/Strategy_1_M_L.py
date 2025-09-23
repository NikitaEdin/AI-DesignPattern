class Strategy:
    def __init__(self, name):
        self.name = name
    
    def execute(self):
        print("Executing strategy", self.name)

class ConcreteStrategyA(Strategy):
    def execute(self):
        super().execute()
        print("Executing strategy A")

class ConcreteStrategyB(Strategy):
    def execute(self):
        super().execute()
        print("Executing strategy B")

def main():
    context = Strategy("context")
    context.execute()

if __name__ == "__main__":
    main()