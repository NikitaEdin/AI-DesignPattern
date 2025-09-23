```
         
class BankAccountFacade:
    def __init__(self, account_number):
        self.account_number = account_number
    
    def deposit(self, amount):
        bank_api = BankAPI()
        bank_api.deposit(amount)
    
    def withdraw(self, amount):
        bank_api = BankAPI()
        bank_api.withdraw(amount)
    
class BankAPI:
    def deposit(self, amount):
        print("Depositing $" + str(amount) + " into account " + str(self.account_number))
    
    def withdraw(self, amount):
        print("Withdrawing $" + str(amount) + " from account " + str(self.account_number))
        
def main():
    account = BankAccountFacade(1234567890)
    account.deposit(100)
    account.withdraw(50)
    
if __name__ == "__main__":
    main()
         ```