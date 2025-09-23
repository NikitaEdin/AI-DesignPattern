class AccountState:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
        else:
            raise ValueError("Insufficient balance")

class AccountContext:
    def __init__(self, account_state):
        self.account_state = account_state

    def deposit(self, amount):
        self.account_state.deposit(amount)

    def withdraw(self, amount):
        self.account_state.withdraw(amount)

class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
        else:
            raise ValueError("Insufficient balance")

def main():
    account = Account(100)
    context = AccountContext(account)

    print("Balance before deposit:", account.balance)
    context.deposit(50)
    print("Balance after deposit:", account.balance)

    print("\nBalance before withdrawal:", account.balance)
    context.withdraw(75)
    print("Balance after withdrawal:", account.balance)

if __name__ == "__main__":
    main()