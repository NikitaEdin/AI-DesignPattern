import threading
from typing import Optional
from contextlib import contextmanager

class AuthenticationService:
    def login(self, username: str, password: str) -> bool:
        return username == "admin" and password == "secret123"

class DatabaseConnection:
    def __init__(self):
        self._connected = False
    
    def connect(self):
        self._connected = True
    
    def disconnect(self):
        self._connected = False
    
    def execute_query(self, query: str) -> str:
        if not self._connected:
            raise RuntimeError("Not connected")
        return f"Results for: {query}"
    
    def close(self):
        self.disconnect()

class Logger:
    def __init__(self):
        self._lock = threading.Lock()
    
    def log(self, message: str):
        with self._lock:
            print(f"[LOG] {message}")

class ReportGenerator:
    def __init__(self, db: DatabaseConnection, logger: Logger):
        self._db = db
        self._logger = logger
    
    def generate_monthly_report(self) -> str:
        data = self._db.execute_query("SELECT * FROM sales WHERE month = CURRENT_DATE")
        self._logger.log("Monthly report generated")
        return f"Monthly Report: {data}"

class SystemOrchestrator:
    def __init__(self):
        self._auth = AuthenticationService()
        self._db = DatabaseConnection()
        self._logger = Logger()
        self._report_gen = ReportGenerator(self._db, self._logger)
    
    @contextmanager
    def session(self, username: str, password: str):
        if not self._auth.login(username, password):
            raise ValueError("Invalid credentials")
        
        self._db.connect()
        self._logger.log(f"User {username} logged in")
        
        try:
            yield self
        finally:
            self._db.close()
            self._logger.log("Session closed")
    
    def generate_report(self) -> str:
        return self._report_gen.generate_monthly_report()

if __name__ == "__main__":
    system = SystemOrchestrator()
    
    try:
        with system.session("admin", "secret123") as session:
            report = session.generate_report()
            print(report)
    except ValueError as e:
        print(f"Error: {e}")