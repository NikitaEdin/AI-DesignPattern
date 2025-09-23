class BankAccount:
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.balance = 0
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient balance")
    
    def get_balance(self):
        return self.balance
    
class BankFacade:
    def __init__(self, bank_account):
        self.bank_account = bank_account
    
    def deposit(self, amount):
        self.bank_account.deposit(amount)
    
    def withdraw(self, amount):
        self.bank_account.withdraw(amount)
    
    def get_balance(self):
        return self.bank_account.get_balance()

if __name__ == "__main__":
    bank_facade = BankFacade(BankAccount("Alice"))
    bank_facade.deposit(100)
    print(bank_facade.get_balance()) # 100
    bank_facade.withdraw(50)
    print(bank_facade.get_balance()) # 50