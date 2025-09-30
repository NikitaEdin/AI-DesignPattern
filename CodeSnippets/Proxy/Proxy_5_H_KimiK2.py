import time
import threading
from typing import Optional

class SensitiveData:
    def __init__(self):
        self._data = "Confidential Information"
    
    def get_info(self):
        return self._data

class AccessControl:
    def __init__(self, real_subject: SensitiveData):
        self._real_subject = real_subject
        self._access_count = 0
        self._lock = threading.Lock()
        self._last_access = 0
        self._cooldown = 1.0
    
    def get_info(self):
        current_time = time.time()
        with self._lock:
            if current_time - self._last_access < self._cooldown:
                raise Exception("Access denied: too frequent requests")
            self._last_access = current_time
            if self._access_count >= 3:
                raise Exception("Access denied: limit exceeded")
            self._access_count += 1
        return self._real_subject.get_info()

class MonitoringWrapper:
    def __init__(self, controlled_access: AccessControl):
        self._controlled_access = controlled_access
        self._request_log = []
    
    def get_info(self):
        request_time = time.strftime("%H:%M:%S")
        self._request_log.append(request_time)
        try:
            result = self._controlled_access.get_info()
            return f"[{request_time}] Access granted: {result}"
        except Exception as e:
            return f"[{request_time}] {str(e)}"
    
    def get_logs(self):
        return self._request_log

if __name__ == "__main__":
    real_data = SensitiveData()
    access_gate = AccessControl(real_data)
    monitored_access = MonitoringWrapper(access_gate)
    
    for i in range(5):
        time.sleep(1.2)
        print(monitored_access.get_info())
    
    print("Access log:", monitored_access.get_logs())