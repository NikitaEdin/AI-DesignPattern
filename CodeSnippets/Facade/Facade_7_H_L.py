class BankAccountFacade:
    def __init__(self, account_number):
        self.account = BankAccount(account_number)
    
    def deposit(self, amount):
        return self.account.deposit(amount)
    
    def withdraw(self, amount):
        return self.account.withdraw(amount)
    
    def get_balance(self):
        return self.account.get_balance()