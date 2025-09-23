```python
 class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Balance must be positive")
        self._balance = amount

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient balance")

class BankFacade:
    def __init__(self, account):
        self.account = account

    def deposit(self, amount):
        self.account.deposit(amount)

    def withdraw(self, amount):
        self.account.withdraw(amount)

# Usage example:
def main():
    account = BankAccount()
    facade = BankFacade(account)
    facade.deposit(100)
    facade.withdraw(50)
    print(account.balance)

if __name__ == "__main__":
    main()
  ```