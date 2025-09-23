class BankAccount:
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.balance = 0
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            return False
        else:
            self.balance -= amount
            return True