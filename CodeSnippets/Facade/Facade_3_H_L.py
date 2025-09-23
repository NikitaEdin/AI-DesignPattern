class Bank:
    def __init__(self, balance):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient funds.")
    
    def get_balance(self):
        return self.balance

class BankFacade:
    def __init__(self, bank=Bank()):
        self.bank = bank
    
    def check_account(self):
        print("Checking account balance.")
        print(f"Current balance: {self.bank.get_balance()}")
    
    def deposit(self, amount):
        print("Depositing funds.")
        self.bank.deposit(amount)
    
    def withdraw(self, amount):
        print("Withdrawing funds.")
        self.bank.withdraw(amount)

if __name__ == "__main__":
    bank_facade = BankFacade()
    bank_facade.check_account()
    bank_facade.deposit(100)
    bank_facade.withdraw(50)
    bank_facade.check_account()