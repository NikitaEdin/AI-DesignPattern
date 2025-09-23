class BankAccountFacade:
    def __init__(self, account_number):
        self.account_number = account_number

    def deposit(self, amount):
        bank_account = BankAccount(self.account_number)
        bank_account.deposit(amount)

    def withdraw(self, amount):
        bank_account = BankAccount(self.account_number)
        bank_account.withdraw(amount)

class BankAccount:
    def __init__(self, account_number):
        self.account_number = account_number
        self.balance = 0

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Invalid amount")
        self.balance += amount

    def withdraw(self, amount):
        if amount < 0 or amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

if __name__ == "__main__":
    account = BankAccountFacade(123456789)
    account.deposit(100)
    account.withdraw(50)