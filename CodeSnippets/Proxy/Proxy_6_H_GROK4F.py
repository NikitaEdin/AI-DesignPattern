from abc import ABC, abstractmethod
import time

class MediaViewer(ABC):
    @abstractmethod
    def display(self, path: str) -> str:
        pass

class RealMediaViewer(MediaViewer):
    def __init__(self):
        self._loaded_content = {}

    def display(self, path: str) -> str:
        if path not in self._loaded_content:
            print(f"Simulating load for {path}...")
            time.sleep(2)
            self._loaded_content[path] = f"Content from {path}"
        return self._loaded_content[path]

class MediaAccessController(MediaViewer):
    def __init__(self, user_role: str = "guest"):
        self._user_role = user_role
        self._real_viewer = RealMediaViewer()
        self._cache = {}
        self._load_attempts = {}

    def display(self, path: str) -> str:
        if not self._is_authorized(path):
            raise PermissionError(f"Access denied for {path} under role {self._user_role}")
        
        if path not in self._cache:
            attempts = self._load_attempts.get(path, 0)
            if attempts >= 3:
                raise RuntimeError(f"Failed to load {path} after 3 attempts")
            
            try:
                self._cache[path] = self._real_viewer.display(path)
                self._load_attempts[path] = 0
            except Exception:
                self._load_attempts[path] = attempts + 1
                raise
        return self._cache[path]

    def _is_authorized(self, path: str) -> bool:
        restricted_paths = {"secret.jpg", "private.pdf"}
        if self._user_role == "admin":
            return True
        return path not in restricted_paths

if __name__ == "__main__":
    controller = MediaAccessController("user_role")
    print(controller.display("image.jpg"))
    print(controller.display("image.jpg"))
    
    admin_controller = MediaAccessController("admin")
    print(admin_controller.display("secret.jpg"))
    
    try:
        controller.display("secret.jpg")
    except PermissionError as e:
        print(e)