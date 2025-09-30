import time
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    UNDONE = "undone"

class Task(ABC):
    def __init__(self):
        self.status = Status.PENDING
        self.timestamp = time.time()
    
    @abstractmethod
    def execute(self) -> bool:
        pass
    
    @abstractmethod
    def revoke(self) -> bool:
        pass
    
    def get_status(self) -> Status:
        return self.status

class LightManager:
    def __init__(self):
        self.lights = {"living": False, "bedroom": False, "kitchen": False}
    
    def switch(self, room: str, state: bool) -> bool:
        if room not in self.lights:
            return False
        self.lights[room] = state
        return True
    
    def get_state(self, room: str) -> Optional[bool]:
        return self.lights.get(room)

class LightSwitch(Task):
    def __init__(self, manager: LightManager, room: str, desired: bool):
        super().__init__()
        self.manager = manager
        self.room = room
        self.desired = desired
        self.previous = None
    
    def execute(self) -> bool:
        self.previous = self.manager.get_state(self.room)
        success = self.manager.switch(self.room, self.desired)
        if success:
            self.status = Status.EXECUTED
        return success
    
    def revoke(self) -> bool:
        if self.previous is None:
            return False
        success = self.manager.switch(self.room, self.previous)
        if success:
            self.status = Status.UNDONE
        return success

class MacroTask(Task):
    def __init__(self, tasks: List[Task]):
        super().__init__()
        self.tasks = tasks
        self.executed_tasks = []
    
    def execute(self) -> bool:
        for task in self.tasks:
            if task.execute():
                self.executed_tasks.append(task)
            else:
                self._rollback()
                return False
        self.status = Status.EXECUTED
        return True
    
    def revoke(self) -> bool:
        for task in reversed(self.executed_tasks):
            task.revoke()
        self.status = Status.UNDONE
        return True
    
    def _rollback(self):
        for task in self.executed_tasks:
            task.revoke()
        self.executed_tasks.clear()

class TaskQueue:
    def __init__(self):
        self.history = []
        self.future = []
    
    def submit(self, task: Task) -> bool:
        if task.execute():
            self.history.append(task)
            self.future.clear()
            return True
        return False
    
    def undo_last(self) -> bool:
        if not self.history:
            return False
        task = self.history.pop()
        if task.revoke():
            self.future.append(task)
            return True
        return False
    
    def redo_last(self) -> bool:
        if not self.future:
            return False
        task = self.future.pop()
        if task.execute():
            self.history.append(task)
            return True
        return False

if __name__ == "__main__":
    lights = LightManager()
    queue = TaskQueue()
    
    evening_routine = MacroTask([
        LightSwitch(lights, "living", True),
        LightSwitch(lights, "bedroom", True),
        LightSwitch(lights, "kitchen", False)
    ])
    
    queue.submit(evening_routine)
    queue.undo_last()
    queue.redo_last()