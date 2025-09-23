import abc
from typing import List

class PricingRule(abc.ABC):
    @abc.abstractmethod
    def apply(self, base_price: float, quantity: int) -> float:
        pass

class FlatDiscountRule(PricingRule):
    def __init__(self, discount_rate: float):
        if not 0 <= discount_rate <= 1:
            raise ValueError("Discount rate must be between 0 and 1")
        self.discount_rate = discount_rate

    def apply(self, base_price: float, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        return base_price * quantity * (1 - self.discount_rate)

class VolumeDiscountRule(PricingRule):
    def __init__(self, threshold: int, discount_rate: float):
        if threshold <= 0:
            raise ValueError("Threshold must be positive")
        if not 0 <= discount_rate <= 1:
            raise ValueError("Discount rate must be between 0 and 1")
        self.threshold = threshold
        self.discount_rate = discount_rate

    def apply(self, base_price: float, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if quantity >= self.threshold:
            return base_price * quantity * (1 - self.discount_rate)
        return base_price * quantity

class CombinedRule(PricingRule):
    def __init__(self, rules: List[PricingRule]):
        if not rules:
            raise ValueError("At least one rule required")
        self.rules = rules

    def apply(self, base_price: float, quantity: int) -> float:
        current_price = base_price * quantity
        for rule in self.rules:
            if isinstance(rule, VolumeDiscountRule):
                current_price = rule.apply(current_price / quantity, quantity)
            else:
                current_price = rule.apply(current_price / quantity, quantity)
        return current_price

class PricingCalculator:
    def __init__(self, rule: PricingRule = None):
        self._rule = rule
        self._cache = {}

    @property
    def current_rule(self) -> PricingRule:
        if self._rule is None:
            raise ValueError("No rule set")
        return self._rule

    def set_rule(self, rule: PricingRule) -> None:
        if not isinstance(rule, PricingRule):
            raise TypeError("Must provide a valid pricing rule")
        self._rule = rule
        self._cache.clear()

    def compute_total(self, base_price: float, quantity: int) -> float:
        if base_price < 0:
            raise ValueError("Base price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        key = (base_price, quantity)
        if key in self._cache:
            return self._cache[key]
        if self._rule is None:
            raise ValueError("No pricing rule configured")
        total = self._rule.apply(base_price, quantity)
        self._cache[key] = total
        return total

class RuleFactory:
    @staticmethod
    def create_by_quantity(quantity: int) -> PricingRule:
        if quantity > 50:
            return VolumeDiscountRule(50, 0.15)
        elif quantity > 10:
            return FlatDiscountRule(0.10)
        else:
            return FlatDiscountRule(0.05)

def main():
    calculator = PricingCalculator(FlatDiscountRule(0.05))
    print(calculator.compute_total(20.0, 5))  # 95.0

    calculator.set_rule(VolumeDiscountRule(10, 0.20))
    print(calculator.compute_total(20.0, 15))  # 240.0

    factory = RuleFactory()
    dynamic_rule = factory.create_by_quantity(60)
    calculator.set_rule(dynamic_rule)
    print(calculator.compute_total(20.0, 60))  # 1020.0

    combined = CombinedRule([FlatDiscountRule(0.05), VolumeDiscountRule(20, 0.10)])
    calculator.set_rule(combined)
    print(calculator.compute_total(20.0, 25))  # 414.5

    try:
        calculator.compute_total(20.0, -5)
    except ValueError as e:
        print(f"Handled error: {e}")

    print(calculator.compute_total(20.0, 5))  # Cached: 95.0

if __name__ == "__main__":
    main()