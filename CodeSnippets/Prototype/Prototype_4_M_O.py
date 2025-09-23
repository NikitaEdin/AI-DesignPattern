import copy
import uuid

class Cloneable:
    def clone(self, deep=True):
        if not isinstance(deep, bool):
            raise TypeError("deep must be a boolean")
        new_obj = copy.deepcopy(self) if deep else copy.copy(self)
        if hasattr(new_obj, "reset_identity") and callable(new_obj.reset_identity):
            try:
                new_obj.reset_identity()
            except Exception as e:
                raise RuntimeError("failed to reset identity") from e
        return new_obj

class Document(Cloneable):
    def __init__(self, title, sections=None, metadata=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.sections = list(sections or [])
        self.metadata = dict(metadata or {})
    def reset_identity(self):
        self.id = str(uuid.uuid4())
    def add_section(self, content):
        self.sections.append(content)
    def __repr__(self):
        return f"<Document id={self.id} title={self.title!r} sections={self.sections!r} metadata={self.metadata!r}>"

class TemplateRegistry:
    def __init__(self):
        self._store = {}
    def register_template(self, name, template):
        if not hasattr(template, "clone"):
            raise TypeError("template must support cloning")
        self._store[name] = template
    def create_from_template(self, name, deep=True, **overrides):
        if name not in self._store:
            raise KeyError(f"template '{name}' not found")
        obj = self._store[name].clone(deep=deep)
        for attr, value in overrides.items():
            if not hasattr(obj, attr):
                raise AttributeError(f"attribute '{attr}' not found on cloned object")
            setattr(obj, attr, value)
        return obj

if __name__ == "__main__":
    registry = TemplateRegistry()
    base = Document("Monthly Report", sections=[{"heading":"Intro","points":[1,2]}], metadata={"author":"Alice"})
    registry.register_template("monthly", base)
    shallow_clone = registry.create_from_template("monthly", deep=False)
    deep_clone = registry.create_from_template("monthly", deep=True, title="Monthly Report (Copy)")
    shallow_clone.sections[0]["points"].append(3)
    deep_clone.sections[0]["points"].append(99)
    base.add_section({"heading":"Summary","points":[0]})
    print("Base:", base)
    print("Shallow Clone:", shallow_clone)
    print("Deep Clone:", deep_clone)