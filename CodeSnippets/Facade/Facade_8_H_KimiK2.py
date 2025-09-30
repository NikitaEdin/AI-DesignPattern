import threading
from typing import Optional, Dict, Any
import json
import time

class AuthenticationService:
    def __init__(self):
        self._users = {"admin": "secret123", "user": "pass456"}
        self._sessions = {}
        self._lock = threading.Lock()
    
    def login(self, username: str, password: str) -> Optional[str]:
        with self._lock:
            if username in self._users and self._users[username] == password:
                session_id = f"{username}_{int(time.time())}"
                self._sessions[session_id] = username
                return session_id
            return None
    
    def validate(self, session_id: str) -> bool:
        with self._lock:
            return session_id in self._sessions

class DatabaseService:
    def __init__(self):
        self._data = {"admin": {"balance": 1000}, "user": {"balance": 500}}
        self._lock = threading.Lock()
    
    def get_balance(self, username: str) -> int:
        with self._lock:
            return self._data.get(username, {}).get("balance", 0)
    
    def update_balance(self, username: str, amount: int) -> bool:
        with self._lock:
            if username in self._data:
                self._data[username]["balance"] += amount
                return True
            return False
    
    def get_report(self) -> Dict[str, Any]:
        with self._lock:
            return self._data.copy()

class NotificationService:
    def __init__(self):
        self._notifications = []
        self._lock = threading.Lock()
    
    def send(self, message: str) -> None:
        with self._lock:
            self._notifications.append({"time": time.time(), "message": message})
    
    def get_history(self) -> list:
        with self._lock:
            return self._notifications.copy()

class BankingPortal:
    def __init__(self):
        self._auth = AuthenticationService()
        self._db = DatabaseService()
        self._notify = NotificationService()
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        return self._auth.login(username, password)
    
    def check_balance(self, session_id: str) -> Optional[int]:
        if not self._auth.validate(session_id):
            return None
        username = session_id.split('_')[0]
        return self._db.get_balance(username)
    
    def transfer(self, session_id: str, amount: int) -> bool:
        if not self._auth.validate(session_id) or amount <= 0:
            return False
        username = session_id.split('_')[0]
        if self._db.update_balance(username, -amount):
            self._notify.send(f"Transferred {amount} from {username}")
            return True
        return False
    
    def get_statement(self, session_id: str) -> Optional[str]:
        if not self._auth.validate(session_id):
            return None
        username = session_id.split('_')[0]
        balance = self._db.get_balance(username)
        report = self._db.get_report()
        history = self._notify.get_history()
        return json.dumps({
            "username": username,
            "balance": balance,
            "system_report": report,
            "notifications": history[-5:]
        }, indent=2)

if __name__ == "__main__":
    portal = BankingPortal()
    
    session = portal.authenticate("admin", "secret123")
    if session:
        print("Balance:", portal.check_balance(session))
        portal.transfer(session, 100)
        print("New Balance:", portal.check_balance(session))
        print("Statement:", portal.get_statement(session))