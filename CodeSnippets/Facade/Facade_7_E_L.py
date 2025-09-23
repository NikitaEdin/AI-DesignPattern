class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance must be positive")
        self._balance = value

class BankFacade:
    def __init__(self, bank_account):
        self._bank_account = bank_account

    def deposit(self, amount):
        self._bank_account.balance += amount

    def withdraw(self, amount):
        if self._bank_account.balance >= amount:
            self._bank_account.balance -= amount
        else:
            raise ValueError("Insufficient balance")

if __name__ == "__main__":
    bank = BankFacade(BankAccount())
    bank.deposit(100)
    print(bank.balance)  # Output: 100
    bank.withdraw(50)
    print(bank.balance)  # Output: 50