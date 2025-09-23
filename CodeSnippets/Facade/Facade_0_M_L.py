```python
            class BankAccountFacade:
                def __init__(self, account_id):
                    self.account_id = account_id
                    self.bank_api = BankAPI()
                    
                def deposit(self, amount):
                    self.bank_api.deposit(self.account_id, amount)
                    
                def withdraw(self, amount):
                    self.bank_api.withdraw(self.account_id, amount)
                    
                def get_balance(self):
                    return self.bank_api.get_balance(self.account_id)
                    
            class BankAPI:
                def deposit(self, account_id, amount):
                    # implementation for the deposit method
                    
                def withdraw(self, account_id, amount):
                    # implementation for the withdraw method
                    
                def get_balance(self, account_id):
                    # implementation for the get balance method
                    
            def main():
                facade = BankAccountFacade("12345")
                facade.deposit(100)
                facade.withdraw(50)
                print(facade.get_balance())
        ```
         In this implementation, the `BankAPI` class provides a set of methods for interacting with a bank account: depositing, withdrawing, and getting the balance. The `BankAccountFacade` class acts as an interface to these methods by providing a simpler API that can be used by clients.
         
         The `BankAccountFacade` class has a single method called `deposit` which takes an amount as input and delegates the call to the `bank_api.deposit` method. Similarly, the `withdraw` method is implemented in the same way. The `get_balance` method simply returns the result of calling `bank_api.get_balance`.
         
         In the main section of the code, we create an instance of the `BankAccountFacade` class and use it to deposit $100, withdraw $50, and then get the balance. We can see that the facade provides a simpler API than the underlying bank API.