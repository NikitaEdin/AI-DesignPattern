import threading
import time
import uuid
import copy
import random


class AuthError(Exception):
    pass


class NotificationError(Exception):
    pass


class AuthService:
    def __init__(self, valid_tokens=None):
        self._valid = set(valid_tokens or [])

    def authenticate(self, token: str) -> bool:
        if token in self._valid:
            return True
        raise AuthError("invalid token")


class RepositoryService:
    def __init__(self):
        self._store = {}
        self._idempotency = {}
        self._lock = threading.Lock()

    def save(self, payload: dict, idempotency_key: str):
        with self._lock:
            existing = self._idempotency.get(idempotency_key)
            if existing is not None:
                return existing, False
            record_id = uuid.uuid4().hex
            self._store[record_id] = copy.deepcopy(payload)
            self._idempotency[idempotency_key] = record_id
            return record_id, True

    def get(self, record_id: str):
        with self._lock:
            data = self._store.get(record_id)
            return copy.deepcopy(data) if data is not None else None

    def delete(self, record_id: str):
        with self._lock:
            if record_id not in self._store:
                return False
            del self._store[record_id]
            keys = [k for k, v in list(self._idempotency.items()) if v == record_id]
            for k in keys:
                del self._idempotency[k]
            return True


class NotificationService:
    def __init__(self, failure_rate=0.2, rng=None, sleeper=time.sleep):
        self._failure_rate = float(failure_rate)
        self._rng = rng or random.Random()
        self._sleeper = sleeper

    def _attempt_send(self, payload):
        if self._rng.random() < self._failure_rate:
            raise NotificationError("transient send failure")
        return True

    def notify_with_retries(self, payload, max_retries=3, backoff_base=0.1):
        # max_retries is number of retries after the first attempt
        attempts = max_retries + 1
        for i in range(attempts):
            try:
                return self._attempt_send(payload)
            except NotificationError:
                if i == attempts - 1:
                    raise
                self._sleeper(backoff_base * (2 ** i))


class CoordinatorService:
    def __init__(self, auth: AuthService, repo: RepositoryService, notifier: NotificationService):
        self._auth = auth
        self._repo = repo
        self._notifier = notifier

    def process(self, token: str, payload: dict, idempotency_key: str, notify_retries=3):
        self._auth.authenticate(token)
        record_id, created = self._repo.save(payload, idempotency_key)
        try:
            self._notifier.notify_with_retries(payload, max_retries=notify_retries)
            return record_id, created
        except NotificationError:
            if created:
                # rollback only if this call actually created the record
                self._repo.delete(record_id)
            raise


if __name__ == "__main__":
    # deterministic RNG for predictable behavior in examples
    rng = random.Random(12345)
    auth = AuthService(valid_tokens=["token-abc"])
    repo = RepositoryService()
    notifier = NotificationService(failure_rate=1.0, rng=rng, sleeper=lambda t: None)  # force failure

    coordinator = CoordinatorService(auth, repo, notifier)

    # Pre-create a record with idempotency key 'key-existing'
    pre_id, _ = repo.save({"item": "preexisting"}, "key-existing")
    print("preexisting id:", pre_id)

    # Process with same idempotency key; notification will fail but should NOT delete preexisting record
    try:
        coordinator.process("token-abc", {"item": "preexisting"}, "key-existing", notify_retries=1)
    except NotificationError:
        pass

    still_there = repo.get(pre_id)
    print("still there after failed notify (should be present):", still_there is not None)

    # Now process a new key where creation happens and notification fails -> rollback removes it
    try:
        coordinator.process("token-abc", {"item": "to-rollback"}, "key-rollback", notify_retries=1)
    except NotificationError:
        pass

    rollback_id = repo._idempotency.get("key-rollback")
    print("rollback id mapping should be None:", rollback_id is None)