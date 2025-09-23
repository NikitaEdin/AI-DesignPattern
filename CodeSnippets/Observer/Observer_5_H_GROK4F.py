import weakref

class CentralCoordinator:
    def __init__(self):
        self._subscribers = []
        self._state = None

    def attach(self, subscriber, priority=0):
        if any(ref() is subscriber for ref, _ in self._subscribers):
            return
        weak_sub = weakref.ref(subscriber)
        self._subscribers.append((priority, weak_sub))

    def detach(self, subscriber):
        self._subscribers = [(p, r) for p, r in self._subscribers if r() is not subscriber]

    def set_state(self, new_state):
        self._state = new_state
        self._notify()

    def _notify(self):
        active_subs = [(p, r()) for p, r in self._subscribers if r() is not None]
        active_subs.sort(key=lambda x: x[0])
        for _, sub in active_subs:
            try:
                sub.receive_update(self._state)
            except Exception:
                pass  # Ignore errors from individual subscribers

    def get_state(self):
        return self._state

class DataReceiver:
    def __init__(self, name):
        self.name = name

    def receive_update(self, state):
        print(f"{self.name} received state: {state}")

def main():
    coord = CentralCoordinator()
    
    rec1 = DataReceiver("Receiver A")
    rec2 = DataReceiver("Receiver B")
    rec3 = DataReceiver("Receiver C")
    
    coord.attach(rec1, priority=2)
    coord.attach(rec2, priority=1)
    coord.attach(rec3, priority=3)
    
    print("Initial state: None")
    
    coord.set_state("Initial Update")
    # Expected: B (1), A (2), C (3)
    
    coord.detach(rec2)
    
    coord.set_state("Second Update")
    # Expected: B detached, so A (2), C (3)
    
    # Test weakref: let rec1 go out of scope implicitly
    del rec1
    import gc
    gc.collect()
    
    coord.set_state("Final Update")
    # Expected: Only C remains active

if __name__ == "__main__":
    main()