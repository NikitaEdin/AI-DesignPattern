# State Design Pattern Implementation
class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient Balance!")

class ActiveState:
    def __init__(self, account):
        self.account = account

    def deposit(self, amount):
        self.account.deposit(amount)
        print(f"Deposited {amount}. New balance is {self.account.balance}")

    def withdraw(self, amount):
        if self.account.balance >= amount:
            self.account.withdraw(amount)
            print(f"Withdrew {amount}. New balance is {self.account.balance}")
        else:
            print("Insufficient Balance!")

class FrozenState:
    def __init__(self, account):
        self.account = account

    def deposit(self, amount):
        print("Cannot Deposit in Frozen State!")

    def withdraw(self, amount):
        if self.account.balance >= amount:
            self.account.withdraw(amount)
            print(f"Withdrew {amount}. New balance is {self.account.balance}")
        else:
            print("Insufficient Balance!")

# Usage Example
active = ActiveState(Account())
frozen = FrozenState(Account())

# Testing
print("Testing Active State")
active.deposit(10)
active.withdraw(5)
active.withdraw(5)
active.withdraw(5)

print("\nTesting Frozen State")
frozen.deposit(10)
frozen.withdraw(5)
frozen.withdraw(5)
frozen.withdraw(5)