from typing import Callable, List

class Context:
    def __init__(self, strategy: Callable[[int], int]) -> None:
        self.strategy = strategy

    def execute(self, input_value: int) -> int:
        return self.strategy(input_value)

class Strategy1:
    def __call__(self, input_value: int) -> int:
        return input_value * 2

class Strategy2:
    def __call__(self, input_value: int) -> int:
        return input_value + 3

def main() -> None:
    context = Context(Strategy1())
    print(context.execute(5))  # prints 10

    context = Context(Strategy2())
    print(context.execute(5))  # prints 8

if __name__ == "__main__":
    main()