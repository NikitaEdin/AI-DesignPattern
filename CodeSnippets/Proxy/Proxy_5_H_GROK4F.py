from abc import ABC, abstractmethod
import time

class Viewer(ABC):
    @abstractmethod
    def show(self) -> str:
        pass

class FullViewer(Viewer):
    def __init__(self, filename: str):
        self.filename = filename
        self.content = None
        self._load_content()

    def _load_content(self):
        try:
            print(f"Performing heavy load for {self.filename}...")
            time.sleep(3)
            self.content = f"Detailed content loaded from {self.filename} at {time.time()}"
        except Exception:
            self.content = f"Failed to load {self.filename}"

    def show(self) -> str:
        if self.content is None:
            self._load_content()
        return self.content

class GuardedViewer(Viewer):
    def __init__(self, filename: str, user_role: str):
        self.filename = filename
        self.user_role = user_role
        self._full_viewer = None
        self._cached_content = None
        self._last_access = None

    def _check_authorization(self) -> bool:
        authorized_roles = {"admin", "editor"}
        return self.user_role in authorized_roles

    def show(self) -> str:
        current_time = time.time()
        self._last_access = current_time

        if not self._check_authorization():
            return f"Access denied for role: {self.user_role}"

        if self._cached_content is None:
            if self._full_viewer is None:
                self._full_viewer = FullViewer(self.filename)
            self._cached_content = self._full_viewer.show()

        return self._cached_content

if __name__ == "__main__":
    print("Demonstrating first access (lazy load):")
    viewer1 = GuardedViewer("confidential_report.pdf", "admin")
    result1 = viewer1.show()
    print(result1[:50] + "..." if len(result1) > 50 else result1)
    print()

    print("Second access (cached):")
    result2 = viewer1.show()
    print(result2[:50] + "..." if len(result2) > 50 else result2)
    print()

    print("Unauthorized access:")
    viewer2 = GuardedViewer("confidential_report.pdf", "guest")
    result3 = viewer2.show()
    print(result3)
    print()

    print("Edge case - another admin access:")
    viewer3 = GuardedViewer("another_file.docx", "admin")
    result4 = viewer3.show()
    print(result4[:50] + "..." if len(result4) > 50 else result4)