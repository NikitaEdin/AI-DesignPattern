import time
import random

class ServiceError(Exception):
    pass

class AuthService:
    def __init__(self, users):
        self._users = users

    def authenticate(self, username, password):
        if username not in self._users or self._users[username] != password:
            raise ServiceError("Authentication failed for user")
        token = f"token-{username}-{int(time.time())}"
        return token

class ProfileService:
    def __init__(self, profiles):
        self._profiles = profiles

    def get_profile(self, token, user_id):
        if not token or not token.startswith("token-"):
            raise ServiceError("Invalid token")
        profile = self._profiles.get(user_id)
        if not profile:
            raise ServiceError("Profile not found")
        return profile

class MessagingService:
    def send_email(self, recipient, subject, body):
        if "@" not in recipient:
            raise ServiceError("Invalid email address")
        if "fail" in recipient:
            raise ServiceError("Simulated delivery failure")
        return {"status": "sent", "to": recipient, "subject": subject}

class SystemCoordinator:
    def __init__(self, auth_service, profile_service, messaging_service, max_retries=3, retry_delay=0.1):
        self.auth = auth_service
        self.profile = profile_service
        self.messaging = messaging_service
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def onboard_user(self, username, password, user_id):
        try:
            token = self.auth.authenticate(username, password)
        except ServiceError as e:
            raise ServiceError(f"Onboard failed during authentication: {e}")

        try:
            profile = self.profile.get_profile(token, user_id)
        except ServiceError as e:
            raise ServiceError(f"Onboard failed fetching profile: {e}")

        email = profile.get("email")
        subject = "Welcome!"
        body = f"Hello {profile.get('name')}, your account is ready."
        attempt = 0
        while attempt < self.max_retries:
            try:
                result = self.messaging.send_email(email, subject, body)
                return {"onboard": "success", "email_result": result, "profile": profile}
            except ServiceError as e:
                attempt += 1
                if attempt >= self.max_retries:
                    raise ServiceError(f"Onboard failed sending email after {attempt} attempts: {e}")
                time.sleep(self.retry_delay)

if __name__ == "__main__":
    users = {"alice": "password123", "bob": "secure!"}
    profiles = {
        "u1": {"name": "Alice A.", "email": "alice@example.com"},
        "u2": {"name": "Bob B.", "email": "bob@fail.example.com"}
    }

    auth = AuthService(users)
    profile = ProfileService(profiles)
    messaging = MessagingService()
    coordinator = SystemCoordinator(auth, profile, messaging)

    try:
        result = coordinator.onboard_user("alice", "password123", "u1")
        print("Onboard result:", result)
    except ServiceError as e:
        print("Error:", e)

    try:
        result = coordinator.onboard_user("bob", "secure!", "u2")
        print("Onboard result:", result)
    except ServiceError as e:
        print("Error:", e)

    try:
        result = coordinator.onboard_user("eve", "nopass", "u3")
        print("Onboard result:", result)
    except ServiceError as e:
        print("Error:", e)