import copy
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict


class Duplicable(ABC):
    @abstractmethod
    def duplicate(self, deep: bool = True, overrides: Dict[str, Any] = None):
        pass


class TemplateRegistry:
    def __init__(self):
        self._store: Dict[str, Duplicable] = {}

    def register(self, key: str, template: Duplicable):
        if not isinstance(template, Duplicable):
            raise TypeError("Only duplicable objects can be registered")
        self._store[key] = template

    def unregister(self, key: str):
        self._store.pop(key, None)

    def create(self, key: str, deep: bool = True, overrides: Dict[str, Any] = None):
        template = self._store.get(key)
        if template is None:
            raise KeyError(f"No template registered under key: {key}")
        return template.duplicate(deep=deep, overrides=overrides or {})


class Document(Duplicable):
    def __init__(self, title: str, content: list, metadata: dict):
        self.id = uuid.uuid4().hex
        self.title = title
        self.content = content  # list of paragraphs (mutable)
        self.metadata = metadata  # dict (mutable)

    def duplicate(self, deep: bool = True, overrides: Dict[str, Any] = None):
        if deep:
            new_obj = copy.deepcopy(self)
        else:
            new_obj = copy.copy(self)
            # shallow copy mutable containers to avoid accidental shared state
            new_obj.content = list(self.content)
            new_obj.metadata = dict(self.metadata)
        new_obj.id = uuid.uuid4().hex
        overrides = overrides or {}
        for k, v in overrides.items():
            if not hasattr(new_obj, k):
                raise AttributeError(f"{self.__class__.__name__} has no attribute '{k}'")
            setattr(new_obj, k, v)
        new_obj._post_duplicate(original=self)
        return new_obj

    def _post_duplicate(self, original):
        if 'version' in original.metadata:
            self.metadata['copied_from_version'] = original.metadata.get('version')


class ImageAsset(Duplicable):
    def __init__(self, name: str, pixels: bytes, tags: list):
        self.id = uuid.uuid4().hex
        self.name = name
        self.pixels = pixels  # immutable bytes
        self.tags = tags  # mutable list

    def duplicate(self, deep: bool = True, overrides: Dict[str, Any] = None):
        if deep:
            new_obj = copy.deepcopy(self)
        else:
            new_obj = copy.copy(self)
            new_obj.tags = list(self.tags)
        new_obj.id = uuid.uuid4().hex
        overrides = overrides or {}
        for k, v in overrides.items():
            if not hasattr(new_obj, k):
                raise AttributeError(f"{self.__class__.__name__} has no attribute '{k}'")
            setattr(new_obj, k, v)
        new_obj._post_duplicate(original=self)
        return new_obj

    def _post_duplicate(self, original):
        if self.pixels == original.pixels:
            self.tags.append('shared-pixels')


if __name__ == "__main__":
    registry = TemplateRegistry()

    doc_template = Document(
        title="Annual Report",
        content=["Intro", "Financials", "Summary"],
        metadata={"version": 3, "author": "Alice"}
    )
    img_template = ImageAsset(
        name="Logo",
        pixels=b"\x89PNG\r\n\x1a\n",
        tags=["brand", "vector"]
    )

    registry.register("report", doc_template)
    registry.register("logo", img_template)

    report_copy_shallow = registry.create("report", deep=False, overrides={"title": "Annual Report (Draft)"})
    report_copy_shallow.content.append("Appendix")
    report_copy_shallow.metadata["reviewed"] = False

    report_copy_deep = registry.create("report", deep=True, overrides={"title": "Annual Report (Final)"})
    report_copy_deep.content.append("Final Notes")
    report_copy_deep.metadata["reviewed"] = True

    logo_shared = registry.create("logo", deep=False)
    logo_deep = registry.create("logo", deep=True, overrides={"name": "Logo v2"})

    print("Original doc id:", doc_template.id, "title:", doc_template.title, "content:", doc_template.content, "metadata:", doc_template.metadata)
    print("Shallow copy id:", report_copy_shallow.id, "title:", report_copy_shallow.title, "content:", report_copy_shallow.content, "metadata:", report_copy_shallow.metadata)
    print("Deep copy id:", report_copy_deep.id, "title:", report_copy_deep.title, "content:", report_copy_deep.content, "metadata:", report_copy_deep.metadata)

    print("Original img id:", img_template.id, "name:", img_template.name, "tags:", img_template.tags)
    print("Shallow logo id:", logo_shared.id, "name:", logo_shared.name, "tags:", logo_shared.tags)
    print("Deep logo id:", logo_deep.id, "name:", logo_deep.name, "tags:", logo_deep.tags)