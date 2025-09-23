from abc import ABC, abstractmethod

class MachineMode(ABC):
    @abstractmethod
    def insert_coin(self, machine):
        pass

    @abstractmethod
    def select_product(self, machine):
        pass

    @abstractmethod
    def dispense(self, machine):
        pass

class IdleMode(MachineMode):
    def insert_coin(self, machine):
        machine.current_mode = CoinInsertedMode()
        print("Coin inserted.")

    def select_product(self, machine):
        print("Error: Insert coin first.")
        raise ValueError("No coin inserted.")

    def dispense(self, machine):
        print("Error: Insert coin and select product first.")
        raise ValueError("Nothing to dispense.")

class CoinInsertedMode(MachineMode):
    def insert_coin(self, machine):
        print("Error: Coin already inserted.")
        raise ValueError("Coin already present.")

    def select_product(self, machine):
        machine.current_mode = ProductSelectedMode()
        print("Product selected.")

    def dispense(self, machine):
        print("Error: Select product first.")
        raise ValueError("No product selected.")

class ProductSelectedMode(MachineMode):
    def insert_coin(self, machine):
        print("Error: Coin already inserted; select product.")
        raise ValueError("Coin already present.")

    def select_product(self, machine):
        print("Error: Product already selected.")
        raise ValueError("Product already selected.")

    def dispense(self, machine):
        machine.current_mode = IdleMode()
        print("Product dispensed.")

class VendingMachine:
    def __init__(self):
        self.current_mode = IdleMode()

    def insert_coin(self):
        try:
            self.current_mode.insert_coin(self)
        except ValueError as e:
            print(e)

    def select_product(self):
        try:
            self.current_mode.select_product(self)
        except ValueError as e:
            print(e)

    def dispense(self):
        try:
            self.current_mode.dispense(self)
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    vm = VendingMachine()
    vm.insert_coin()
    vm.select_product()
    vm.dispense()
    vm.select_product()