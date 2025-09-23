class BankAccountFacade:
    def __init__(self, account_number):
        self.account_number = account_number
        self.bank_api = BankAPI()
    
    def deposit(self, amount):
        self.bank_api.deposit(self.account_number, amount)
    
    def withdraw(self, amount):
        self.bank_api.withdraw(self.account_number, amount)
    
    def balance(self):
        return self.bank_api.balance(self.account_number)