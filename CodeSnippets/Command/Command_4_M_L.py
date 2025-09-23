class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            print("Insufficient funds")
            return False

class BankTransaction:
    def __init__(self, amount, account):
        self.amount = amount
        self.account = account

    def execute(self):
        if self.amount > 0:
            return self.account.deposit(self.amount)
        else:
            return self.account.withdraw(-self.amount)

class CommandBankAccount:
    def __init__(self, bank_account):
        self.bank_account = bank_account

    def deposit(self, amount):
        command = BankTransaction(amount, self.bank_account)
        return command.execute()

    def withdraw(self, amount):
        command = BankTransaction(-amount, self.bank_account)
        return command.execute()

class Command:
    def __init__(self, bank_account):
        self.bank_account = bank_account

    def execute(self):
        pass

# Usage example
account = BankAccount(100)
command = CommandBankAccount(account)
print("Initial balance:", account.balance)
command.deposit(50)
print("Balance after deposit:", account.balance)
command.withdraw(20)
print("Balance after withdrawal:", account.balance)