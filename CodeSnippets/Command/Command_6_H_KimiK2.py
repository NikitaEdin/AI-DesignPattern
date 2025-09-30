import time
from typing import Dict, List, Protocol
from dataclasses import dataclass

class Receiver(Protocol):
    def execute(self, amount: int) -> None: ...

@dataclass
class Operation:
    def do(self) -> None: ...
    def undo(self) -> None: ...
    def __str__(self) -> str: ...

class BankAccount:
    def __init__(self) -> None:
        self.balance = 0
        self.actions: List[str] = []
    def deposit(self, amount: int) -> None:
        self.balance += amount
        self.actions.append(f"Deposit {amount}")
    def withdraw(self, amount: int) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            self.actions.append(f"Withdraw {amount}")
            return True
        return False
    def __str__(self) -> str:
        return f"Balance: {self.balance}"

class Deposit(Operation):
    def __init__(self, account: BankAccount, amount: int) -> None:
        self.account = account
        self.amount = amount
        self.timestamp = time.time()
    def do(self) -> None:
        self.account.deposit(self.amount)
    def undo(self) -> None:
        self.account.balance -= self.amount
    def __str__(self) -> str: return f"Deposit {self.amount}"

class Withdraw(Operation):
    def __init__(self, account: BankAccount, amount: int) -> None:
        self.account = account
        self.amount = amount
        self.timestamp = time.time()
    def do(self) -> None:
        self.successful = self.account.withdraw(self.amount)
    def undo(self) -> None:
        if self.successful:
            self.account.balance += self.amount
    def __str__(self) -> str: return f"Withdraw {self.amount}"

class Transfer(Operation):
    def __init__(self, from_account: BankAccount, to_account: BankAccount, amount: int) -> None:
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
    def do(self) -> None:
        self.successful = self.from_account.withdraw(self.amount)
        if self.successful:
            self.to_account.deposit(self.amount)
    def undo(self) -> None:
        if self.successful:
            self.from_account.deposit(self.amount)
            self.to_account.withdraw(self.amount)
    def __str__(self) -> str: return f"Transfer {self.amount} from {self.from_account} to {self.to_account}"

class MacroOperation(Operation):
    def __init__(self, operations: List[Operation]) -> None:
        self.operations = operations
    def do(self) -> None:
        self.executed: List[Operation] = []
        try:
            for op in self.operations:
                op.do()
                self.executed.append(op)
        except Exception:
            for op in reversed(self.executed):
                op.undo()
            raise
    def undo(self) -> None:
        for op in reversed(self.executed):
            op.undo()
    def __str__(self) -> str: return f"Macro({len(self.operations)})"

class History:
    def __init__(self) -> None:
        self.past: List[Operation] = []
        self.future: List[Operation] = []
    def push(self, op: Operation) -> None:
        op.do()
        self.past.append(op)
        self.future.clear()
    def undo(self) -> bool:
        if not self.past: return False
        op = self.past.pop()
        op.undo()
        self.future.append(op)
        return True
    def redo(self) -> bool:
        if not self.future: return False
        op = self.future.pop()
        op.do()
        self.past.append(op)
        return True

if __name__ == "__main__":
    a1 = BankAccount()
    a2 = BankAccount()
    h = History()
    h.push(Deposit(a1, 100))
    h.push(Withdraw(a1, 30))
    h.push(Transfer(a1, a2, 40))
    print(a1, a2)
    h.undo()
    print(a1, a2)
    h.redo()
    print(a1, a2)