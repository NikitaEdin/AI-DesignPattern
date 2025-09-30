import weakref
import threading
from typing import Set, List, Any
from abc import ABC, abstractmethod

class UpdateTarget(ABC):
    def __init__(self):
        self._watchers: Set[weakref.ref] = set()
        self._lock = threading.Lock()
    
    def attach(self, watcher):
        with self._lock:
            self._watchers.add(weakref.ref(watcher, self._cleanup))
    
    def detach(self, watcher):
        with self._lock:
            self._watchers.discard(weakref.ref(watcher))
    
    def _cleanup(self, ref):
        with self._lock:
            self._watchers.discard(ref)
    
    def _notify(self, event: str, data: Any = None):
        with self._lock:
            dead = set()
            for ref in self._watchers:
                watcher = ref()
                if watcher:
                    try:
                        watcher.refresh(self, event, data)
                    except Exception:
                        pass
                else:
                    dead.add(ref)
            self._watchers -= dead

class UpdateReceiver(ABC):
    @abstractmethod
    def refresh(self, target: UpdateTarget, event: str, data: Any):
        pass

class NewsTicker(UpdateTarget):
    def __init__(self):
        super().__init__()
        self._stories: List[str] = []
    
    def add_story(self, story: str):
        self._stories.append(story)
        self._notify('new_story', story)
    
    def clear(self):
        self._stories.clear()
        self._notify('cleared')

class Subscriber(UpdateReceiver):
    def __init__(self, name: str):
        self.name = name
        self.messages: List[str] = []
    
    def refresh(self, target: UpdateTarget, event: str, data: Any):
        self.messages.append(f'{event}: {data}')
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Subscriber) and self.name == other.name

if __name__ == '__main__':
    ticker = NewsTicker()
    alice = Subscriber('Alice')
    bob = Subscriber('Bob')
    ticker.attach(alice)
    ticker.attach(bob)
    ticker.add_story('Python 4.0 released')
    ticker.detach(bob)
    ticker.add_story('AI takes over')
    print(alice.messages)