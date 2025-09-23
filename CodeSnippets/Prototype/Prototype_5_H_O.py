import copy
import threading
import uuid

class Cloneable:
    def clone(self, *, deep: bool = True, **modifications):
        # create copy (shallow or deep)
        obj = copy.deepcopy(self) if deep else copy.copy(self)
        # apply ad-hoc modifications to the new instance
        for k, v in modifications.items():
            setattr(obj, k, v)
        # allow the clone to finalize any clone-specific initialization
        obj._post_clone(source=self, deep=deep)
        return obj

    def _post_clone(self, *, source, deep: bool):
        # default hook: subclasses may override to adjust clone based on source and depth
        pass

class SharedResource:
    def __init__(self, data):
        self.data = data

    def __deepcopy__(self, memo):
        # shared resources remain shared across clones
        return self

    def __repr__(self):
        return f"<SharedResource {self.data!r}>"

class Attachment:
    def __init__(self, name, owner=None, resource=None):
        self.name = name
        self.owner = owner
        self.resource = resource

    def __copy__(self):
        # shallow copy: keep same resource and owner reference
        return self.__class__(self.name, owner=self.owner, resource=self.resource)

    def __deepcopy__(self, memo):
        # deep copy: resource may be shared (its deepcopy can return self)
        res = copy.deepcopy(self.resource, memo)
        a = self.__class__(copy.deepcopy(self.name, memo), owner=None, resource=res)
        memo[id(self)] = a
        return a

    def __repr__(self):
        return f"<Attachment {self.name!r} owner_id={id(self.owner)}>"

class Document(Cloneable):
    def __init__(self, title, metadata=None):
        self.id = uuid.uuid4().hex
        self.version = 1
        self.title = title
        self.metadata = dict(metadata or {})
        self.attachments = []

    def add_attachment(self, attachment):
        attachment.owner = self
        self.attachments.append(attachment)

    def __copy__(self):
        cls = self.__class__
        new = cls.__new__(cls)
        new.id = uuid.uuid4().hex
        new.version = self.version
        new.title = self.title
        # shallow copy metadata (so clone can mutate without changing original dict)
        new.metadata = dict(self.metadata)
        # new container, same attachment objects (shared)
        new.attachments = list(self.attachments)
        return new

    def __deepcopy__(self, memo):
        cls = self.__class__
        new = cls.__new__(cls)
        memo[id(self)] = new
        new.id = uuid.uuid4().hex
        new.version = self.version + 1
        new.title = copy.deepcopy(self.title, memo)
        new.metadata = copy.deepcopy(self.metadata, memo)
        # deep-copy attachments; set their owner to the new document
        new.attachments = []
        for a in self.attachments:
            acopy = copy.deepcopy(a, memo)
            acopy.owner = new
            new.attachments.append(acopy)
        return new

    def _post_clone(self, *, source, deep: bool):
        # no mutation of the source; clone is already adjusted in __deepcopy__
        # ensure cloned metadata exists (already a copy in __copy__/__deepcopy__)
        if not deep:
            # keep shared attachments as-is; nothing to change
            pass

    def __repr__(self):
        return f"<Document {self.title!r} id={self.id} ver={self.version}>"

class TemplateRegistry:
    def __init__(self):
        self._lock = threading.RLock()
        self._store = {}

    def register(self, name, template):
        with self._lock:
            self._store[name] = template

    def unregister(self, name):
        with self._lock:
            self._store.pop(name, None)

    def create_from(self, name, *, deep=True, **mods):
        with self._lock:
            template = self._store.get(name)
            if template is None:
                raise KeyError(name)
            return template.clone(deep=deep, **mods)

if __name__ == "__main__":
    # setup
    shared = SharedResource({"common": 42})
    doc = Document("Report", metadata={"author": "Alice"})
    a1 = Attachment("fig1.png", resource=shared)
    a2 = Attachment("notes.txt", resource=None)
    doc.add_attachment(a1)
    doc.add_attachment(a2)

    registry = TemplateRegistry()
    registry.register("report_template", doc)

    # create a shallow clone: shares attachments and shared resources; metadata copied
    shallow = registry.create_from("report_template", deep=False)
    # create a deep clone: attachments deep-copied, shared resources remain shared
    deep = registry.create_from("report_template", deep=True)

    print("original:", doc)
    print(" shallow attachments owners:", [a.owner is doc for a in shallow.attachments])
    print(" deep attachments owners:", [a.owner is deep for a in deep.attachments])
    print("shared resource identity preserved:",
          deep.attachments[0].resource is shared and shallow.attachments[0].resource is shared)