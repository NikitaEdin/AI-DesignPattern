from abc import ABC, abstractmethod

class DocumentViewer(ABC):
    @abstractmethod
    def get_content(self):
        pass

    @abstractmethod
    def get_metadata(self):
        pass

class FullDocumentViewer(DocumentViewer):
    def __init__(self, filename):
        self.filename = filename
        self._content = None
        self._metadata = None
        self._load()

    def _load(self):
        if self.filename == "invalid.txt":
            raise ValueError("Invalid file")
        self._content = f"Content of {self.filename}"
        self._metadata = {"size": 1024, "type": "txt"}

    def get_content(self):
        return self._content

    def get_metadata(self):
        return self._metadata

class SecureDocumentViewer(DocumentViewer):
    def __init__(self, filename, user_role):
        self.filename = filename
        self.user_role = user_role
        self._real_viewer = None
        self._content_cache = None
        self._metadata_cache = None

    def _load_real_viewer(self):
        if self._real_viewer is not None:
            return
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self._real_viewer = FullDocumentViewer(self.filename)
                self._content_cache = self._real_viewer.get_content()
                self._metadata_cache = self._real_viewer.get_metadata()
                break
            except ValueError:
                if attempt == max_retries - 1:
                    raise ValueError("Failed to load after retries")
                continue

    def _has_access(self, resource):
        if self.user_role == "admin":
            return True
        if resource == "metadata" and self.user_role == "user":
            return True
        return False

    def get_content(self):
        if not self._has_access("content"):
            raise PermissionError("Access denied to content")
        self._load_real_viewer()
        return self._content_cache

    def get_metadata(self):
        if not self._has_access("metadata"):
            raise PermissionError("Access denied to metadata")
        self._load_real_viewer()
        return self._metadata_cache

if __name__ == "__main__":
    # Test access denial for guest
    try:
        viewer = SecureDocumentViewer("doc.txt", "guest")
        viewer.get_metadata()
    except PermissionError as e:
        print(e)

    # Test user access to metadata
    viewer = SecureDocumentViewer("doc.txt", "user")
    print(viewer.get_metadata())
    try:
        viewer.get_content()
    except PermissionError as e:
        print(e)

    # Test admin access
    admin_viewer = SecureDocumentViewer("doc.txt", "admin")
    print(admin_viewer.get_content())
    print(admin_viewer.get_metadata())  # Should use cache, no reload

    # Test failure with retries
    try:
        fail_viewer = SecureDocumentViewer("invalid.txt", "admin")
        fail_viewer.get_content()
    except ValueError as e:
        print("Load failed:", e)