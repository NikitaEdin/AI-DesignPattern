from abc import ABC, abstractmethod
from typing import Dict, Any
import threading

class Mode(ABC):
    @abstractmethod
    def connect(self, context: 'NetworkConnection') -> str:
        pass
    
    @abstractmethod
    def disconnect(self, context: 'NetworkConnection') -> str:
        pass
    
    @abstractmethod
    def send_data(self, context: 'NetworkConnection', data: str) -> str:
        pass

class DisconnectedMode(Mode):
    def connect(self, context: 'NetworkConnection') -> str:
        context._transition_to(ConnectedMode())
        return "Connection established"
    
    def disconnect(self, context: 'NetworkConnection') -> str:
        return "Already disconnected"
    
    def send_data(self, context: 'NetworkConnection', data: str) -> str:
        return "Cannot send data: Not connected"

class ConnectedMode(Mode):
    def connect(self, context: 'NetworkConnection') -> str:
        return "Already connected"
    
    def disconnect(self, context: 'NetworkConnection') -> str:
        context._transition_to(DisconnectedMode())
        return "Connection closed"
    
    def send_data(self, context: 'NetworkConnection', data: str) -> str:
        if len(data) > 1000:
            context._transition_to(ErrorMode())
            return "Data too large, connection error"
        context._add_to_history(f"Sent: {data}")
        return f"Data transmitted: {data}"

class ErrorMode(Mode):
    def connect(self, context: 'NetworkConnection') -> str:
        context._transition_to(ConnectedMode())
        return "Recovered from error, reconnected"
    
    def disconnect(self, context: 'NetworkConnection') -> str:
        context._transition_to(DisconnectedMode())
        return "Error cleared, disconnected"
    
    def send_data(self, context: 'NetworkConnection', data: str) -> str:
        return "Cannot send data: Connection in error mode"

class NetworkConnection:
    def __init__(self):
        self._current_mode = DisconnectedMode()
        self._history = []
        self._lock = threading.Lock()
        self._observers = []
    
    def _transition_to(self, mode: Mode):
        with self._lock:
            old_mode = self._current_mode.__class__.__name__
            self._current_mode = mode
            new_mode = self._current_mode.__class__.__name__
            self._notify_observers(f"Mode changed: {old_mode} -> {new_mode}")
    
    def _add_to_history(self, entry: str):
        with self._lock:
            self._history.append(entry)
            if len(self._history) > 10:
                self._history.pop(0)
    
    def add_observer(self, observer):
        self._observers.append(observer)
    
    def _notify_observers(self, message: str):
        for observer in self._observers:
            observer(message)
    
    def connect(self) -> str:
        return self._current_mode.connect(self)
    
    def disconnect(self) -> str:
        return self._current_mode.disconnect(self)
    
    def send_data(self, data: str) -> str:
        return self._current_mode.send_data(self, data)
    
    def get_current_mode(self) -> str:
        return self._current_mode.__class__.__name__
    
    def get_history(self) -> list:
        return self._history.copy()

if __name__ == "__main__":
    def mode_observer(message):
        print(f"Observer: {message}")
    
    connection = NetworkConnection()
    connection.add_observer(mode_observer)
    
    print(f"Initial mode: {connection.get_current_mode()}")
    print(connection.send_data("test"))
    print(connection.connect())
    print(connection.send_data("Hello World"))
    print(connection.send_data("x" * 1001))
    print(f"Current mode: {connection.get_current_mode()}")
    print(connection.connect())
    print(connection.disconnect())
    print(f"History: {connection.get_history()}")