from abc import ABC, abstractmethod
from typing import Any, List, Optional


class ListModel:
    def __init__(self):
        self._items: List[Any] = []

    def add(self, item: Any) -> int:
        idx = len(self._items)
        self._items.append(item)
        return idx

    def insert(self, index: int, item: Any) -> int:
        if index < 0:
            index = 0
        if index > len(self._items):
            index = len(self._items)
        self._items.insert(index, item)
        return index

    def remove_at(self, index: int) -> Any:
        if index < 0 or index >= len(self._items):
            raise IndexError("Index out of range")
        return self._items.pop(index)

    def find_by_identity(self, item: Any) -> Optional[int]:
        for i, x in enumerate(self._items):
            if x is item:
                return i
        return None

    def snapshot(self) -> List[Any]:
        return list(self._items)

    def __repr__(self):
        return repr(self._items)


class BaseAction(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def revert(self) -> None:
        ...

    @property
    def reversible(self) -> bool:
        return True


class AddItemAction(BaseAction):
    def __init__(self, target: ListModel, item: Any):
        self.target = target
        self.item = item
        self._executed = False

    def execute(self) -> None:
        if self._executed:
            # allow redo: re-add same object
            self.target.add(self.item)
        else:
            self.target.add(self.item)
            self._executed = True

    def revert(self) -> None:
        idx = self.target.find_by_identity(self.item)
        if idx is None:
            raise RuntimeError("Item to remove not found during revert")
        self.target.remove_at(idx)


class RemoveItemAction(BaseAction):
    def __init__(self, target: ListModel, index: int):
        self.target = target
        self.index = index
        self.removed: Optional[Any] = None
        self._executed = False

    def execute(self) -> None:
        if self._executed:
            raise RuntimeError("Cannot execute removed twice without revert")
        self.removed = self.target.remove_at(self.index)
        self._executed = True

    def revert(self) -> None:
        if self.removed is None:
            raise RuntimeError("Nothing to revert")
        # Clamp index to valid range so ordering is preserved as much as possible
        insert_index = max(0, min(self.index, len(self.target.snapshot())))
        self.target.insert(insert_index, self.removed)
        self._executed = False
        self.removed = None


class GroupAction(BaseAction):
    def __init__(self, actions: List[BaseAction]):
        self.actions = list(actions)

    @property
    def reversible(self) -> bool:
        return all(a.reversible for a in self.actions)

    def execute(self) -> None:
        executed = []
        try:
            for a in self.actions:
                a.execute()
                executed.append(a)
        except Exception as e:
            rollback_errors = []
            for a in reversed(executed):
                try:
                    a.revert()
                except Exception as re:
                    rollback_errors.append(re)
            if rollback_errors:
                raise RuntimeError("Execution failed and rollback had errors") from e
            raise

    def revert(self) -> None:
        errors = []
        for a in reversed(self.actions):
            try:
                a.revert()
            except Exception as e:
                errors.append(e)
        if errors:
            raise RuntimeError("One or more reverts failed")


class Executor:
    def __init__(self, history_limit: int = 100):
        self._undo: List[BaseAction] = []
        self._redo: List[BaseAction] = []
        self.history_limit = max(1, history_limit)

    def perform(self, action: BaseAction) -> None:
        action.execute()
        if action.reversible:
            self._undo.append(action)
            self._redo.clear()
            if len(self._undo) > self.history_limit:
                self._undo.pop(0)

    def back(self) -> None:
        if not self._undo:
            raise RuntimeError("Nothing to undo")
        action = self._undo[-1]
        # attempt revert first to keep stacks consistent
        action.revert()
        self._undo.pop()
        self._redo.append(action)

    def forward(self) -> None:
        if not self._redo:
            raise RuntimeError("Nothing to redo")
        action = self._redo[-1]
        action.execute()
        self._redo.pop()
        self._undo.append(action)


if __name__ == "__main__":
    model = ListModel()
    execu = Executor(history_limit=10)

    a1 = AddItemAction(model, {"id": 1})
    a2 = AddItemAction(model, {"id": 2})
    execu.perform(a1)
    execu.perform(a2)
    print("After adds:", model)

    r1 = RemoveItemAction(model, 0)
    execu.perform(r1)
    print("After remove index 0:", model)

    execu.back()
    print("After undo remove:", model)

    group = GroupAction([AddItemAction(model, {"id": 3}), RemoveItemAction(model, 1)])
    try:
        execu.perform(group)
    except Exception as e:
        print("Group failed:", e)
    print("Final model:", model)
    execu.back()
    print("After undo group:", model)
    execu.forward()
    print("After redo group:", model)