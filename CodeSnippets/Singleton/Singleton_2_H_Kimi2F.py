import threading
import functools

class SettingsHub:
    _lock = threading.RLock()
    _instance = None

    def __init__(self):
        raise RuntimeError('Use instance()')

    def __init_subclass__(cls, **kwargs):
        raise TypeError('Subclassing not allowed')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    inst = super().__new__(cls)
                    inst._configure()
                    cls._instance = inst
        return cls._instance

    def _configure(self):
        self._data = {}
        self._sealed = False

    def set(self, key, value):
        if self._sealed:
            raise AttributeError('Immutable after seal')
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def seal(self):
        self._sealed = True

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce__(self):
        return (self.instance, ())

def synchronized_singleton(cls):
    orig_new = cls.__new__
    cls._lock = threading.RLock()
    cls._instance = None

    @functools.wraps(orig_new)
    def __new__(cls_inner, *args, **kwargs):
        if cls_inner._instance is None:
            with cls_inner._lock:
                if cls_inner._instance is None:
                    cls_inner._instance = orig_new(cls_inner)
        return cls_inner._instance

    cls.__new__ = __new__
    return cls

@synchronized_singleton
class CacheStore:
    def __init__(self):
        self.storage = {}

    def store(self, key, value):
        self.storage[key] = value

    def retrieve(self, key):
        return self.storage.get(key)

if __name__ == '__main__':
    a = SettingsHub.instance()
    b = SettingsHub.instance()
    assert a is b
    a.set('theme', 'dark')
    assert b.get('theme') == 'dark'
    a.seal()
    try:
        b.set('user', 'john')
    except AttributeError as e:
        pass

    c = CacheStore()
    d = CacheStore()
    assert c is d
    c.store('token', 42)
    assert d.retrieve('token') == 42