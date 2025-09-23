from abc import ABC, abstractmethod


class OperationBase(ABC):
    @property
    def is_reversible(self) -> bool:
        return True

    @abstractmethod
    def execute(self, receiver):
        pass

    @abstractmethod
    def revert(self, receiver):
        pass


class Calculator:
    def __init__(self, value=0):
        self.value = value

    def __repr__(self):
        return f"Calculator(value={self.value})"


class AddOp(OperationBase):
    def __init__(self, amount):
        self.amount = amount
        self._prev = None

    def execute(self, receiver: Calculator):
        self._prev = receiver.value
        receiver.value = receiver.value + self.amount
        return receiver.value

    def revert(self, receiver: Calculator):
        if self._prev is None:
            raise RuntimeError("Nothing to revert")
        receiver.value = self._prev
        return receiver.value


class MulOp(OperationBase):
    def __init__(self, factor):
        self.factor = factor
        self._prev = None

    def execute(self, receiver: Calculator):
        self._prev = receiver.value
        receiver.value = receiver.value * self.factor
        return receiver.value

    def revert(self, receiver: Calculator):
        if self._prev is None:
            raise RuntimeError("Nothing to revert")
        receiver.value = self._prev
        return receiver.value


class SetOp(OperationBase):
    def __init__(self, new_value):
        self.new_value = new_value

    @property
    def is_reversible(self) -> bool:
        return False

    def execute(self, receiver: Calculator):
        receiver.value = self.new_value
        return receiver.value

    def revert(self, receiver: Calculator):
        raise RuntimeError("Operation is not reversible")


class AggregateOperation(OperationBase):
    def __init__(self, operations):
        self.operations = list(operations)

    @property
    def is_reversible(self) -> bool:
        return all(getattr(op, "is_reversible", True) for op in self.operations)

    def execute(self, receiver: Calculator):
        executed = []
        last_result = None
        try:
            for op in self.operations:
                last_result = op.execute(receiver)
                executed.append(op)
            return last_result
        except Exception as exc:
            # attempt to revert reversible executed ops in reverse order
            errors = []
            for op in reversed(executed):
                if getattr(op, "is_reversible", True):
                    try:
                        op.revert(receiver)
                    except Exception as e:
                        errors.append(e)
            if errors:
                raise RuntimeError("Partial rollback failed") from exc
            raise

    def revert(self, receiver: Calculator):
        if not self.is_reversible:
            raise RuntimeError("Aggregate contains non-reversible sub-operations")
        errors = []
        for op in reversed(self.operations):
            try:
                op.revert(receiver)
            except Exception as e:
                errors.append(e)
        if errors:
            raise RuntimeError("Failed to revert aggregate")


class Controller:
    def __init__(self):
        self._history = []
        self._redo = []

    def perform(self, operation: OperationBase, receiver: Calculator):
        result = operation.execute(receiver)
        # clear redo on any new action
        self._redo.clear()
        if operation.is_reversible:
            self._history.append(operation)
        return result

    def undo(self, receiver: Calculator):
        if not self._history:
            raise RuntimeError("Nothing to undo")
        op = self._history[-1]
        if not op.is_reversible:
            raise RuntimeError("Operation is not reversible")
        # try revert before mutating history to keep invariants on failure
        result = op.revert(receiver)
        self._history.pop()
        self._redo.append(op)
        return result

    def redo(self, receiver: Calculator):
        if not self._redo:
            raise RuntimeError("Nothing to redo")
        op = self._redo[-1]
        # attempt execute; keep redo stack intact on failure
        result = op.execute(receiver)
        self._redo.pop()
        if op.is_reversible:
            self._history.append(op)
        return result


if __name__ == "__main__":
    calc = Calculator()
    ctrl = Controller()

    ctrl.perform(AddOp(5), calc)
    ctrl.perform(MulOp(3), calc)
    print(calc)  # Calculator(value=15)

    ctrl.undo(calc)
    print(calc)  # Calculator(value=5)

    ctrl.perform(SetOp(100), calc)
    print(calc)  # Calculator(value=100)
    # SetOp is not reversible, so undo will affect previous reversible op
    try:
        ctrl.undo(calc)  # will undo the last reversible (AddOp)
    except RuntimeError as e:
        print("Undo failed:", e)
    print(calc)

    # Aggregate with mixed reversibility: will execute but not be recorded
    mixed = AggregateOperation([AddOp(2), SetOp(77)])
    ctrl.perform(mixed, calc)
    print("After mixed aggregate:", calc)
    # Aggregate pure reversible: recorded and undoable as a single unit
    pure = AggregateOperation([AddOp(1), MulOp(2)])
    ctrl.perform(pure, calc)
    print("After pure aggregate:", calc)
    ctrl.undo(calc)
    print("After undo pure aggregate:", calc)