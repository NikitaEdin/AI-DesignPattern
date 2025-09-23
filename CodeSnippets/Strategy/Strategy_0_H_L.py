class Context:
      def __init__(self, strategy):
          self._strategy = strategy
  
      def do_algorithm(self, input):
          return self._strategy.do_algorithm(input)
  
class StrategyA:
    def do_algorithm(self, input):
        # Implement the algorithm for Strategy A here
        return input * 2

class StrategyB:
    def do_algorithm(self, input):
        # Implement the algorithm for Strategy B here
        return input + 3

# Usage example
if __name__ == "__main__":
    context = Context(StrategyA())
    result = context.do_algorithm(10)
    print(result) # prints 20
  
    context = Context(StrategyB())
    result = context.do_algorithm(10)
    print(result) # prints 13