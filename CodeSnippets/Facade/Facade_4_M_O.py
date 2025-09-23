import time, threading, hashlib, base64
class AuthenticationError(Exception): pass
class OrchestrationError(Exception): pass

class AuthService:
    def __init__(self):
        self._users = {"alice":"s3cr3t", "bob":"hunter2"}
        self._tokens = {}  # token -> expiry
    def login(self, username, password, ttl=5):
        if self._users.get(username) != password:
            raise AuthenticationError("invalid credentials")
        raw = f"{username}:{time.time()}"
        token = base64.urlsafe_b64encode(raw.encode()).decode()
        self._tokens[token] = time.time() + ttl
        return token
    def validate(self, token):
        exp = self._tokens.get(token)
        if not exp or time.time() > exp:
            raise AuthenticationError("token expired or invalid")
        return True

class ProfileService:
    def get_profile(self, username):
        # simulate data fetch
        return {"username": username, "joined": 2020 + (len(username) % 3)}

class AlertService:
    def notify(self, username, message):
        print(f"[ALERT] To {username}: {message}")

class Orchestrator:
    def __init__(self, auth:AuthService, profile:ProfileService, alert:AlertService):
        self._auth = auth
        self._profile = profile
        self._alert = alert
        self._cache = {}  # username -> (profile, expiry)
        self._lock = threading.Lock()
        self._cache_ttl = 30
    def authenticate_and_get_profile(self, username, password):
        try:
            token = self._auth.login(username, password)
        except AuthenticationError as e:
            raise OrchestrationError("authentication failed") from e
        # At this point credentials are valid; safe to use cached profile
        with self._lock:
            entry = self._cache.get(username)
            if entry and time.time() < entry[1]:
                return entry[0]
        # fetch fresh profile and cache it
        try:
            profile = self._profile.get_profile(username)
        except Exception as e:
            raise OrchestrationError("profile retrieval failed") from e
        with self._lock:
            self._cache[username] = (profile, time.time() + self._cache_ttl)
        # optionally send a login alert
        try:
            self._alert.notify(username, "Login successful")
        except Exception:
            pass
        return profile

if __name__ == "__main__":
    auth = AuthService()
    prof = ProfileService()
    alert = AlertService()
    svc = Orchestrator(auth, prof, alert)

    # successful login populates cache
    p1 = svc.authenticate_and_get_profile("alice", "s3cr3t")
    print("First fetch:", p1)
    # second call uses cached profile but still requires correct credentials
    p2 = svc.authenticate_and_get_profile("alice", "s3cr3t")
    print("Second fetch (cached):", p2)
    # wrong password will fail even if profile is cached
    try:
        svc.authenticate_and_get_profile("alice", "wrongpass")
    except OrchestrationError as e:
        print("Expected failure with wrong password:", e)