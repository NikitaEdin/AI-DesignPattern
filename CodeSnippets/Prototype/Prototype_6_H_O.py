import copy
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class CloneBase(ABC):
    def __init__(self):
        self._instance_id = uuid.uuid4()

    @abstractmethod
    def clone(self, deep: bool = True) -> "CloneBase":
        pass

    def clone_with_overrides(self, deep: bool = True, **overrides) -> "CloneBase":
        cloned = self.clone(deep=deep)
        for k, v in overrides.items():
            setattr(cloned, k, v)
        cloned._instance_id = uuid.uuid4()
        return cloned

    def identity(self) -> uuid.UUID:
        return self._instance_id


class TemplateRegistry:
    def __init__(self):
        self._store: Dict[str, CloneBase] = {}

    def register(self, key: str, template: CloneBase, *, overwrite: bool = False) -> None:
        if key in self._store and not overwrite:
            raise KeyError(f"Key '{key}' already registered")
        self._store[key] = template

    def unregister(self, key: str) -> None:
        if key not in self._store:
            raise KeyError(f"Key '{key}' not found")
        del self._store[key]

    def create(self, key: str, deep: bool = True, **overrides) -> CloneBase:
        if key not in self._store:
            raise KeyError(f"Key '{key}' not found")
        template = self._store[key]
        return template.clone_with_overrides(deep=deep, **overrides)


class Asset(CloneBase):
    def __init__(self, name: str, data: Any):
        super().__init__()
        self.name = name
        self.data = data

    def __deepcopy__(self, memo):
        copied = Asset(self.name, copy.deepcopy(self.data, memo))
        copied._instance_id = uuid.uuid4()
        memo[id(self)] = copied
        return copied

    def clone(self, deep: bool = True) -> "Asset":
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    def __repr__(self):
        return f"<Asset name={self.name!r} id={self._instance_id}>"


class Document(CloneBase):
    def __init__(self, title: str, body: str, assets: Optional[list] = None, metadata: Optional[dict] = None):
        super().__init__()
        self.title = title
        self.body = body
        self.assets = list(assets) if assets else []
        self.metadata = dict(metadata) if metadata else {}

    def __deepcopy__(self, memo):
        copied_assets = [asset.clone(deep=True) if isinstance(asset, CloneBase) else copy.deepcopy(asset, memo) for asset in self.assets]
        copied = Document(copy.deepcopy(self.title, memo), copy.deepcopy(self.body, memo), copied_assets, copy.deepcopy(self.metadata, memo))
        copied._instance_id = uuid.uuid4()
        memo[id(self)] = copied
        return copied

    def clone(self, deep: bool = True) -> "Document":
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    def add_asset(self, asset: Asset) -> None:
        self.assets.append(asset)

    def __repr__(self):
        asset_ids = [str(a.identity()) if isinstance(a, CloneBase) else repr(a) for a in self.assets]
        return f"<Document title={self.title!r} id={self._instance_id} assets={asset_ids} metadata={self.metadata!r}>"


if __name__ == "__main__":
    registry = TemplateRegistry()

    logo = Asset("logo.png", b"\x89PNG...")
    manual = Document("User Manual", "Initial content", assets=[logo], metadata={"version": 1})

    registry.register("manual_v1", manual)

    clone_shallow = registry.create("manual_v1", deep=False)
    clone_deep = registry.create("manual_v1", deep=True, title="User Manual - Copy")

    print("Original:", manual)
    print("Shallow clone:", clone_shallow)
    print("Deep clone:", clone_deep)

    clone_shallow.body = "Modified in shallow"
    clone_shallow.assets[0].name = "logo_renamed.png"

    clone_deep.body = "Modified in deep"
    clone_deep.assets[0].name = "logo_copied.png"

    print("\nAfter modifications:")
    print("Original:", manual)
    print("Shallow clone:", clone_shallow)
    print("Deep clone:", clone_deep)

    try:
        registry.register("manual_v1", manual)
    except KeyError as e:
        print("\nExpected error when re-registering without overwrite:", e)

    registry.register("manual_v1", manual, overwrite=True)
    new_clone = registry.create("manual_v1", deep=True, metadata={"version": 2})
    print("\nNew clone with overridden metadata:", new_clone)