class BankAccountFacade:
    def __init__(self, bank_account):
        self.bank_account = bank_account

    def deposit(self, amount):
        self.bank_account.deposit(amount)

    def withdraw(self, amount):
        self.bank_account.withdraw(amount)

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient funds")

if __name__ == "__main__":
    bank_account = BankAccount()
    facade = BankAccountFacade(bank_account)
    facade.deposit(100)
    print(bank_account.balance)  # prints 100
    facade.withdraw(50)
    print(bank_account.balance)  # prints 50