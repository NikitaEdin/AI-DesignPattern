import random
class BankFacade():
    def __init__(self, bank):
        self.bank = bank
    def deposit(self, amount):
        return self.bank.deposit(amount)
    def withdraw(self, amount):
        return self.bank.withdraw(amount)
    def balance(self):
        return self.bank.balance()
class Bank():
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
        print("Deposited $" + str(amount) + " into " + self.name + "'s account")
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance for " + self.name)
        else:
            self.balance -= amount
            print("Withdrew $" + str(amount) + " from " + self.name + "'s account")
    def balance(self):
        return self.balance

# Test the BankFacade
john = Bank("John", 1000)
bob = Bank("Bob", 2000)
facade = BankFacade(john)

print("Balance before transfer: " + str(facade.balance())) # Check the balance before transferring money
facade.deposit(500) # Deposit $500 into John's account
facade.withdraw(100) # Withdraw $100 from John's account
print("Balance after transfer: " + str(facade.balance())) # Check the balance after transferring money
john.deposit(200) # Deposit $200 into John's account
john.withdraw(150) # Withdraw $150 from John's account
print("Balance after transfer: " + str(facade.balance())) # Check the balance after transferring money

# Test the BankFacade with a different bank account
bob = Bank("Bob", 2000)
facade = BankFacade(bob)
print("Balance before transfer: " + str(facade.balance())) # Check the balance before transferring money
facade.deposit(500) # Deposit $500 into Bob's account
facade.withdraw(100) # Withdraw $100 from Bob's account
print("Balance after transfer: " + str(facade.balance())) # Check the balance after transferring money
bob.deposit(200) # Deposit $200 into Bob's account
bob.withdraw(150) # Withdraw $150 from Bob's account
print("Balance after transfer: " + str(facade.balance())) # Check the balance after transferring money)