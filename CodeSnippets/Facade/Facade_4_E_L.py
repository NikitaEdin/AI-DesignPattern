class BankAccount(object):
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True
    
class BankAccountFacade:
    def __init__(self, account):
        self.account = account
    
    def deposit(self, amount):
        return self.account.deposit(amount)
    
    def withdraw(self, amount):
        return self.account.withdraw(amount)
    
# Usage example
if __name__ == "__main__":
    account = BankAccount()
    facade = BankAccountFacade(account)
    
    print("Initial balance:", account.balance)
    
    facade.deposit(100)
    print("Balance after depositing $100:", account.balance)
    
    facade.withdraw(50)
    print("Balance after withdrawing $50:", account.balance)