import time
import random
from dataclasses import dataclass
from typing import Optional, Dict, Any, Callable, ContextManager


class OperationError(Exception):
    pass


class AuthenticationError(OperationError):
    pass


class StorageError(OperationError):
    pass


class NotificationError(OperationError):
    pass


@dataclass
class CoordinatorConfig:
    max_notification_retries: int = 3
    retry_backoff: float = 0.1
    allow_anonymous: bool = False


class AuthService:
    def __init__(self, users: Optional[Dict[str, str]] = None):
        self._users = users or {}

    def authenticate(self, user_id: str, token: str) -> bool:
        if user_id not in self._users:
            raise AuthenticationError("User not found")
        if self._users[user_id] != token:
            raise AuthenticationError("Invalid token")
        return True


class StorageService:
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._transaction_backup: Optional[Dict[str, Any]] = None

    def begin_transaction(self) -> None:
        if self._transaction_backup is not None:
            raise StorageError("Transaction already active")
        self._transaction_backup = dict(self._store)

    def commit(self) -> None:
        if self._transaction_backup is None:
            raise StorageError("No active transaction")
        self._transaction_backup = None

    def rollback(self) -> None:
        if self._transaction_backup is None:
            raise StorageError("No active transaction")
        self._store = self._transaction_backup
        self._transaction_backup = None

    def save(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get(self, key: str) -> Any:
        return self._store.get(key)


class NotificationService:
    def __init__(self, failure_rate: float = 0.2):
        self.failure_rate = failure_rate

    def send(self, recipient: str, message: str) -> None:
        if random.random() < self.failure_rate:
            raise NotificationError("Transient send failure")
        # simulate send success


class ApplicationCoordinator(ContextManager):
    def __init__(self, config: Optional[CoordinatorConfig] = None,
                 user_store: Optional[Dict[str, str]] = None,
                 notifier_failure_rate: float = 0.2):
        self.config = config or CoordinatorConfig()
        self._user_store = user_store or {}
        self._auth: Optional[AuthService] = None
        self._storage: Optional[StorageService] = None
        self._notifier: Optional[NotificationService] = None
        self._active = False
        self._notifier_failure_rate = notifier_failure_rate

    def _init_auth(self) -> AuthService:
        if self._auth is None:
            self._auth = AuthService(self._user_store)
        return self._auth

    def _init_storage(self) -> StorageService:
        if self._storage is None:
            self._storage = StorageService()
        return self._storage

    def _init_notifier(self) -> NotificationService:
        if self._notifier is None:
            self._notifier = NotificationService(self._notifier_failure_rate)
        return self._notifier

    def __enter__(self):
        if self._active:
            raise OperationError("Coordinator already active")
        self._active = True
        self._init_storage().begin_transaction()
        return self

    def __exit__(self, exc_type, exc, tb):
        if not self._active:
            return False
        storage = self._storage
        if exc is None:
            try:
                storage.commit()
            except Exception as e:
                storage.rollback()
                self._active = False
                raise
        else:
            storage.rollback()
        self._active = False
        return False

    def process_request(self, user_id: Optional[str], token: Optional[str], payload: Dict[str, Any]) -> Dict[str, Any]:
        if user_id is None:
            if not self.config.allow_anonymous:
                raise AuthenticationError("Anonymous access disabled")
            authenticated = True
        else:
            authenticated = self._init_auth().authenticate(user_id, token or "")

        if not authenticated:
            raise AuthenticationError("Authentication failed")

        storage = self._init_storage()
        key = f"{user_id or 'anon'}:{int(time.time() * 1000)}"
        try:
            storage.save(key, payload)
        except Exception as e:
            raise StorageError(f"Failed to save payload: {e}") from e

        notify_result = self._attempt_notify(user_id or "anonymous", "Your data was stored")
        return {"status": "ok", "key": key, "notification": notify_result}

    def _attempt_notify(self, recipient: str, message: str) -> str:
        notifier = self._init_notifier()
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.config.max_notification_retries + 1):
            try:
                notifier.send(recipient, message)
                return f"sent (attempt {attempt})"
            except NotificationError as e:
                last_exc = e
                time.sleep(self.config.retry_backoff * attempt)
        raise NotificationError(f"Failed after {self.config.max_notification_retries} attempts") from last_exc


if __name__ == "__main__":
    random.seed(0)
    users = {"alice": "token123", "bob": "secret"}
    coord = ApplicationCoordinator(CoordinatorConfig(max_notification_retries=5, retry_backoff=0.01), user_store=users, notifier_failure_rate=0.5)

    try:
        with coord as app:
            result = app.process_request("alice", "token123", {"value": 42})
            print("Success:", result)
    except Exception as e:
        print("Error during operation:", type(e).__name__, str(e))

    try:
        with coord as app:
            result = app.process_request("eve", "bad", {"value": 99})
            print("Should not print:", result)
    except Exception as e:
        print("Expected failure:", type(e).__name__, str(e))

    coord2 = ApplicationCoordinator(CoordinatorConfig(allow_anonymous=True), user_store=users, notifier_failure_rate=0.0)
    try:
        with coord2 as app:
            result = app.process_request(None, None, {"anon": True})
            print("Anonymous success:", result)
    except Exception as e:
        print("Unexpected error:", type(e).__name__, str(e))