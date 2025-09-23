import copy
from abc import ABC, abstractmethod
from typing import Any, Dict


class CloneError(Exception):
    pass


class NotRegisteredError(CloneError):
    pass


class ValidationError(CloneError):
    pass


class BaseArtifact(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass

    def replicate(self, deep: bool = True, **overrides) -> "BaseArtifact":
        try:
            new_obj = copy.deepcopy(self) if deep else copy.copy(self)
        except Exception as e:
            raise CloneError(f"failed to copy: {e}") from e
        self._apply_overrides(new_obj, overrides)
        return new_obj

    @staticmethod
    def _apply_overrides(target: "BaseArtifact", overrides: Dict[str, Any]) -> None:
        for key, value in overrides.items():
            if not BaseArtifact._attribute_exists(target, key):
                raise ValidationError(f"attribute '{key}' does not exist on {type(target).__name__}")
            attr = getattr(type(target), key, None)
            if isinstance(attr, property) and attr.fset is None:
                raise ValidationError(f"attribute '{key}' is read-only")
            try:
                setattr(target, key, value)
            except Exception as e:
                raise ValidationError(f"could not set attribute '{key}': {e}") from e

    @staticmethod
    def _attribute_exists(target: "BaseArtifact", name: str) -> bool:
        if name in getattr(target, "__dict__", {}):
            return True
        if any(name == n for n in dir(type(target))):
            return True
        return False


class Document(BaseArtifact):
    def __init__(self, title: str, content: str, metadata: Dict[str, Any] = None):
        self.title = title
        self.content = content
        self.metadata = metadata if metadata is not None else {}

    def describe(self) -> str:
        return f"Document(title={self.title!r}, content_len={len(self.content)}, metadata_keys={list(self.metadata.keys())})"


class Image(BaseArtifact):
    def __init__(self, name: str, pixels: list):
        self.name = name
        self.pixels = pixels

    @property
    def size(self):
        return (len(self.pixels), len(self.pixels[0]) if self.pixels else 0)

    def describe(self) -> str:
        return f"Image(name={self.name!r}, size={self.size})"


class Registry:
    def __init__(self):
        self._store: Dict[str, BaseArtifact] = {}

    def register(self, key: str, obj: BaseArtifact, force: bool = False) -> None:
        if not force and key in self._store:
            raise CloneError(f"key '{key}' already registered")
        self._store[key] = obj

    def unregister(self, key: str) -> None:
        if key not in self._store:
            raise NotRegisteredError(f"key '{key}' not found")
        del self._store[key]

    def create(self, key: str, deep: bool = True, **overrides) -> BaseArtifact:
        if key not in self._store:
            raise NotRegisteredError(f"key '{key}' not found")
        prototype = self._store[key]
        return prototype.replicate(deep=deep, **overrides)


def main():
    registry = Registry()

    doc = Document("Report", "Initial content", metadata={"author": "Alice"})
    doc.metadata["self_ref"] = doc
    registry.register("annual_report", doc)

    doc_clone = registry.create("annual_report", deep=True, title="Annual Report 2025")
    doc_clone.metadata["author"] = "Bob"

    shallow_clone = registry.create("annual_report", deep=False, title="Shallow Copy")
    shallow_clone.metadata["author"] = "Carol"

    img = Image("logo", pixels=[[0, 1], [1, 0]])
    registry.register("logo_image", img)

    img_clone = registry.create("logo_image", deep=True, name="logo_v2")

    print("Original:", registry.create("annual_report", deep=True).describe())
    print("Deep Clone:", doc_clone.describe(), "author:", doc_clone.metadata["author"])
    print("Shallow Clone:", shallow_clone.describe(), "author:", shallow_clone.metadata["author"])
    print("Original author after clones:", registry.create("annual_report", deep=True).metadata["author"])
    print("Image original size:", img.describe())
    print("Image clone:", img_clone.describe())

    try:
        registry.create("unknown_key")
    except NotRegisteredError as e:
        print("Expected error:", e)

    try:
        registry.create("annual_report", title="New", non_existing_attr=123)
    except ValidationError as e:
        print("Expected validation error:", e)


if __name__ == "__main__":
    main()