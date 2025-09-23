import threading
import time
import random
import logging
from functools import lru_cache
from typing import Any, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

class AuthError(Exception):
    pass

class ValidationError(Exception):
    pass

class PersistenceError(Exception):
    pass

class NotificationError(Exception):
    pass

class AuthenticationService:
    def __init__(self):
        self._valid_tokens = {"alice": "token123", "bob": "token456"}
        self._lock = threading.Lock()

    @lru_cache(maxsize=128)
    def validate(self, user: str, token: str) -> bool:
        time.sleep(0.05)
        expected = self._valid_tokens.get(user)
        if expected is None:
            raise AuthError("unknown user")
        if token != expected:
            raise AuthError("invalid token")
        return True

    def revoke(self, user: str):
        with self._lock:
            self._valid_tokens.pop(user, None)
            self.validate.cache_clear()

class DatabaseService:
    def __init__(self):
        self._storage: Dict[int, Dict[str, Any]] = {}
        self._id_seq = 0
        self._lock = threading.Lock()

    def save(self, user: str, payload: Dict[str, Any]) -> int:
        if not isinstance(payload, dict) or not payload:
            raise ValidationError("payload must be a non-empty dict")
        if len(str(payload)) > 1000:
            raise ValidationError("payload too large")
        with self._lock:
            self._id_seq += 1
            rec_id = self._id_seq
            if random.random() < 0.05:
                raise PersistenceError("transient db error")
            self._storage[rec_id] = {"user": user, "payload": payload, "ts": time.time()}
            return rec_id

    def get(self, rec_id: int) -> Optional[Dict[str, Any]]:
        return self._storage.get(rec_id)

class MessagingService:
    def __init__(self, backoff: float = 0.1, attempts: int = 3):
        self.backoff = backoff
        self.attempts = attempts

    def send(self, user: str, message: str) -> bool:
        if not message:
            raise NotificationError("empty message")
        last_exc = None
        for attempt in range(1, self.attempts + 1):
            time.sleep(self.backoff * attempt)
            if random.random() < 0.8:
                logger.info("message sent to %s on attempt %d", user, attempt)
                return True
            last_exc = NotificationError("transient send failure")
        raise last_exc or NotificationError("failed to send")

class SystemOrchestrator:
    def __init__(self):
        self._lock = threading.Lock()
        self._auth_service: Optional[AuthenticationService] = None
        self._db_service: Optional[DatabaseService] = None
        self._msg_service: Optional[MessagingService] = None

    @property
    def auth(self) -> AuthenticationService:
        if self._auth_service is None:
            with self._lock:
                if self._auth_service is None:
                    self._auth_service = AuthenticationService()
        return self._auth_service

    @property
    def db(self) -> DatabaseService:
        if self._db_service is None:
            with self._lock:
                if self._db_service is None:
                    self._db_service = DatabaseService()
        return self._db_service

    @property
    def messenger(self) -> MessagingService:
        if self._msg_service is None:
            with self._lock:
                if self._msg_service is None:
                    self._msg_service = MessagingService()
        return self._msg_service

    def execute_transaction(self, user: str, token: str, payload: Dict[str, Any], notify: bool = True) -> Dict[str, Any]:
        start = time.time()
        try:
            self.auth.validate(user, token)
            rec_id = self._attempt_save(user, payload)
            result = {"status": "ok", "record_id": rec_id, "latency": time.time() - start}
            if notify:
                try:
                    self.messenger.send(user, f"Record {rec_id} created")
                    result["notified"] = True
                except NotificationError as e:
                    result["notified"] = False
                    result["notification_error"] = str(e)
            return result
        except (AuthError, ValidationError, PersistenceError) as e:
            return {"status": "error", "error": str(e), "latency": time.time() - start}

    def _attempt_save(self, user: str, payload: Dict[str, Any], retries: int = 3) -> int:
        attempt = 0
        while attempt < retries:
            attempt += 1
            try:
                return self.db.save(user, payload)
            except PersistenceError:
                time.sleep(0.05 * attempt)
        raise PersistenceError("max retries reached")

if __name__ == "__main__":
    orchestrator = SystemOrchestrator()
    examples = [
        ("alice", "token123", {"item": "book", "qty": 1}),
        ("bob", "wrong", {"item": "pen"}),
        ("carol", "token789", {"x": "y"}),
        ("alice", "token123", {}),
    ]
    for user, token, payload in examples:
        result = orchestrator.execute_transaction(user, token, payload, notify=True)
        print(user, result)