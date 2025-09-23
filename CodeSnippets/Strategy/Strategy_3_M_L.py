# Strategy Pattern Implementation in Python
class Context:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def execute(self, input_data):
        return self.strategy.execute(input_data)

class Strategy1:
    def execute(self, input_data):
        return input_data * 2

class Strategy2:
    def execute(self, input_data):
        return input_data + 3

def main():
    # Create an instance of the Context class with a specific strategy
    context = Context(Strategy1())
    
    # Execute the strategy on some input data
    result = context.execute(5)
    print(result) # Output: 10
    
    # Change the strategy and execute again
    context.strategy = Strategy2()
    result = context.execute(5)
    print(result) # Output: 8

if __name__ == "__main__":
    main()