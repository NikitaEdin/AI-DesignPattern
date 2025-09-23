class BankAccountFacade:
    def __init__(self, bank_account):
        self.bank_account = bank_account

    def deposit(self, amount):
        return self.bank_account.deposit(amount)

    def withdraw(self, amount):
        return self.bank_account.withdraw(amount)

    def get_balance(self):
        return self.bank_account.get_balance()

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return self.balance
        else:
            return "Insufficient balance"

    def get_balance(self):
        return self.balance

if __name__ == "__main__":
    bank_account = BankAccount()
    facade = BankAccountFacade(bank_account)

    print("Initial balance:", facade.get_balance())

    facade.deposit(100)
    print("Balance after deposit:", facade.get_balance())

    facade.withdraw(50)
    print("Balance after withdrawal:", facade.get_balance())