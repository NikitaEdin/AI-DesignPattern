import threading
import time
from typing import Any

class GlobalConfig:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, **kwargs):
        if self._initialized:
            return
        
        self._data = {}
        self._timestamp = time.time()
        self._access_count = 0
        self._initialized = True
        
        if kwargs:
            self._data.update(kwargs)
    
    def set_value(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = value
            self._access_count += 1
    
    def get_value(self, key: str, default: Any = None) -> Any:
        with self._lock:
            self._access_count += 1
            return self._data.get(key, default)
    
    def get_stats(self) -> dict:
        with self._lock:
            return {
                'created_at': self._timestamp,
                'access_count': self._access_count,
                'keys_count': len(self._data)
            }
    
    def __del__(self):
        if hasattr(self, '_data'):
            self._data.clear()

def worker_thread(config_id: int, iterations: int):
    config = GlobalConfig()
    for i in range(iterations):
        config.set_value(f'thread_{config_id}_key_{i}', i * 10)
        time.sleep(0.01)
        value = config.get_value(f'thread_{config_id}_key_{i}')
    return config.get_stats()

if __name__ == '__main__':
    config1 = GlobalConfig(app_name='MyApp', version='1.0.0')
    config2 = GlobalConfig(debug=True)
    
    assert id(config1) == id(config2)
    assert config1.get_value('app_name') == 'MyApp'
    assert config2.get_value('debug') is True
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker_thread, args=(i, 3))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    final_config = GlobalConfig()
    stats = final_config.get_stats()
    
    print("Final configuration state:")
    for key, value in sorted(final_config._data.items()):
        print(f"  {key}: {value}")
    
    print(f"\nStatistics: {stats}")