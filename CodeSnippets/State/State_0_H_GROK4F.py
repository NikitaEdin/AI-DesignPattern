from abc import ABC, abstractmethod

class VendingMachine:
    def __init__(self, initial_stock=5):
        self.stock = initial_stock
        if initial_stock == 0:
            self.mode = OutOfStock(self)
        else:
            self.mode = WaitingForPayment(self)

    def insert_coin(self):
        return self.mode.insert_coin()

    def press_select(self):
        return self.mode.press_select()

    def request_refund(self):
        return self.mode.request_refund()

    def restock(self, amount):
        self.stock += amount
        if self.stock > 0 and isinstance(self.mode, OutOfStock):
            self.mode = WaitingForPayment(self)
        return f"Stock updated to {self.stock}"

    def get_mode(self):
        return self.mode.__class__.__name__

class TransactionMode(ABC):
    def __init__(self, machine):
        self.machine = machine

    @abstractmethod
    def insert_coin(self):
        pass

    @abstractmethod
    def press_select(self):
        pass

    @abstractmethod
    def request_refund(self):
        pass

class WaitingForPayment(TransactionMode):
    def insert_coin(self):
        self.machine.mode = PaymentMade(self.machine)
        return "Coin inserted. Please select item."

    def press_select(self):
        return "No coin inserted. Please insert coin first."

    def request_refund(self):
        return "No coin to refund."

class PaymentMade(TransactionMode):
    def insert_coin(self):
        return "Coin already inserted. Please select item or request refund."

    def press_select(self):
        if self.machine.stock > 0:
            self.machine.stock -= 1
            self.machine.mode = ItemSold(self.machine)
            return "Item dispensed. Enjoy!"
        else:
            self.machine.mode = WaitingForPayment(self.machine)
            return "Out of stock. Coin refunded."

    def request_refund(self):
        self.machine.mode = WaitingForPayment(self.machine)
        return "Coin refunded."

class ItemSold(TransactionMode):
    def insert_coin(self):
        self.machine.mode = PaymentMade(self.machine)
        return "Coin inserted for next item."

    def press_select(self):
        return "Item just dispensed. Insert coin for another or request refund if needed."

    def request_refund(self):
        return "Cannot refund after item dispensed."

class OutOfStock(TransactionMode):
    def insert_coin(self):
        return "Machine out of stock. Restock required."

    def press_select(self):
        return "No items available. Restock required."

    def request_refund(self):
        return "No coin inserted to refund."

if __name__ == "__main__":
    vm = VendingMachine(1)
    print(f"Initial mode: {vm.get_mode()}")
    print(vm.insert_coin())
    print(f"Mode: {vm.get_mode()}")
    print(vm.press_select())
    print(f"Mode: {vm.get_mode()}")
    print(f"Stock: {vm.stock}")
    print(vm.insert_coin())
    print(f"Mode: {vm.get_mode()}")
    print(vm.press_select())
    print(f"Mode: {vm.get_mode()}")
    print(f"Stock: {vm.stock}")
    print(vm.request_refund())
    print(f"Mode: {vm.get_mode()}")
    empty_vm = VendingMachine(0)
    print(f"Empty initial mode: {empty_vm.get_mode()}")
    print(empty_vm.insert_coin())
    print(empty_vm.restock(3))
    print(f"Mode after restock: {empty_vm.get_mode()}")