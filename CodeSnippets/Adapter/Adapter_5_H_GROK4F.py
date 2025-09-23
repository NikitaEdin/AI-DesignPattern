class ShippingCalculator:
    def calculate_shipping_cost(self, weight_kg, destination_country):
        raise NotImplementedError("Subclasses must implement this method")

class LegacyFedExAPI:
    def request_rate(self, volume_cubic_m, zone_id):
        if zone_id not in [1, 2, 3]:
            raise ValueError(f"Invalid zone ID: {zone_id}")
        factors = {1: 10.0, 2: 15.0, 3: 20.0}
        base_rate = factors.get(zone_id, 0.0)
        if base_rate == 0.0:
            raise ValueError("Unsupported zone for rate calculation")
        return volume_cubic_m * base_rate

class CompatibleFedExCalculator(ShippingCalculator):
    def __init__(self, legacy_api):
        self.legacy_api = legacy_api
        self.zone_mapping = {
            'US': 1,
            'CA': 2,
            'MX': 3,
            'Other': 0
        }
        self.volume_per_kg = 0.001
        self.max_weight = 100.0

    def calculate_shipping_cost(self, weight_kg, destination_country):
        if not isinstance(weight_kg, (int, float)) or weight_kg <= 0:
            raise ValueError("Weight must be a positive number")
        if weight_kg > self.max_weight:
            raise ValueError(f"Weight exceeds maximum of {self.max_weight} kg")
        if not isinstance(destination_country, str) or not destination_country.strip():
            raise ValueError("Destination country must be a non-empty string")
        dest = destination_country.strip().upper()
        if dest not in [k.upper() for k in self.zone_mapping.keys()]:
            raise ValueError(f"Unsupported destination: {destination_country}")
        zone = self.zone_mapping.get(dest, 0)
        if zone == 0:
            raise ValueError("No valid zone mapping for this destination")
        volume = weight_kg * self.volume_per_kg
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                cost = self.legacy_api.request_rate(volume, zone)
                return round(cost, 2)
            except ValueError as e:
                if attempt == max_retries:
                    raise RuntimeError(f"Failed to calculate after {max_retries} attempts: {e}")
                continue
        raise RuntimeError("Unexpected failure in rate calculation")

class OrderProcessor:
    def __init__(self, calculator):
        if not isinstance(calculator, ShippingCalculator):
            raise TypeError("Calculator must implement ShippingCalculator")
        self.calculator = calculator

    def process_order(self, weight, destination):
        try:
            cost = self.calculator.calculate_shipping_cost(weight, destination)
            print(f"Shipping cost for {weight}kg to {destination}: ${cost}")
            return cost
        except (ValueError, RuntimeError) as e:
            print(f"Error processing order: {e}")
            return None

if __name__ == "__main__":
    legacy_api = LegacyFedExAPI()
    fedex_calc = CompatibleFedExCalculator(legacy_api)
    processor = OrderProcessor(fedex_calc)
    processor.process_order(10, 'US')
    processor.process_order(5, 'CA')
    processor.process_order(20, 'MX')
    processor.process_order(0, 'US')
    processor.process_order(10, 'ZZ')
    processor.process_order(150, 'US')