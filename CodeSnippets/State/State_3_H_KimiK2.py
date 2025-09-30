import random
import time
from abc import ABC, abstractmethod


class Connection:
    _pool = {}

    def __init__(self):
        self._current = self._fetch('Idle')
        self._idle_timeout = 0.3
        self._retry_limit = 3

    def _fetch(self, key):
        if key not in self._pool:
            if key == 'Idle':
                self._pool[key] = Idle(self)
            elif key == 'Active':
                self._pool[key] = Active(self)
            else:
                raise ValueError('Unknown type')
        return self._pool[key]

    def _swap(self, key):
        self._current = self._fetch(key)

    def start(self):
        self._current.initiate()

    def stop(self):
        self._current.terminate()

    def transmit(self):
        self._current.transmit()


class Mode(ABC):
    def __init__(self, ctx):
        self._ctx = ctx

    @abstractmethod
    def initiate(self): pass

    @abstractmethod
    def transmit(self): pass

    @abstractmethod
    def terminate(self): pass


class Idle(Mode):
    def initiate(self):
        print('Idle -> Active')
        self._ctx._swap('Active')

    def transmit(self):
        print('Cannot transmit in idle')

    def terminate(self):
        print('Already idle')


class Active(Mode):
    def __init__(self, ctx):
        super().__init__(ctx)
        self._attempts = 0
        self._base_delay = 0.05

    def initiate(self):
        print('Already active')

    def transmit(self):
        if self._attempts >= self._ctx._retry_limit:
            print('Exhausted, returning to idle')
            self.terminate()
            return
        jitter = random.uniform(0, 0.1)
        wait = self._base_delay * (2 ** self._attempts) + jitter
        time.sleep(wait)
        success = random.random() > 0.5
        if success:
            print('Transmit OK')
            self._attempts = 0
        else:
            self._attempts += 1
            print('Retry')

    def terminate(self):
        print('Active -> Idle')
        self._ctx._swap('Idle')


def main():
    conn = Connection()
    conn.start()
    conn.transmit()
    conn.stop()


if __name__ == '__main__':
    main()