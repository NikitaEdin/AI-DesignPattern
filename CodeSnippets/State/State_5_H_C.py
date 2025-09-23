from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json

class MachineCondition(ABC):
    @abstractmethod
    def power_on(self, context: 'SmartDevice') -> str:
        pass
    
    @abstractmethod
    def power_off(self, context: 'SmartDevice') -> str:
        pass
    
    @abstractmethod
    def perform_operation(self, context: 'SmartDevice') -> str:
        pass
    
    @abstractmethod
    def enter_maintenance(self, context: 'SmartDevice') -> str:
        pass

class OfflineCondition(MachineCondition):
    def power_on(self, context: 'SmartDevice') -> str:
        context.transition_to(OnlineCondition())
        return "Device powered on successfully"
    
    def power_off(self, context: 'SmartDevice') -> str:
        return "Device is already offline"
    
    def perform_operation(self, context: 'SmartDevice') -> str:
        return "Cannot perform operation: device is offline"
    
    def enter_maintenance(self, context: 'SmartDevice') -> str:
        context.transition_to(MaintenanceCondition())
        return "Entering maintenance mode from offline"

class OnlineCondition(MachineCondition):
    def power_on(self, context: 'SmartDevice') -> str:
        return "Device is already online"
    
    def power_off(self, context: 'SmartDevice') -> str:
        context.transition_to(OfflineCondition())
        context.reset_operations()
        return "Device powered off"
    
    def perform_operation(self, context: 'SmartDevice') -> str:
        context.increment_operations()
        if context.get_operations() >= 5:
            context.transition_to(MaintenanceCondition())
            return "Operation completed. Maintenance required after 5 operations"
        return f"Operation {context.get_operations()} completed successfully"
    
    def enter_maintenance(self, context: 'SmartDevice') -> str:
        context.transition_to(MaintenanceCondition())
        return "Entering maintenance mode"

class MaintenanceCondition(MachineCondition):
    def power_on(self, context: 'SmartDevice') -> str:
        return "Cannot power on: device in maintenance mode"
    
    def power_off(self, context: 'SmartDevice') -> str:
        context.transition_to(OfflineCondition())
        return "Maintenance completed, device powered off"
    
    def perform_operation(self, context: 'SmartDevice') -> str:
        return "Cannot perform operation: device under maintenance"
    
    def enter_maintenance(self, context: 'SmartDevice') -> str:
        return "Device is already in maintenance mode"

class SmartDevice:
    def __init__(self):
        self._condition: MachineCondition = OfflineCondition()
        self._operations_count: int = 0
        self._history: list = []
    
    def transition_to(self, condition: MachineCondition) -> None:
        self._history.append(type(self._condition).__name__)
        self._condition = condition
    
    def get_current_condition(self) -> str:
        return type(self._condition).__name__
    
    def increment_operations(self) -> None:
        self._operations_count += 1
    
    def get_operations(self) -> int:
        return self._operations_count
    
    def reset_operations(self) -> None:
        self._operations_count = 0
    
    def get_history(self) -> list:
        return self._history.copy()
    
    def power_on(self) -> str:
        return self._condition.power_on(self)
    
    def power_off(self) -> str:
        return self._condition.power_off(self)
    
    def perform_operation(self) -> str:
        return self._condition.perform_operation(self)
    
    def enter_maintenance(self) -> str:
        return self._condition.enter_maintenance(self)
    
    def get_device_info(self) -> Dict[str, Any]:
        return {
            'current_condition': self.get_current_condition(),
            'operations_count': self._operations_count,
            'condition_history': self._history
        }

if __name__ == "__main__":
    device = SmartDevice()
    
    actions = [
        ('power_on', device.power_on),
        ('perform_operation', device.perform_operation),
        ('perform_operation', device.perform_operation),
        ('perform_operation', device.perform_operation),
        ('perform_operation', device.perform_operation),
        ('perform_operation', device.perform_operation),
        ('power_off', device.power_off),
        ('enter_maintenance', device.enter_maintenance),
        ('power_off', device.power_off)
    ]
    
    for action_name, action in actions:
        result = action()
        print(f"{action_name}: {result} | Current: {device.get_current_condition()}")
    
    print(f"\nDevice Info: {json.dumps(device.get_device_info(), indent=2)}")