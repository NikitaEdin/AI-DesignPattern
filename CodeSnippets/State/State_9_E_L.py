class Account:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount

class CurrentState:
    def __init__(self, account):
        self.account = account

    def __str__(self):
        return "Current State"

    def process(self, event):
        if event == "DEPOSIT":
            self.account.deposit(10)
        elif event == "WITHDRAW":
            self.account.withdraw(5)
        else:
            raise ValueError("Invalid event")

class PendingState:
    def __init__(self, account):
        self.account = account

    def __str__(self):
        return "Pending State"

    def process(self, event):
        if event == "DEPOSIT":
            self.account.deposit(20)
        elif event == "WITHDRAW":
            self.account.withdraw(15)
        else:
            raise ValueError("Invalid event")

class ClosedState:
    def __init__(self, account):
        self.account = account

    def __str__(self):
        return "Closed State"

    def process(self, event):
        if event == "DEPOSIT":
            self.account.deposit(30)
        elif event == "WITHDRAW":
            self.account.withdraw(25)
        else:
            raise ValueError("Invalid event")

class StateMachine:
    def __init__(self, account):
        self.account = account
        self.state = CurrentState(account)

    def handle_event(self, event):
        self.state.process(event)
        if self.state == CurrentState:
            self.state = PendingState(self.account)
        elif self.state == PendingState:
            self.state = ClosedState(self.account)
        else:
            raise ValueError("Invalid state")

# Usage example
account = Account()
machine = StateMachine(account)
machine.handle_event("DEPOSIT")
print(account.balance) # Output: 10
machine.handle_event("WITHDRAW")
print(account.balance) # Output: 5
machine.handle_event("DEPOSIT")
print(account.balance) # Output: 20
machine.handle_event("WITHDRAW")
print(account.balance) # Output: 15
machine.handle_event("DEPOSIT")
print(account.balance) # Output: 30