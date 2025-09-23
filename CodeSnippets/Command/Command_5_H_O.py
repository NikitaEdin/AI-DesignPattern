from abc import ABC, abstractmethod
from contextlib import contextmanager

class ActionBase(ABC):
    reversible = True

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class MacroAction(ActionBase):
    def __init__(self):
        self._actions = []
        self._executed = []

    @property
    def reversible(self):
        return all(a.reversible for a in self._actions)

    def add(self, action):
        self._actions.append(action)

    def execute(self):
        self._executed.clear()
        results = []
        try:
            for a in self._actions:
                res = a.execute()
                self._executed.append(a)
                results.append(res)
        except Exception:
            # rollback reversible executed sub-actions in reverse order
            for done in reversed(self._executed):
                if done.reversible:
                    try:
                        done.undo()
                    except Exception:
                        pass
            raise
        return results

    def undo(self):
        # undo reversible sub-actions in reverse order
        for a in reversed(self._executed):
            if a.reversible:
                a.undo()

class Executor:
    def __init__(self):
        self._history = []
        self._future = []
        self._batch_stack = []

    def submit(self, action):
        if self._batch_stack:
            self._batch_stack[-1].add(action)
            return None
        # execute immediately
        result = action.execute()
        # any new action invalidates redo history
        self._future.clear()
        if action.reversible:
            self._history.append(action)
        return result

    def undo(self):
        if not self._history:
            raise RuntimeError("Nothing to undo")
        action = self._history.pop()
        action.undo()
        self._future.append(action)

    def redo(self):
        if not self._future:
            raise RuntimeError("Nothing to redo")
        action = self._future.pop()
        action.execute()
        if action.reversible:
            self._history.append(action)

    @contextmanager
    def batch(self):
        macro = MacroAction()
        self._batch_stack.append(macro)
        try:
            yield macro
            completed = self._batch_stack.pop()
            completed.execute()
            # only archive if fully reversible
            if completed.reversible:
                self._history.append(completed)
                self._future.clear()
        except Exception:
            # ensure stack cleaned if exception inside with-block before pop
            if self._batch_stack and self._batch_stack[-1] is macro:
                self._batch_stack.pop()
            raise

# Receivers and concrete actions

class Light:
    def __init__(self):
        self.on = False

class ToggleLightAction(ActionBase):
    def __init__(self, light):
        self.light = light
        self._prev = None

    def execute(self):
        self._prev = self.light.on
        self.light.on = not self.light.on
        return self.light.on

    def undo(self):
        if self._prev is None:
            return
        self.light.on = self._prev

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

class DepositAction(ActionBase):
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def execute(self):
        self.account.balance += self.amount
        return self.account.balance

    def undo(self):
        self.account.balance -= self.amount

class WithdrawAction(ActionBase):
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def execute(self):
        if self.account.balance < self.amount:
            raise RuntimeError("Insufficient funds")
        self.account.balance -= self.amount
        return self.account.balance

    def undo(self):
        self.account.balance += self.amount

if __name__ == "__main__":
    exe = Executor()
    light = Light()
    acct = BankAccount(100)

    # simple actions
    exe.submit(ToggleLightAction(light))
    print("Light on?", light.on)
    exe.undo()
    print("Light on after undo?", light.on)
    exe.redo()
    print("Light on after redo?", light.on)

    # transactions
    exe.submit(DepositAction(acct, 50))
    print("Balance:", acct.balance)
    exe.submit(WithdrawAction(acct, 30))
    print("Balance after withdrawal:", acct.balance)
    exe.undo()
    print("Balance after undo withdrawal:", acct.balance)

    # batch example
    try:
        with exe.batch():
            exe.submit(DepositAction(acct, 200))
            exe.submit(WithdrawAction(acct, 500))  # may raise
            exe.submit(ToggleLightAction(light))
    except Exception as e:
        print("Batch failed:", e)
    print("Balance after batch attempt:", acct.balance, "Light on?", light.on)

    # successful batch
    with exe.batch():
        exe.submit(DepositAction(acct, 20))
        exe.submit(WithdrawAction(acct, 10))
    print("Balance after successful batch:", acct.balance)
    exe.undo()
    print("Balance after undoing batch:", acct.balance)