from dataclasses import dataclass
from typing import Dict, Optional


class AuthError(Exception):
    pass


class DBError(Exception):
    pass


class NotificationError(Exception):
    pass


@dataclass
class UserProfile:
    username: str
    email: Optional[str]
    full_name: str


class DatabaseConnector:
    def __init__(self):
        self._storage: Dict[str, UserProfile] = {
            "alice": UserProfile("alice", "alice@example.com", "Alice A."),
            "bob": UserProfile("bob", None, "Bob B."),
        }

    def fetch_profile(self, username: str) -> UserProfile:
        profile = self._storage.get(username)
        if not profile:
            raise DBError(f"user '{username}' not found")
        return profile


class AuthService:
    def __init__(self):
        self._credentials = {"alice": "wonder", "bob": "builder"}

    def authenticate(self, username: str, password: str) -> bool:
        expected = self._credentials.get(username)
        if expected is None:
            raise AuthError("unknown user")
        if expected != password:
            raise AuthError("invalid credentials")
        return True


class NotificationService:
    def send_email(self, email: str, subject: str, body: str) -> bool:
        if not email:
            raise NotificationError("missing email address")
        return True


class SystemCoordinator:
    def __init__(self):
        self._auth = AuthService()
        self._db = DatabaseConnector()
        self._notify = NotificationService()
        self._profile_cache: Dict[str, UserProfile] = {}

    def login_and_notify(self, username: str, password: str, subject: str, body: str) -> bool:
        try:
            self._auth.authenticate(username, password)
            profile = self._get_profile_cached(username)
            self._notify.send_email(profile.email or "", subject, body)
            return True
        except (AuthError, DBError, NotificationError) as e:
            print(f"operation failed: {e}")
            return False

    def _get_profile_cached(self, username: str) -> UserProfile:
        if username in self._profile_cache:
            return self._profile_cache[username]
        profile = self._db.fetch_profile(username)
        self._profile_cache[username] = profile
        return profile


if __name__ == "__main__":
    coordinator = SystemCoordinator()
    success = coordinator.login_and_notify("alice", "wonder", "Welcome", "Hello Alice!")
    print("alice success:", success)
    success = coordinator.login_and_notify("bob", "builder", "Update", "Hi Bob!")
    print("bob success:", success)
    success = coordinator.login_and_notify("bob", "wrong", "Fail", "This should fail")
    print("bob wrong password success:", success)
    success = coordinator.login_and_notify("charlie", "nopass", "No User", "No user here")
    print("charlie success:", success)