import time
import random
import logging
from dataclasses import dataclass
from typing import Any, Optional, Callable, List
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

class ServiceError(Exception):
    pass

class AggregatedServiceError(Exception):
    def __init__(self, errors: List[Exception]):
        self.errors = errors
        super().__init__(f"{len(errors)} errors occurred: {[str(e) for e in errors]}")

@dataclass
class Request:
    username: str
    password: str
    payload: Any

@dataclass
class Result:
    success: bool
    message: str
    data_id: Optional[str] = None

class AuthenticationService:
    def authenticate(self, username: str, password: str) -> str:
        if not username or not password:
            raise ServiceError("Missing credentials")
        if username == "locked":
            raise ServiceError("Account locked")
        if random.random() < 0.1:
            raise ServiceError("Auth transient failure")
        return f"token_{username}_{int(time.time())}"

class StorageService:
    def __init__(self):
        self._storage = {}
        self._counter = 0
    def store(self, token: str, payload: Any) -> str:
        if not token:
            raise ServiceError("Unauthorized")
        if random.random() < 0.1:
            raise ServiceError("Storage transient failure")
        self._counter += 1
        key = f"item_{self._counter}"
        self._storage[key] = {"token": token, "payload": payload, "ts": time.time()}
        return key
    def retrieve(self, key: str) -> Any:
        return self._storage.get(key)

class MessagingService:
    def send(self, token: str, message: str) -> bool:
        if not token:
            raise ServiceError("No token for messaging")
        if random.random() < 0.15:
            raise ServiceError("Messaging transient failure")
        return True

def retry(max_attempts: int = 3, base_delay: float = 0.1, max_delay: float = 1.0, jitter: float = 0.05):
    def decorator(fn: Callable):
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    delay = min(max_delay, base_delay * (2 ** (attempt - 1))) + random.uniform(-jitter, jitter)
                    time.sleep(max(0, delay))
            raise last_exc
        return wrapper
    return decorator

class ServiceCoordinator:
    def __init__(self, auth: Optional[AuthenticationService] = None,
                 storage: Optional[StorageService] = None,
                 messaging: Optional[MessagingService] = None,
                 max_retries: int = 3):
        self._auth = auth
        self._storage = storage
        self._messaging = messaging
        self._lock = threading.Lock()
        self._initialized = False
        self._max_retries = max_retries

    def initialize(self):
        with self._lock:
            if self._initialized:
                return
            if self._auth is None:
                self._auth = AuthenticationService()
            if self._storage is None:
                self._storage = StorageService()
            if self._messaging is None:
                self._messaging = MessagingService()
            self._initialized = True
            logger.info("Services initialized")

    def shutdown(self):
        with self._lock:
            if not self._initialized:
                return
            self._initialized = False
            self._auth = None
            self._storage = None
            self._messaging = None
            logger.info("Services shut down")

    @property
    def auth(self) -> AuthenticationService:
        if not self._initialized:
            self.initialize()
        return self._auth

    @property
    def storage(self) -> StorageService:
        if not self._initialized:
            self.initialize()
        return self._storage

    @property
    def messaging(self) -> MessagingService:
        if not self._initialized:
            self.initialize()
        return self._messaging

    def process(self, request: Request) -> Result:
        errors: List[Exception] = []
        token = None
        try:
            token = self._attempt_auth(request)
        except Exception as e:
            errors.append(e)
        data_id = None
        try:
            if token:
                data_id = self._attempt_store(token, request.payload)
        except Exception as e:
            errors.append(e)
        notify_ok = False
        try:
            if token:
                notify_ok = self._attempt_notify(token, f"Stored {data_id}" if data_id else "Store failed")
        except Exception as e:
            errors.append(e)
        if errors:
            raise AggregatedServiceError(errors)
        return Result(success=True, message="Processed successfully", data_id=data_id if data_id else None)

    @retry()
    def _attempt_auth(self, request: Request) -> str:
        return self.auth.authenticate(request.username, request.password)

    @retry()
    def _attempt_store(self, token: str, payload: Any) -> str:
        return self.storage.store(token, payload)

    @retry()
    def _attempt_notify(self, token: str, message: str) -> bool:
        return self.messaging.send(token, message)

if __name__ == "__main__":
    coordinator = ServiceCoordinator(max_retries=4)
    requests = [
        Request(username="alice", password="password", payload={"task": "backup"}),
        Request(username="", password="nope", payload={"task": "fail"}),
        Request(username="locked", password="x", payload={"task": "locked"}),
    ]
    for req in requests:
        try:
            res = coordinator.process(req)
            logger.info("Result: %s", res)
        except AggregatedServiceError as ae:
            logger.error("Aggregated errors: %s", ae)
            for err in ae.errors:
                logger.error(" - %s", err)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
    coordinator.shutdown()