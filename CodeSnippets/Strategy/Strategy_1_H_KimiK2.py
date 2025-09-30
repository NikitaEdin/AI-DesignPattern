from abc import ABC, abstractmethod
import math

class Invoice:
    def __init__(self, base_amount: float, currency: str = "USD"):
        self.base_amount = base_amount
        self.currency = currency
        self._pricing_model = None
    
    def set_pricing_model(self, model):
        self._pricing_model = model
    
    def calculate_total(self) -> float:
        if self._pricing_model is None:
            raise ValueError("Pricing model not set")
        return self._pricing_model.compute(self.base_amount)
    
    def get_discount_breakdown(self) -> dict:
        if self._pricing_model is None:
            raise ValueError("Pricing model not set")
        return self._pricing_model.get_breakdown(self.base_amount)

class PricingModel(ABC):
    @abstractmethod
    def compute(self, amount: float) -> float: ...
    
    @abstractmethod
    def get_breakdown(self, amount: float) -> dict: ...

class StandardPricing(PricingModel):
    def __init__(self, tax_rate: float = 0.08):
        self.tax_rate = tax_rate
    
    def compute(self, amount: float) -> float:
        return round(amount * (1 + self.tax_rate), 2)
    
    def get_breakdown(self, amount: float) -> dict:
        tax = round(amount * self.tax_rate, 2)
        return {"base": amount, "tax": tax, "total": amount + tax}

class PremiumPricing(PricingModel):
    def __init__(self, discount_rate: float = 0.10, tax_rate: float = 0.08):
        self.discount_rate = discount_rate
        self.tax_rate = tax_rate
    
    def compute(self, amount: float) -> float:
        discounted = amount * (1 - self.discount_rate)
        return round(discounted * (1 + self.tax_rate), 2)
    
    def get_breakdown(self, amount: float) -> dict:
        discount = round(amount * self.discount_rate, 2)
        discounted = amount - discount
        tax = round(discounted * self.tax_rate, 2)
        return {"base": amount, "discount": discount, "tax": tax, "total": discounted + tax}

class DynamicPricing(PricingModel):
    def __init__(self, threshold: float = 1000, high_discount: float = 0.15, low_discount: float = 0.05):
        self.threshold = threshold
        self.high_discount = high_discount
        self.low_discount = low_discount
        self.tax_rate = 0.08
    
    def compute(self, amount: float) -> float:
        discount = self.high_discount if amount >= self.threshold else self.low_discount
        discounted = amount * (1 - discount)
        return round(discounted * (1 + self.tax_rate), 2)
    
    def get_breakdown(self, amount: float) -> dict:
        discount_rate = self.high_discount if amount >= self.threshold else self.low_discount
        discount = round(amount * discount_rate, 2)
        discounted = amount - discount
        tax = round(discounted * self.tax_rate, 2)
        return {"base": amount, "discount": discount, "threshold_met": amount >= self.threshold, "tax": tax, "total": discounted + tax}

if __name__ == "__main__":
    invoice1 = Invoice(1500)
    invoice1.set_pricing_model(PremiumPricing())
    print(f"Premium total: ${invoice1.calculate_total()}")
    print(invoice1.get_discount_breakdown())
    
    invoice2 = Invoice(800)
    invoice2.set_pricing_model(DynamicPricing())
    print(f"Dynamic total: ${invoice2.calculate_total()}")
    print(invoice2.get_discount_breakdown())