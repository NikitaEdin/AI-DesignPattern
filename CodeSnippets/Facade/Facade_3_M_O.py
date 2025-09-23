import time
from typing import List, Dict


class ServiceError(Exception):
    pass


class AuthenticationService:
    def create_user(self, user_id: str) -> str:
        if not user_id or " " in user_id:
            raise ServiceError("Invalid user identifier")
        token = f"tok_{int(time.time())}_{user_id}"
        return token

    def remove_user(self, user_id: str) -> None:
        if not user_id:
            raise ServiceError("Cannot remove empty user id")
        return None


class DataService:
    def provision_storage(self, user_id: str) -> str:
        if user_id == "baduser":
            raise ServiceError("Storage provisioning failed")
        return f"storage://{user_id}"

    def remove_storage(self, storage_uri: str) -> None:
        if not storage_uri:
            raise ServiceError("Invalid storage uri")
        return None


class NotificationService:
    def send_welcome(self, email: str, token: str) -> bool:
        if "@" not in email:
            raise ServiceError("Invalid email address")
        return True


class SystemController:
    def __init__(self):
        self.auth = AuthenticationService()
        self.data = DataService()
        self.notify = NotificationService()
        self.audit: List[Dict] = []

    def _record(self, step: str, detail: str) -> None:
        self.audit.append({"time": time.time(), "step": step, "detail": detail})

    def onboard_user(self, user_id: str, email: str, dry_run: bool = False) -> Dict:
        self.audit.clear()
        try:
            self._record("start", f"onboarding {user_id}")
            token = self.auth.create_user(user_id)
            self._record("auth_created", token)
            storage = self.data.provision_storage(user_id)
            self._record("storage_provisioned", storage)
            if dry_run:
                self._record("dry_run", "no notification sent")
                return {"status": "dry_run_complete", "audit": list(self.audit)}
            self.notify.send_welcome(email, token)
            self._record("notification_sent", email)
            return {"status": "success", "user": user_id, "storage": storage, "audit": list(self.audit)}
        except Exception as e:
            self._record("error", str(e))
            try:
                if 'storage' in locals():
                    self.data.remove_storage(locals().get("storage"))
                    self._record("storage_removed", locals().get("storage"))
                if 'token' in locals():
                    self.auth.remove_user(user_id)
                    self._record("user_removed", user_id)
            except Exception as cleanup_err:
                self._record("cleanup_error", str(cleanup_err))
            return {"status": "failed", "error": str(e), "audit": list(self.audit)}

    def get_audit_log(self) -> List[Dict]:
        return list(self.audit)


if __name__ == "__main__":
    controller = SystemController()
    result1 = controller.onboard_user("alice", "alice@example.com")
    print(result1)
    result2 = controller.onboard_user("baduser", "bob@example.com")
    print(result2)
    result3 = controller.onboard_user("charlie", "invalid-email", dry_run=True)
    print(result3)