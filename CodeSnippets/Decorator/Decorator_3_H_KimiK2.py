import functools
import time
from typing import Protocol, runtime_checkable

@runtime_checkable
class CoffeeInterface(Protocol):
    def cost(self) -> float: ...
    def ingredients(self) -> str: ...

class BaseCoffee:
    def cost(self) -> float:
        return 2.0
    def ingredients(self) -> str:
        return "Coffee"

class BaseAdditive:
    def __init__(self, beverage: CoffeeInterface):
        self._beverage = beverage
    def cost(self) -> float:
        return self._beverage.cost()
    def ingredients(self) -> str:
        return self._beverage.ingredients()

class Milk(BaseAdditive):
    def cost(self) -> float:
        return super().cost() + 0.5
    def ingredients(self) -> str:
        return super().ingredients() + ", Milk"

class Sugar(BaseAdditive):
    def cost(self) -> float:
        return super().cost() + 0.3
    def ingredients(self) -> str:
        return super().ingredients() + ", Sugar"

class WhippedCream(BaseAdditive):
    def cost(self) -> float:
        return super().cost() + 0.8
    def ingredients(self) -> str:
        return super().ingredients() + ", Whipped Cream"

class LoggingEnhancement(BaseAdditive):
    def __init__(self, beverage: CoffeeInterface, log_function):
        super().__init__(beverage)
        self._log_function = log_function
    def cost(self) -> float:
        result = super().cost()
        self._log_function(f"Cost calculated: {result}")
        return result
    def ingredients(self) -> str:
        result = super().ingredients()
        self._log_function(f"Ingredients listed: {result}")
        return result

class AutoRetryEnhancement(BaseAdditive):
    def __init__(self, beverage: CoffeeInterface, max_retries: int = 3):
        super().__init__(beverage)
        self._max_retries = max_retries
    def cost(self) -> float:
        for attempt in range(self._max_retries):
            try:
                return super().cost()
            except Exception as e:
                if attempt == self._max_retries - 1:
                    raise
                time.sleep(0.1)
        return 0.0
    def ingredients(self) -> str:
        for attempt in range(self._max_retries):
            try:
                return super().ingredients()
            except Exception:
                time.sleep(0.1)
        return "Error retrieving ingredients"

def main():
    coffee = BaseCoffee()
    coffee = Milk(coffee)
    coffee = Sugar(coffee)
    coffee = WhippedCream(coffee)
    print(f"Beverage: {coffee.ingredients()}")
    print(f"Total Cost: ${coffee.cost():.2f}")
    def logger(message):
        print(f"[LOG] {message}")
    coffee = BaseCoffee()
    logged_coffee = LoggingEnhancement(Sugar(Milk(coffee)), logger)
    print(f"Logged Beverage: {logged_coffee.ingredients()}")
    print(f"Logged Cost: ${logged_coffee.cost():.2f}")
    coffee = BaseCoffee()
    resilient_coffee = AutoRetryEnhancement(Sugar(Milk(coffee)), max_retries=2)
    print(f"Resilient Beverage: {resilient_coffee.ingredients()}")
    print(f"Resilient Cost: ${resilient_coffee.cost():.2f}")

if __name__ == "__main__":
    main()