import math

class PriceEstimator:
    def __init__(self, calculator):
        self.calculator = calculator
    def calculate(self, units):
        return self.calculator.compute(units)

class FlatRateCalculator:
    def compute(self, units):
        return units * 5.0

class BulkCalculator:
    def compute(self, units):
        return (units // 10) * 45 + (units % 10) * 5.0

class PremiumCalculator:
    def compute(self, units):
        return units * 7.5 * 1.15

if __name__ == "__main__":
    try:
        units = 25
        estimator = PriceEstimator(FlatRateCalculator())
        print(estimator.calculate(units))
        estimator = PriceEstimator(BulkCalculator())
        estimator.calculate(units)
        estimator = PriceEstimator(PremiumCalculator())
        estimator.calculate(units)
    except Exception:
        print("error")