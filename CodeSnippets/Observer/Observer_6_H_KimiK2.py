import threading
from typing import List, Any
from datetime import datetime

class Subject:
    def __init__(self):
        self._tip_followers: List['Follower'] = []
        self._tip_state: Any = None
        self._tip_lock = threading.Lock()
        self._tip_history: List[Any] = []

    def attach(self, follower: 'Follower') -> None:
        with self._tip_lock:
            if follower not in self._tip_followers:
                self._tip_followers.append(follower)

    def detach(self, follower: 'Follower') -> None:
        with self._tip_lock:
            if follower in self._tip_followers:
                self._tip_followers.remove(follower)

    def notify(self) -> None:
        with self._tip_lock:
            followers_copy = self._tip_followers.copy()
        for follower in followers_copy:
            follower.refresh(self)

    def set_state(self, state: Any) -> None:
        with self._tip_lock:
            self._tip_state = state
            self._tip_history.append((datetime.now(), state))
        self.notify()

    def get_state(self) -> Any:
        with self._tip_lock:
            return self._tip_state

    def get_history(self) -> List[Any]:
        with self._tip_lock:
            return self._tip_history.copy()

class Follower:
    def __init__(self, name: str):
        self._tip_name = name
        self._tip_last_seen = None

    def refresh(self, subject: Subject) -> None:
        current = subject.get_state()
        if self._tip_last_seen != current:
            self._tip_last_seen = current
            print(f"{self._tip_name} detected change: {current}")

class DataStream(Subject):
    def __init__(self):
        super().__init__()
        self._tip_counter = 0

    def push(self, value: Any) -> None:
        self._tip_counter += 1
        self.set_state({'seq': self._tip_counter, 'data': value})

if __name__ == "__main__":
    stream = DataStream()
    follower1 = Follower("Alpha")
    follower2 = Follower("Beta")
    stream.attach(follower1)
    stream.attach(follower2)
    stream.push("first")
    stream.detach(follower1)
    stream.push("second")