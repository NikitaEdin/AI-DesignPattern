class Account:
    def __init__(self, balance):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient funds")
    
    def get_balance(self):
        return self.balance

class CheckingAccount(Account):
    def __init__(self, balance):
        super().__init__(balance)
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient funds")

class SavingsAccount(Account):
    def __init__(self, balance):
        super().__init__(balance)
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient funds")

class AccountManager:
    def __init__(self, account):
        self.account = account
    
    def deposit(self, amount):
        self.account.deposit(amount)
    
    def withdraw(self, amount):
        self.account.withdraw(amount)
    
    def get_balance(self):
        return self.account.get_balance()

if __name__ == "__main__":
    checking_account = CheckingAccount(1000)
    savings_account = SavingsAccount(500)
    
    manager = AccountManager(checking_account)
    manager.deposit(200)
    print(manager.get_balance()) # prints 1200
    
    manager.withdraw(300)
    print(manager.get_balance()) # prints 900
    
    manager = AccountManager(savings_account)
    manager.deposit(500)
    print(manager.get_balance()) # prints 1000
    
    manager.withdraw(200)
    print(manager.get_balance()) # prints 800