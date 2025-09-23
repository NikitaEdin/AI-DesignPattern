import threading
import time
import random
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, TimeoutError

class ServiceError(Exception):
    pass

class TransientServiceError(ServiceError):
    pass

class AuthService:
    def validate_user(self, user_id: str) -> str:
        if not user_id or not isinstance(user_id, str):
            raise ServiceError("Invalid user identifier")
        if random.random() < 0.05:
            raise TransientServiceError("Auth transient failure")
        return f"token-{user_id}"

class DataService:
    def process(self, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not token.startswith("token-"):
            raise ServiceError("Unauthorized token")
        if random.random() < 0.1:
            raise TransientServiceError("Data processing transient error")
        time.sleep(0.05)
        result = {"processed": True, "input_summary": {"keys": len(payload)}}
        return result

class NotificationService:
    def send(self, user_id: str, message: str) -> bool:
        if random.random() < 0.15:
            raise TransientServiceError("Notification temporary issue")
        return True

@dataclass
class OperationResult:
    success: bool
    data: Optional[Dict[str, Any]]
    notifications_sent: int
    errors: List[str]
    attempts: int

class Coordinator:
    def __init__(self):
        self._auth = None
        self._data = None
        self._notify = None
        self._init_lock = threading.Lock()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=4)

    def _get_auth(self):
        if self._auth is None:
            with self._init_lock:
                if self._auth is None:
                    self._auth = AuthService()
        return self._auth

    def _get_data(self):
        if self._data is None:
            with self._init_lock:
                if self._data is None:
                    self._data = DataService()
        return self._data

    def _get_notify(self):
        if self._notify is None:
            with self._init_lock:
                if self._notify is None:
                    self._notify = NotificationService()
        return self._notify

    def _cache_key(self, user_id: str, payload: Dict[str, Any]) -> str:
        try:
            body = json.dumps(payload, sort_keys=True, default=str)
        except Exception:
            body = str(payload)
        return f"{user_id}:{body}"

    def _run_with_timeout(self, func, timeout: Optional[float]):
        future = self._executor.submit(func)
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            future.cancel()
            raise ServiceError("Operation timed out")

    def execute(self, user_id: str, payload: Dict[str, Any], retries: int = 3, timeout: Optional[float] = 2.0, use_cache: bool = True) -> OperationResult:
        attempts = 0
        errors: List[str] = []
        notifications = 0
        cache_key = self._cache_key(user_id, payload) if use_cache else None

        if cache_key:
            with self._cache_lock:
                cached = self._cache.get(cache_key)
                if cached:
                    return OperationResult(True, cached, 0, [], 0)

        while attempts < retries:
            attempts += 1
            try:
                auth = self._get_auth()
                token = self._run_with_timeout(lambda: auth.validate_user(user_id), timeout)
                data_service = self._get_data()
                processed = self._run_with_timeout(lambda: data_service.process(token, payload), timeout)
                notify = self._get_notify()
                sent = self._run_with_timeout(lambda: notify.send(user_id, f"Update for {user_id}"), timeout)
                notifications += 1 if sent else 0
                if cache_key:
                    with self._cache_lock:
                        self._cache[cache_key] = processed
                return OperationResult(True, processed, notifications, [], attempts)
            except TransientServiceError as e:
                errors.append(f"Transient: {e}")
                time.sleep(0.1 * attempts)
                continue
            except ServiceError as e:
                errors.append(f"Permanent: {e}")
                return OperationResult(False, None, notifications, errors, attempts)
            except Exception as e:
                errors.append(f"Unknown: {e}")
                return OperationResult(False, None, notifications, errors, attempts)
        return OperationResult(False, None, notifications, errors, attempts)

if __name__ == "__main__":
    coord = Coordinator()
    sample_payload = {"items": [1,2,3], "meta": {"priority": "high"}}
    for i in range(5):
        uid = f"user{i%3}"
        result = coord.execute(uid, sample_payload, retries=4, timeout=1.0, use_cache=True)
        print(f"Run {i+1} user={uid} success={result.success} attempts={result.attempts} errors={result.errors} data={result.data} notifications={result.notifications_sent}")