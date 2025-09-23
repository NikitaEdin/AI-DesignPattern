import copy
import threading
import uuid


class Cloneable:
    def __init__(self):
        self._allow_clone = True

    def clone(self, deep=True, overrides=None, allow_new_attributes=False, memo=None):
        if not getattr(self, "_allow_clone", True):
            raise RuntimeError("Cloning is disabled for this instance")
        if deep:
            new = copy.deepcopy(self, memo)
        else:
            new = copy.copy(self)
        if overrides:
            for k, v in overrides.items():
                if not allow_new_attributes and not hasattr(new, k):
                    raise AttributeError(f"Attribute '{k}' not found on cloned object")
                setattr(new, k, v)
        hook = getattr(new, "after_copy", None)
        if callable(hook):
            hook()
        return new


class TemplateRegistry:
    def __init__(self):
        self._templates = {}
        self._lock = threading.RLock()

    def register(self, key, template):
        with self._lock:
            if not isinstance(template, Cloneable):
                raise TypeError("Only Cloneable instances can be registered")
            self._templates[key] = template

    def unregister(self, key):
        with self._lock:
            self._templates.pop(key, None)

    def create(self, key, deep=True, overrides=None, allow_new_attributes=False):
        with self._lock:
            template = self._templates.get(key)
            if template is None:
                raise KeyError(f"No template registered under key '{key}'")
            return template.clone(deep=deep, overrides=overrides, allow_new_attributes=allow_new_attributes)


class Author(Cloneable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.uid = uuid.uuid4()

    def after_copy(self):
        self.uid = uuid.uuid4()


class Document(Cloneable):
    def __init__(self, title, paragraphs, author, metadata=None):
        super().__init__()
        self.title = title
        self.paragraphs = list(paragraphs)
        self.author = author
        self.metadata = dict(metadata or {})

    def after_copy(self):
        self.metadata = dict(self.metadata)
        self.metadata.setdefault("copied_at", None)


class Node(Cloneable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.next = None

    def __repr__(self):
        return f"<Node {self.name} at {hex(id(self))}>"


if __name__ == "__main__":
    registry = TemplateRegistry()

    author_template = Author("Alice")
    doc_template = Document(
        title="Draft",
        paragraphs=["Intro", "Body", "Conclusion"],
        author=author_template,
        metadata={"version": 1},
    )

    registry.register("author:v1", author_template)
    registry.register("doc:v1", doc_template)

    clone1 = registry.create("doc:v1", deep=True, overrides={"title": "Copy A"})
    clone2 = registry.create("doc:v1", deep=False, overrides={"title": "Copy B"})

    print("Original title:", doc_template.title)
    print("Clone1 title, author uid:", clone1.title, clone1.author.uid)
    print("Clone2 title, author uid:", clone2.title, clone2.author.uid)
    clone1.paragraphs.append("Appendix")
    print("Original paragraphs after clone1 modification (deep):", doc_template.paragraphs)
    print("Clone1 paragraphs:", clone1.paragraphs)
    clone2.paragraphs.append("Notes")
    print("Original paragraphs after clone2 modification (shallow):", doc_template.paragraphs)
    print("Clone2 paragraphs:", clone2.paragraphs)

    node = Node("root")
    node.next = node
    registry.register("node:self", node)
    node_clone = registry.create("node:self", deep=True)
    print("Original node:", node, "next points to self:", node.next is node)
    print("Cloned node:", node_clone, "next points to clone:", node_clone.next is node_clone)

    try:
        registry.create("doc:v1", deep=True, overrides={"nonexistent": 123})
    except AttributeError as e:
        print("Expected error on invalid override:", e)