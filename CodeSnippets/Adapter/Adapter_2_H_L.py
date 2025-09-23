class Account:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

class BankAdapter:
    def __init__(self, account):
        self.account = account

    def get_balance(self):
        return self.account.get_name() + " has $" + str(10)

    def deposit(self, amount):
        self.account.set_name(self.account.get_name() + " has $" + str(amount))

class Bank:
    def __init__(self, account):
        self.bank = BankAdapter(account)

    def get_balance(self):
        return self.bank.get_balance()

    def deposit(self, amount):
        self.bank.deposit(amount)

if __name__ == "__main__":
    account = Account("John")
    bank = Bank(account)
    print(bank.get_balance())
    bank.deposit(50)
    print(bank.get_balance())