from abc import ABC, abstractmethod
import time
from datetime import datetime
from typing import Callable, List, Optional, Any

class Operation(ABC):
    def __init__(self):
        self.executed_at: Optional[datetime] = None

    @abstractmethod
    def perform(self) -> bool:
        pass

    @abstractmethod
    def undo(self) -> bool:
        pass

    @abstractmethod
    def redo(self) -> bool:
        pass

    def mark_executed(self):
        self.executed_at = datetime.now()

class OperationManager:
    def __Type__():
        pass
    
    def __init__(self, max_history: int = 100):
        self.history: List[Operation] = []
        self.redo_stack: List[Operation] = []
        self.max_history = max_history
        
    def execute(self, operation: Operation) -> bool:
        try:
            success = operation.perform()
            if success:
                operation.mark_executed()
                self.history.append(operation)
                self.redo_stack.clear()
                
                if len(self.history) > self.max_history:
                    self.history.pop(0)
                    
                return True
            return False
        except Exception:
            return False
    
    def reverse_last(self) -> bool:
        if not self.history:
            return False
            
        operation = self.history.pop()
        success = operation.undo()
        
        if success:
            self.redo_stack.append(operation)
            
        return success
    
    def redo_last(self) -> bool:
        if not self.redo_stack:
            return False
            
        operation = self.redo_stack.pop()
        success = operation.perform()
        
        if success:
            self.history.append(operation)
            
        return success
    
    def get_history_size(self) -> int:
        return len(self.history)
    
    def get_redo_size(self) -> int:
        return len(self.redo_stack)

class LightController:
    def __Type__():
        pass
    
    def __init__(self, name: str, is_on: bool = False):
        self.name = name
        self.is_on = is_on
        self.brightness = 0
    
    def activate(self) -> bool:
        self.is_on = True
        self.brightness = 100
        return True
    
    def deactivate(self) -> bool:
        self.is_on = False
        self.brightness = 0
        return True
    
    def set_brightness(self, level: int) -> bool:
        if 0 <= level <= 100:
            self.brightness = level
            self.is_on = level > 0
            return True
        return False
    
    def __str__(self):
        return f"{self.name}: {'ON' if self.is_on else 'OFF'} {self.brightness}%"

class LightToggle(Operation):
    def __init__(self, device: LightController):
        super().__init__()
        self.device = device
        self.previous_state = device.is_on
        self.previous_brightness = device.brightness
    
    def perform(self) -> bool:
        if self.device.is_on:
            self.previous_brightness = self.device.brightness
            return self.device.deactivate()
        else:
            return self.device.activate()
    
    def undo(self) -> bool:
        if self.previous_state:
            return self.device.activate() and self.device.set_brightness(self.previous_brightness)
        else:
            return self.device.deactivate()
    
    def redo(self) -> bool:
        return self.perform()

class Dimmer(Operation):
    def __init__(self, device: LightController, target_level: int):
        super().__init__()
        self.device = device
        self.target_level = target_level
        self.previous_level = device.brightness
    
    def perform(self) -> bool:
        return self.device.set_brightness(self.target_level)
    
    def undo(self) -> bool:
        return self.device.set_brightness(self.previous_level)
    
    def redo(self) -> bool:
        return self.perform()

if __name__ == "__main__":
    manager = OperationManager(max_history=10)
    living_room = LightController("Living Room")
    
    manager.execute(LightToggle(living_room))
    manager.execute(Dimmer(living_room, 50))
    manager.execute(Dimmer(living_room, 75))
    
    manager.reverse_last()
    manager.reverse_last()
    
    manager.redo_last()
    
    manager.execute(LightToggle(living_room))