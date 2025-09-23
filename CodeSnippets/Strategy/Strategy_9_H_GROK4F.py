from abc import ABC, abstractmethod

class DiscountRule(ABC):
    @abstractmethod
    def compute(self, amount: float) -> float:
        pass

class FixedAmountRule(DiscountRule):
    def __init__(self, fixed: float):
        if fixed < 0:
            raise ValueError("Fixed amount must be non-negative")
        self.fixed = fixed

    def compute(self, amount: float) -> float:
        if amount <= self.fixed:
            return 0.0
        return amount - self.fixed

class PercentOffRule(DiscountRule):
    def __init__(self, percent: float):
        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100")
        self.rate = percent / 100.0

    def compute(self, amount: float) -> float:
        if amount <= 0:
            return 0.0
        return amount * (1 - self.rate)

class TieredDiscountRule(DiscountRule):
    def __init__(self, tiers: list[tuple[float, float]]):
        if not tiers:
            raise ValueError("Tiers list cannot be empty")
        self.tiers = sorted(tiers, key=lambda t: t[0])
        if self.tiers[0][0] != 0:
            raise ValueError("Tiers must start with threshold 0")

    def compute(self, amount: float) -> float:
        if amount <= 0:
            return 0.0
        disc_rate = 0.0
        for threshold, rate in self.tiers:
            if amount >= threshold:
                disc_rate = rate
        return amount * (1 - disc_rate)

class ShoppingCart:
    def __init__(self, base_total: float):
        if base_total < 0:
            raise ValueError("Base total must be non-negative")
        self.base_total = base_total
        self._rule: DiscountRule | None = None

    def set_discount_rule(self, rule: DiscountRule) -> None:
        self._rule = rule

    def get_final_price(self) -> float:
        if self._rule is None:
            return self.base_total
        return self._rule.compute(self.base_total)

if __name__ == "__main__":
    cart = ShoppingCart(100.0)
    print(f"Base price: {cart.get_final_price()}")

    cart.set_discount_rule(FixedAmountRule(20.0))
    print(f"Fixed discount: {cart.get_final_price()}")

    cart.set_discount_rule(PercentOffRule(15.0))
    print(f"Percent discount: {cart.get_final_price()}")

    try:
        cart.set_discount_rule(PercentOffRule(150.0))
    except ValueError as e:
        print(f"Validation error: {e}")

    tiers = [(0, 0.0), (50, 0.05), (100, 0.10)]
    cart.set_discount_rule(TieredDiscountRule(tiers))
    print(f"Tiered discount for 100: {cart.get_final_price()}")

    small_cart = ShoppingCart(30.0)
    small_cart.set_discount_rule(TieredDiscountRule(tiers))
    print(f"Tiered discount for 30: {small_cart.get_final_price()}")

    zero_cart = ShoppingCart(0.0)
    zero_cart.set_discount_rule(FixedAmountRule(10.0))
    print(f"Edge case zero base: {zero_cart.get_final_price()}")