import uuid
from typing import Dict, Any


class AuthError(Exception):
    pass


class SaveError(Exception):
    pass


class NotificationError(Exception):
    pass


class AuthenticationService:
    def __init__(self):
        self._users = {"alice": "password123"}
        self._tokens: Dict[str, str] = {}

    def authenticate(self, username: str, password: str) -> str:
        if self._users.get(username) != password:
            raise AuthError("Invalid credentials")
        token = str(uuid.uuid4())
        self._tokens[token] = username
        return token

    def validate(self, token: str) -> str:
        user = self._tokens.get(token)
        if not user:
            raise AuthError("Invalid or expired token")
        return user


class DataRepository:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def create(self, owner: str, payload: Dict[str, Any]) -> str:
        record_id = str(uuid.uuid4())
        self._store[record_id] = {"owner": owner, "payload": payload}
        return record_id

    def delete(self, record_id: str) -> None:
        if record_id in self._store:
            del self._store[record_id]

    def get(self, record_id: str) -> Dict[str, Any]:
        return self._store.get(record_id, {})

    def all(self) -> Dict[str, Dict[str, Any]]:
        return dict(self._store)


class Notifier:
    def __init__(self, fail_on_notify: bool = False):
        self.fail_on_notify = fail_on_notify

    def send(self, user: str, message: str) -> None:
        if self.fail_on_notify:
            raise NotificationError("Failed to deliver notification")
        # simulate sending


class SystemCoordinator:
    def __init__(self, auth: AuthenticationService, repo: DataRepository, notifier: Notifier):
        self.auth = auth
        self.repo = repo
        self.notifier = notifier

    def submit_record(self, token: str, payload: Dict[str, Any]) -> str:
        try:
            owner = self.auth.validate(token)
            record_id = self.repo.create(owner, payload)
            try:
                self.notifier.send(owner, f"Record {record_id} created")
            except NotificationError as e:
                self.repo.delete(record_id)
                raise SaveError(f"Record creation rolled back due to notification failure: {e}") from e
            return record_id
        except AuthError as e:
            raise e


if __name__ == "__main__":
    auth_service = AuthenticationService()
    repo = DataRepository()
    notifier_ok = Notifier(fail_on_notify=False)
    notifier_fail = Notifier(fail_on_notify=True)

    controller_ok = SystemCoordinator(auth_service, repo, notifier_ok)
    controller_fail = SystemCoordinator(auth_service, repo, notifier_fail)

    try:
        token = auth_service.authenticate("alice", "password123")
        rid = controller_ok.submit_record(token, {"title": "Report", "content": "All good"})
        print("Created record:", rid)
        print("Store after success:", repo.all())
    except Exception as e:
        print("Error during success flow:", e)

    try:
        token2 = auth_service.authenticate("alice", "password123")
        rid2 = controller_fail.submit_record(token2, {"title": "Report 2", "content": "Should rollback"})
        print("Created record:", rid2)
    except Exception as e:
        print("Expected failure and rollback:", e)
        print("Store after rollback attempt:", repo.all())