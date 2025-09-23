import threading
import time
import random
from typing import Any, Dict, List

class CoordinatorError(Exception):
    pass

class TransientError(CoordinatorError):
    pass

class PermanentError(CoordinatorError):
    pass

class AggregateError(CoordinatorError):
    def __init__(self, errors: List[Exception]):
        self.errors = errors
        messages = "; ".join(f"{type(e).__name__}: {e}" for e in errors)
        super().__init__(messages)

def retry(attempts: int = 3, delay: float = 0.2, exceptions=(TransientError,)):
    def deco(fn):
        def wrapper(*args, **kwargs):
            last = None
            for i in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    last = e
                    time.sleep(delay * (2 ** i))
                except Exception:
                    raise
            raise last
        return wrapper
    return deco

class UserAuth:
    def __init__(self, users: Dict[str, Dict[str, Any]]):
        self._users = users

    def authenticate(self, user_id: str) -> Dict[str, Any]:
        if user_id not in self._users:
            raise PermanentError(f"user '{user_id}' not found")
        user = self._users[user_id]
        if not user.get("active", False):
            raise PermanentError(f"user '{user_id}' inactive")
        return user

class RecordStore:
    def __init__(self):
        self._lock = threading.RLock()
        self._store: Dict[str, Dict[str, Any]] = {}

    def fetch(self, record_id: str) -> Dict[str, Any]:
        with self._lock:
            if record_id not in self._store:
                raise PermanentError(f"record '{record_id}' missing")
            return dict(self._store[record_id])

    def save(self, record_id: str, data: Dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise PermanentError("invalid record data")
        with self._lock:
            self._store[record_id] = dict(data)

class Messenger:
    def __init__(self, fail_rate: float = 0.2):
        self.fail_rate = fail_rate
        random.seed(0)

    def send(self, recipient: str, message: str) -> None:
        if random.random() < self.fail_rate:
            raise TransientError("temporary messaging failure")
        if "@" not in recipient:
            raise PermanentError("invalid recipient address")
        # simulate send

class ServiceCoordinator:
    def __init__(self, users: Dict[str, Dict[str, Any]], messenger_fail_rate: float = 0.2):
        self._users = users
        self._lock = threading.Lock()
        self._store = None
        self._auth = None
        self._messenger = None
        self._messenger_fail_rate = messenger_fail_rate

    def _init_services(self):
        with self._lock:
            if self._auth is None:
                self._auth = UserAuth(self._users)
            if self._store is None:
                self._store = RecordStore()
            if self._messenger is None:
                self._messenger = Messenger(fail_rate=self._messenger_fail_rate)

    @retry(attempts=3, delay=0.1, exceptions=(TransientError,))
    def _send_notification(self, recipient: str, message: str) -> None:
        self._messenger.send(recipient, message)

    def perform_user_update(self, user_id: str, record_id: str, patch: Dict[str, Any]) -> Dict[str, Any]:
        self._init_services()
        errors: List[Exception] = []
        original = None
        try:
            user = self._auth.authenticate(user_id)
        except Exception as e:
            raise e

        try:
            original = self._store.fetch(record_id)
        except Exception as e:
            raise e

        updated = dict(original)
        updated.update(patch)
        if not updated.get("title"):
            raise PermanentError("record must have a title")

        try:
            self._store.save(record_id, updated)
        except Exception as e:
            raise e

        try:
            recipient = user.get("email", "")
            self._send_notification(recipient, f"Record {record_id} updated")
        except Exception as e:
            errors.append(e)

        if errors:
            try:
                self._store.save(record_id, original)
            except Exception as rollback_err:
                errors.append(rollback_err)
            raise AggregateError(errors)

        return updated

if __name__ == "__main__":
    users = {
        "alice": {"email": "alice@example.com", "active": True},
        "bob": {"email": "bobexample.com", "active": True},
        "carol": {"email": "carol@example.com", "active": False},
    }
    coordinator = ServiceCoordinator(users, messenger_fail_rate=0.5)
    coordinator._init_services()
    coordinator._store.save("r1", {"title": "Initial", "content": "Hello"})

    try:
        result = coordinator.perform_user_update("alice", "r1", {"content": "Updated"})
        print("Update successful:", result)
    except Exception as e:
        print("Error during update:", type(e).__name__, e)

    try:
        result = coordinator.perform_user_update("bob", "r1", {"content": "Another change"})
        print("Update successful:", result)
    except Exception as e:
        print("Error during update:", type(e).__name__, e)

    try:
        coordinator.perform_user_update("carol", "r1", {"content": "Should fail"})
    except Exception as e:
        print("Error during update:", type(e).__name__, e)