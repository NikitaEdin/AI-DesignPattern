from typing import Any, List, Dict, Optional, Sequence

_SENTINEL = object()

class ExecutionError(Exception):
    pass

class AggregateError(Exception):
    def __init__(self, message: str, errors: Sequence[Exception]):
        super().__init__(message)
        self.errors = list(errors)

class ActionBase:
    reversible: bool = True
    def execute(self) -> None:
        raise NotImplementedError
    def undo(self) -> None:
        raise NotImplementedError

class ListHandler:
    def __init__(self):
        self.store: List[Any] = []
    def append(self, value: Any) -> int:
        self.store.append(value)
        return len(self.store) - 1
    def insert(self, index: int, value: Any) -> int:
        if index < 0:
            index = max(0, len(self.store) + index + 1)
        self.store.insert(index, value)
        return index
    def remove_at(self, index: int) -> Any:
        return self.store.pop(index)

class DictHandler:
    def __init__(self):
        self.store: Dict[Any, Any] = {}
    def set_key(self, key: Any, value: Any) -> None:
        self.store[key] = value
    def delete_key(self, key: Any) -> None:
        del self.store[key]

class AddItemAction(ActionBase):
    def __init__(self, receiver: ListHandler, value: Any, index: Optional[int] = None):
        self.receiver = receiver
        self.value = value
        self.requested_index = index
        self.actual_index: Optional[int] = None
    def execute(self) -> None:
        if self.requested_index is None:
            self.actual_index = self.receiver.append(self.value)
        else:
            self.actual_index = self.receiver.insert(self.requested_index, self.value)
    def undo(self) -> None:
        if self.actual_index is None:
            raise ExecutionError("Nothing to undo")
        self.receiver.remove_at(self.actual_index)
        self.actual_index = None

class RemoveItemAction(ActionBase):
    def __init__(self, receiver: ListHandler, index: int):
        self.receiver = receiver
        self.index = index
        self.removed_value: Any = _SENTINEL
    def execute(self) -> None:
        self.removed_value = self.receiver.remove_at(self.index)
    def undo(self) -> None:
        if self.removed_value is _SENTINEL:
            raise ExecutionError("Nothing to undo")
        self.receiver.insert(self.index, self.removed_value)
        self.removed_value = _SENTINEL

class SetKeyAction(ActionBase):
    def __init__(self, receiver: DictHandler, key: Any, value: Any):
        self.receiver = receiver
        self.key = key
        self.value = value
        self.old_value: Any = _SENTINEL
        self.had_old: bool = False
    def execute(self) -> None:
        self.had_old = self.key in self.receiver.store
        if self.had_old:
            self.old_value = self.receiver.store.get(self.key, _SENTINEL)
        else:
            self.old_value = _SENTINEL
        self.receiver.set_key(self.key, self.value)
    def undo(self) -> None:
        if self.had_old:
            self.receiver.set_key(self.key, self.old_value)
        else:
            if self.key in self.receiver.store:
                self.receiver.delete_key(self.key)

class CompositeAction(ActionBase):
    def __init__(self, actions: Sequence[ActionBase]):
        self.actions = list(actions)
    @property
    def reversible(self) -> bool:
        return all(a.reversible for a in self.actions)
    def execute(self) -> None:
        executed: List[ActionBase] = []
        errors: List[Exception] = []
        for a in self.actions:
            try:
                a.execute()
                executed.append(a)
            except Exception as e:
                errors.append(e)
                rollback_errors: List[Exception] = []
                for r in reversed(executed):
                    try:
                        r.undo()
                    except Exception as re:
                        rollback_errors.append(re)
                if rollback_errors:
                    raise AggregateError("Failure during execute and rollback", errors + rollback_errors)
                raise ExecutionError(f"Failure during execute: {e}") from e
    def undo(self) -> None:
        undone: List[ActionBase] = []
        undo_errors: List[Exception] = []
        for a in reversed(self.actions):
            try:
                a.undo()
                undone.append(a)
            except Exception as e:
                undo_errors.append(e)
                restore_errors: List[Exception] = []
                for r in reversed(undone):
                    try:
                        r.execute()
                    except Exception as re:
                        restore_errors.append(re)
                if restore_errors:
                    raise AggregateError("Partial undo failed and restore failed", undo_errors + restore_errors)
                raise ExecutionError(f"Undo failed: {e}") from e

class Controller:
    def __init__(self):
        self._history: List[ActionBase] = []
        self._redo: List[ActionBase] = []
    def execute_action(self, action: ActionBase) -> None:
        action.execute()
        if getattr(action, "reversible", True):
            self._history.append(action)
            self._redo.clear()
    def undo(self) -> None:
        if not self._history:
            raise ExecutionError("Nothing to undo")
        action = self._history.pop()
        try:
            action.undo()
            self._redo.append(action)
        except Exception as e:
            self._history.append(action)
            raise
    def redo(self) -> None:
        if not self._redo:
            raise ExecutionError("Nothing to redo")
        action = self._redo.pop()
        try:
            action.execute()
            self._history.append(action)
        except Exception:
            self._redo.append(action)
            raise

if __name__ == "__main__":
    lst = ListHandler()
    dct = DictHandler()
    ctrl = Controller()

    a1 = AddItemAction(lst, "a")
    a2 = AddItemAction(lst, "b")
    a3 = AddItemAction(lst, "x", index=1)
    s1 = SetKeyAction(dct, "k", 1)
    s2 = SetKeyAction(dct, "k", None)

    ctrl.execute_action(a1)
    ctrl.execute_action(a2)
    ctrl.execute_action(a3)
    ctrl.execute_action(s1)
    ctrl.execute_action(s2)

    macro = CompositeAction([RemoveItemAction(lst, 0), SetKeyAction(dct, "new", "v")])
    ctrl.execute_action(macro)

    print("list:", lst.store)
    print("dict:", dct.store)

    ctrl.undo()
    ctrl.undo()
    print("after two undos list:", lst.store)
    print("after two undos dict:", dct.store)

    ctrl.redo()
    ctrl.redo()
    print("after two redos list:", lst.store)
    print("after two redos dict:", dct.store)