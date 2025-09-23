class BankingFacade:
    def __init__(self, bank):
        self.bank = bank

    def deposit(self, amount):
        return self.bank.deposit(amount)

    def withdraw(self, amount):
        return self.bank.withdraw(amount)

    def get_balance(self):
        return self.bank.get_balance()

class Bank:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def get_balance(self):
        return self.balance

if __name__ == "__main__":
    bank = Bank()
    banking_facade = BankingFacade(bank)

    # Deposit $100
    banking_facade.deposit(100)
    print("Balance:", banking_facade.get_balance())

    # Withdraw $50
    banking_facade.withdraw(50)
    print("Balance:", banking_facade.get_balance())