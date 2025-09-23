class BankAccount(object):
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds"
        else:
            self.balance -= amount
            return self.balance
    
class BankAccountFacade(object):
    def __init__(self, bank_account):
        self.bank_account = bank_account
    
    def get_balance(self):
        return self.bank_account.balance
    
    def withdraw(self, amount):
        return self.bank_account.withdraw(amount)
    
    def transfer(self, recipient, amount):
        if amount > self.get_balance():
            return "Insufficient funds"
        else:
            self.bank_account.withdraw(amount)
            recipient.bank_account.deposit(amount)
            return self.get_balance()
    
class TransactionService(object):
    def __init__(self, bank_account):
        self.bank_account = bank_account
    
    def process_transaction(self, transaction):
        if transaction == "withdraw":
            return self.bank_account.withdraw()
        elif transaction == "deposit":
            return self.bank_account.deposit()
        else:
            return "Invalid transaction"
    
if __name__ == '__main__':
    bank_account = BankAccount(100)
    facade = BankAccountFacade(bank_account)
    print(facade.get_balance())  # prints 100
    print(facade.withdraw(25))   # prints 75
    print(facade.transfer(BankAccount(50), 25))  # prints 50