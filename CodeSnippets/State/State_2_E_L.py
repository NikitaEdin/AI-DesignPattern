class AccountState:
    def __init__(self, balance):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient funds")
        
    def get_balance(self):
        return self.balance
    
class Main:
    def __init__(self):
        account = AccountState(100)
        print("Initial balance:", account.get_balance())
        account.deposit(50)
        print("Balance after depositing $50:", account.get_balance())
        account.withdraw(20)
        print("Balance after withdrawing $20:", account.get_balance())
        account.withdraw(30)
        print("Balance after withdrawing $30:", account.get_balance())