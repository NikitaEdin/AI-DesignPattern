Facade Pattern Implementation in Python

class BankFacade:
    def __init__(self, bank):
        self.bank = bank
    
    def deposit(self, amount):
        return self.bank.deposit(amount)
    
    def withdraw(self, amount):
        return self.bank.withdraw(amount)
    
    def get_balance(self):
        return self.bank.get_balance()

class Bank:
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. Balance is now {self.get_balance()}")
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        print(f"Withdrew {amount}. Balance is now {self.get_balance()}")
    
    def get_balance(self):
        return self.balance

if __name__ == "__main__":
    bank = Bank(100)
    facade = BankFacade(bank)
    
    facade.deposit(50)
    facade.withdraw(20)
    print(facade.get_balance())