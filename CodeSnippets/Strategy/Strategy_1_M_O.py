from abc import ABC, abstractmethod
from typing import Optional, Dict, Tuple

class CalculatorError(Exception):
    pass

class DiscountCalculator(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        raise NotImplementedError
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError
    def key(self) -> str:
        return f"{type(self).__name__}:{id(self)}"

class NoDiscount(DiscountCalculator):
    def calculate(self, amount: float) -> float:
        if amount < 0:
            raise CalculatorError("negative amount")
        return round(amount, 2)
    def label(self) -> str:
        return "no_discount"

class PercentageDiscount(DiscountCalculator):
    def __init__(self, percent: float):
        if not (0 <= percent <= 100):
            raise ValueError("percent must be between 0 and 100")
        self.percent = percent
    def calculate(self, amount: float) -> float:
        if amount < 0:
            raise CalculatorError("negative amount")
        return round(amount * (1 - self.percent / 100.0), 2)
    def label(self) -> str:
        return f"percent_{int(self.percent)}"

class ThresholdDiscount(DiscountCalculator):
    def __init__(self, threshold: float, discount: float):
        if threshold < 0 or discount < 0:
            raise ValueError("threshold and discount must be non-negative")
        self.threshold = threshold
        self.discount = discount
    def calculate(self, amount: float) -> float:
        if amount < 0:
            raise CalculatorError("negative amount")
        if amount >= self.threshold:
            return round(max(0.0, amount - self.discount), 2)
        return round(amount, 2)
    def label(self) -> str:
        return f"threshold_{int(self.threshold)}_disc_{int(self.discount)}"

class FaultyCalculator(DiscountCalculator):
    def calculate(self, amount: float) -> float:
        raise CalculatorError("intentional failure")
    def label(self) -> str:
        return "faulty"

class OrderProcessor:
    def __init__(self, calculator: DiscountCalculator, fallback: Optional[DiscountCalculator] = None):
        if not isinstance(calculator, DiscountCalculator):
            raise TypeError("calculator must implement DiscountCalculator")
        self._calculator = calculator
        self._fallback = fallback or NoDiscount()
        self._cache: Dict[Tuple[int, float], float] = {}
    def set_calculator(self, calculator: DiscountCalculator):
        if not isinstance(calculator, DiscountCalculator):
            raise TypeError("calculator must implement DiscountCalculator")
        self._calculator = calculator
    def process(self, amount: float) -> float:
        rounded_amount = round(amount, 2)
        cache_key = (id(self._calculator), rounded_amount)
        if cache_key in self._cache:
            return self._cache[cache_key]
        try:
            result = round(self._calculator.calculate(amount), 2)
        except CalculatorError:
            result = round(self._fallback.calculate(amount), 2)
        self._cache[cache_key] = result
        return result

if __name__ == "__main__":
    proc = OrderProcessor(PercentageDiscount(10.0))
    print(proc.process(100.0))   # 90.0
    print(proc.process(100.0))   # cached -> 90.0
    proc.set_calculator(ThresholdDiscount(50.0, 15.0))
    print(proc.process(60.0))    # 45.0
    proc.set_calculator(FaultyCalculator())
    print(proc.process(200.0))   # fallback -> 200.0