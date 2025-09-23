class AccountState(Enum):
    ACTIVE = 1
    INACTIVE = 2

class Account:
    def __init__(self, state=AccountState.ACTIVE):
        self._state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if not isinstance(value, AccountState):
            raise ValueError("Invalid state")
        self._state = value

class Bank:
    def __init__(self):
        self._accounts = {}

    def open_account(self, owner, balance=0):
        account = Account()
        account.owner = owner
        account.balance = balance
        self._accounts[owner] = account
        return account

    def close_account(self, owner):
        del self._accounts[owner]

    def get_account(self, owner):
        return self._accounts.get(owner)

class Transaction:
    def __init__(self, from_account, to_account, amount):
        self._from_account = from_account
        self._to_account = to_account
        self._amount = amount

    @property
    def from_account(self):
        return self._from_account

    @from_account.setter
    def from_account(self, value):
        if not isinstance(value, Account):
            raise ValueError("Invalid from_account")
        self._from_account = value

    @property
    def to_account(self):
        return self._to_account

    @to_account.setter
    def to_account(self, value):
        if not isinstance(value, Account):
            raise ValueError("Invalid to_account")
        self._to_account = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Invalid amount")
        self._amount = value

class BankSystem:
    def __init__(self):
        self._bank = Bank()

    def open_account(self, owner, balance=0):
        return self._bank.open_account(owner, balance)

    def close_account(self, owner):
        self._bank.close_account(owner)

    def get_account(self, owner):
        return self._bank.get_account(owner)

    def transfer(self, from_account, to_account, amount):
        if not isinstance(from_account, Account) or not isinstance(to_account, Account):
            raise ValueError("Invalid account")
        if from_account.balance < amount:
            raise ValueError("Insufficient balance")
        self._bank.transfer(from_account, to_account, amount)

if __name__ == "__main__":
    system = BankSystem()
    account1 = system.open_account("Alice", 1000)
    account2 = system.open_account("Bob")
    print(account1.state)
    print(account2.state)
    transaction = Transaction(from_account=account1, to_account=account2, amount=500)
    system.transfer(transaction)
    print(account1.balance)
    print(account2.balance)