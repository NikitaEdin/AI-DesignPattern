class VendingMachine:
    def __init__(self):
        self._current_mode = ReadyMode(self)
        self._balance = 0.0
    
    def set_mode(self, mode):
        self._current_mode = mode
    
    def insert_coin(self, amount):
        return self._current_mode.insert_coin(amount)
    
    def select_item(self, item):
        return self._current_mode.select_item(item)
    
    def dispense(self):
        return self._current_mode.dispense()
    
    @property
    def balance(self):
        return self._balance
    
    def add_balance(self, amount):
        self._balance += amount
    
    def reset_balance(self):
        self._balance = 0.0

class ReadyMode:
    def __init__(self, machine):
        self._machine = machine
    
    def insert_coin(self, amount):
        if amount <= 0:
            return "Invalid coin amount"
        self._machine.add_balance(amount)
        self._machine.set_mode(CoinInsertedMode(self._machine))
        return f"Coin inserted. Balance: ${self._machine.balance:.2f}"
    
    def select_item(self, item):
        return "Please insert coins first"
    
    def dispense(self):
        return "No item selected"

class CoinInsertedMode:
    def __init__(self, machine):
        self._machine = machine
    
    def insert_coin(self, amount):
        if amount <= 0:
            return "Invalid coin amount"
        self._machine.add_balance(amount)
        return f"Coin added. Balance: ${self._machine.balance:.2f}"
    
    def select_item(self, item):
        item_price = 1.50
        if self._machine.balance >= item_price:
            self._machine.set_mode(DispensingMode(self._machine, item))
            return f"Item '{item}' selected"
        return "Insufficient funds"
    
    def dispense(self):
        return "Please select an item first"

class DispensingMode:
    def __init__(self, machine, item):
        self._machine = machine
        self._item = item
    
    def insert_coin(self, amount):
        return "Please wait, dispensing in progress"
    
    def select_item(self, item):
        return "Already dispensing an item"
    
    def dispense(self):
        self._machine.reset_balance()
        self._machine.set_mode(ReadyMode(self._machine))
        return f"Dispensed: {self._item}"

if __name__ == "__main__":
    machine = VendingMachine()
    
    print(machine.select_item("Soda"))
    print(machine.insert_coin(1.00))
    print(machine.select_item("Soda"))
    print(machine.insert_coin(0.75))
    print(machine.select_item("Soda"))
    print(machine.dispense())
    print(machine.dispense())