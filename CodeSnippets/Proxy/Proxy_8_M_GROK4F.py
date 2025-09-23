from abc import ABC, abstractmethod
import time

class Document(ABC):
    @abstractmethod
    def display(self):
        pass

class RealDocument(Document):
    def __init__(self, filename):
        self._filename = filename
        self._content = None

    def display(self):
        if self._content is None:
            self._content = self._load_content()
        print(self._content)

    def _load_content(self):
        time.sleep(2)
        try:
            # Simulate file loading
            return f"Loaded content from {self._filename}"
        except Exception:
            raise IOError(f"Failed to load {self._filename}")

class AccessControlledDocument(Document):
    def __init__(self, filename, user_role):
        self._filename = filename
        self._user_role = user_role
        self._real_doc = None

    def display(self):
        if self._real_doc is None:
            if not self._is_authorized():
                raise PermissionError(f"Access denied for {self._user_role} to {self._filename}")
            self._real_doc = RealDocument(self._filename)
        self._real_doc.display()

    def _is_authorized(self):
        return self._user_role == "admin"

if __name__ == "__main__":
    # Demonstrate authorized access with lazy loading
    controlled_doc = AccessControlledDocument("document.txt", "admin")
    controlled_doc.display()
    controlled_doc.display()

    # Demonstrate unauthorized access
    try:
        unauthorized_doc = AccessControlledDocument("document.txt", "user")
        unauthorized_doc.display()
    except PermissionError as e:
        print(e)