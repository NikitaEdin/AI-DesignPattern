from abc import ABC, abstractmethod
from typing import Dict, Any
import threading

class Condition(ABC):
    @abstractmethod
    def handle_action(self, context: 'Context', action: str, **kwargs) -> Any:
        pass
    
    @abstractmethod
    def enter(self, context: 'Context') -> None:
        pass
    
    @abstractmethod
    def exit(self, context: 'Context') -> None:
        pass

class IdleCondition(Condition):
    def handle_action(self, context: 'Context', action: str, **kwargs) -> Any:
        if action == 'start':
            context.change_to('active')
            return "Started successfully"
        elif action == 'configure':
            context.data.update(kwargs)
            return "Configuration updated"
        return "Cannot perform action in idle mode"
    
    def enter(self, context: 'Context') -> None:
        context.data['last_idle_entry'] = context.get_timestamp()
    
    def exit(self, context: 'Context') -> None:
        context.data['idle_duration'] = context.get_timestamp() - context.data.get('last_idle_entry', 0)

class ActiveCondition(Condition):
    def handle_action(self, context: 'Context', action: str, **kwargs) -> Any:
        if action == 'pause':
            context.change_to('paused')
            return "Paused"
        elif action == 'stop':
            context.change_to('idle')
            return "Stopped"
        elif action == 'process':
            data = kwargs.get('data', '')
            return f"Processing: {data}"
        return "Invalid action for active mode"
    
    def enter(self, context: 'Context') -> None:
        context.data['start_time'] = context.get_timestamp()
        context.data['operations_count'] = 0
    
    def exit(self, context: 'Context') -> None:
        context.data['total_active_time'] = context.get_timestamp() - context.data.get('start_time', 0)

class PausedCondition(Condition):
    def handle_action(self, context: 'Context', action: str, **kwargs) -> Any:
        if action == 'resume':
            context.change_to('active')
            return "Resumed"
        elif action == 'stop':
            context.change_to('idle')
            return "Stopped from pause"
        return "Limited actions available while paused"
    
    def enter(self, context: 'Context') -> None:
        context.data['pause_time'] = context.get_timestamp()
    
    def exit(self, context: 'Context') -> None:
        pause_duration = context.get_timestamp() - context.data.get('pause_time', 0)
        context.data['total_pause_time'] = context.data.get('total_pause_time', 0) + pause_duration

class Context:
    def __init__(self):
        self._lock = threading.Lock()
        self._conditions = {
            'idle': IdleCondition(),
            'active': ActiveCondition(),
            'paused': PausedCondition()
        }
        self._current = self._conditions['idle']
        self._current_name = 'idle'
        self.data: Dict[str, Any] = {}
        self._timestamp_counter = 0
    
    def change_to(self, condition_name: str) -> None:
        with self._lock:
            if condition_name in self._conditions and condition_name != self._current_name:
                self._current.exit(self)
                self._current_name = condition_name
                self._current = self._conditions[condition_name]
                self._current.enter(self)
    
    def execute(self, action: str, **kwargs) -> Any:
        with self._lock:
            return self._current.handle_action(self, action, **kwargs)
    
    def get_current_condition(self) -> str:
        return self._current_name
    
    def get_timestamp(self) -> int:
        self._timestamp_counter += 1
        return self._timestamp_counter

if __name__ == "__main__":
    machine = Context()
    
    print(f"Initial condition: {machine.get_current_condition()}")
    print(machine.execute('configure', max_speed=100, timeout=30))
    print(machine.execute('start'))
    print(f"Current condition: {machine.get_current_condition()}")
    print(machine.execute('process', data='sample_data'))
    print(machine.execute('pause'))
    print(f"Current condition: {machine.get_current_condition()}")
    print(machine.execute('resume'))
    print(machine.execute('stop'))
    print(f"Final condition: {machine.get_current_condition()}")
    print(f"Machine data: {machine.data}")