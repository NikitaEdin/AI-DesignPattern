import threading
import time
import random
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class AuthService:
    def authenticate(self, user_id: str) -> bool:
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user identifier")
        if user_id == "blocked":
            return False
        return True

class DataService:
    def __init__(self):
        self._call_count = 0

    def fetch(self, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._call_count += 1
        if payload.get("force_error"):
            raise RuntimeError("Data retrieval failed")
        result = {"user": user_id, "data": {"value": random.randint(0, 100)}, "call": self._call_count}
        return result

class NotificationService:
    def send(self, user_id: str, message: str) -> bool:
        if "fail_notify" in message:
            return False
        return True

class ServiceCoordinator:
    def __init__(self,
                 auth: Optional[AuthService] = None,
                 data: Optional[DataService] = None,
                 notifier: Optional[NotificationService] = None):
        self._auth = auth
        self._data = data
        self._notifier = notifier
        self._lock = threading.Lock()

    def _ensure_components(self):
        if self._auth and self._data and self._notifier:
            return
        with self._lock:
            if not self._auth:
                self._auth = AuthService()
            if not self._data:
                self._data = DataService()
            if not self._notifier:
                self._notifier = NotificationService()

    def perform_transaction(self, user_id: str, payload: Dict[str, Any], retries: int = 3, backoff: float = 0.2) -> Dict[str, Any]:
        self._ensure_components()
        result: Dict[str, Any] = {"user": user_id, "status": "unknown", "details": {}, "attempts": 0}
        try:
            result["attempts"] += 1
            auth_ok = self._auth.authenticate(user_id)
            result["details"]["auth"] = auth_ok
            if not auth_ok:
                result["status"] = "unauthorized"
                return result
        except Exception as e:
            result["status"] = "auth_error"
            result["details"]["auth_error"] = str(e)
            return result

        attempt = 0
        while attempt < retries:
            attempt += 1
            result["attempts"] = attempt
            try:
                data = self._data.fetch(user_id, payload)
                result["details"]["data"] = data
                break
            except Exception as e:
                logging.warning("DataService attempt %d failed: %s", attempt, e)
                result["details"].setdefault("data_errors", []).append(str(e))
                time.sleep(backoff * (2 ** (attempt - 1)))
        else:
            result["status"] = "data_failed"
            return result

        message = f"Processed data for {user_id}: {data.get('data')}"
        if payload.get("notify_fail"):
            message += " fail_notify"
        try:
            notify_ok = self._notifier.send(user_id, message)
            result["details"]["notification"] = notify_ok
            result["status"] = "completed" if notify_ok else "partial_completed"
        except Exception as e:
            result["status"] = "notify_error"
            result["details"]["notify_error"] = str(e)

        return result

if __name__ == "__main__":
    random.seed(42)
    coordinator = ServiceCoordinator()
    scenarios = [
        ("alice", {"action": "read"}),
        ("", {"action": "read"}),
        ("blocked", {"action": "read"}),
        ("bob", {"action": "update", "force_error": True}),
        ("carol", {"action": "notify", "notify_fail": True}),
    ]
    for user, payload in scenarios:
        logging.info("Running transaction for %r with payload %r", user, payload)
        outcome = coordinator.perform_transaction(user, payload, retries=2)
        logging.info("Outcome: %s", outcome)