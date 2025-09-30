from typing import Protocol
import statistics
import random

class PricingEngine(Protocol):
    def calculate(self, base_price: float, volatility_factor: float = 1.0) -> float: ...

class BlackScholesEngine:
    def calculate(self, base_price: float, volatility_factor: float = 1.0) -> float:
        return base_price * random.uniform(0.9, 1.1) * volatility_factor

class MonteCarloEngine:
    def __init__(self, iterations: int = 1000):
        self.iterations = iterations
    
    def calculate(self, base_price: float, volatility_factor: float = 1.0) -> float:
        return base_price * statistics.mean(random.gauss(1.0, 0.1) for _ in range(self.iterations)) * volatility_factor

class BinomialEngine:
    def __init__(self, steps: int = 100):
        self.steps = steps
    
    def calculate(self, base_price: float, volatility_factor: float = 1.0) -> float:
        return base_price * (1 + random.uniform(-0.05, 0.05) * volatility_factor)

class PricingContext:
    def __init__(self, engine: PricingEngine):
        self._engine = engine
    
    @property
    def engine(self) -> PricingEngine:
        return self._engine
    
    @engine.setter
    def engine(self, engine: PricingEngine):
        self._engine = engine
    
    def compute(self, base_price: float, volatility_factor: float = 1.0) -> float:
        return self._engine.calculate(base_price, volatility_factor)

if __name__ == "__main__":
    engines = [
        BlackScholesEngine(),
        MonteCarloEngine(500),
        BinomialEngine(50)
    ]
    
    context = PricingContext(engines[0])
    base_price = 100.0
    
    for engine in engines:
        context.engine = engine
        result = context.compute(base_price, 1.2)
        print(f"Result: ${result:.2f}")