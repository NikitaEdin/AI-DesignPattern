# Facade Design Pattern Implementation
class BankAccount:
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

# Facade Class
class BankFacade:
    def __init__(self, bank_account):
        self.bank_account = bank_account
    
    # Deposit Money Method
    def deposit_money(self, amount):
        self.bank_account.deposit(amount)
    
    # Withdraw Money Method
    def withdraw_money(self, amount):
        if self.bank_account.get_balance() >= amount:
            self.bank_account.withdraw(amount)
        else:
            print("Insufficient funds")
    
    # Get Balance Method
    def get_balance(self):
        return self.bank_account.get_balance()

# Usage Example
if __name__ == "__main__":
    bank = BankFacade(BankAccount(1000))
    bank.deposit_money(500)
    print("Balance:", bank.get_balance())
    bank.withdraw_money(200)
    print("Balance:", bank.get_balance())