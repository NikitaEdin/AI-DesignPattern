from abc import ABC, abstractmethod

class BaseHandler(ABC):
    @abstractmethod
    def on_entry(self, context):
        pass

    @abstractmethod
    def on_exit(self, context):
        pass

    @abstractmethod
    def request_review(self, context):
        pass

    @abstractmethod
    def publish(self, context):
        pass

    @abstractmethod
    def reject(self, context):
        pass

class DraftHandler(BaseHandler):
    def on_entry(self, context):
        context.status = "draft"

    def on_exit(self, context):
        pass

    def request_review(self, context):
        if context.is_ready_for_review():
            context.set_current_handler(ReviewHandler())
        else:
            raise ValueError("Document not ready for review")

    def publish(self, context):
        raise RuntimeError("Cannot publish from draft")

    def reject(self, context):
        raise RuntimeError("Cannot reject draft")

class ReviewHandler(BaseHandler):
    def on_entry(self, context):
        context.status = "under_review"

    def on_exit(self, context):
        pass

    def request_review(self, context):
        pass

    def publish(self, context):
        context.set_current_handler(PublishedHandler())

    def reject(self, context):
        context.set_current_handler(DraftHandler())

class PublishedHandler(BaseHandler):
    def on_entry(self, context):
        context.status = "published"

    def on_exit(self, context):
        pass

    def request_review(self, context):
        raise RuntimeError("Cannot request review for published document")

    def publish(self, context):
        pass

    def reject(self, context):
        raise RuntimeError("Cannot reject published document")

class DocumentProcessor:
    def __init__(self):
        self.title = ""
        self.content = ""
        self.status = "draft"
        self._current_handler = DraftHandler()

    def set_current_handler(self, handler):
        self._current_handler.on_exit(self)
        self._current_handler = handler
        handler.on_entry(self)

    def request_review(self):
        self._current_handler.request_review(self)

    def publish(self):
        self._current_handler.publish(self)

    def reject(self):
        self._current_handler.reject(self)

    def is_ready_for_review(self):
        return bool(self.title.strip() and self.content.strip())

if __name__ == "__main__":
    doc = DocumentProcessor()
    print(f"Initial status: {doc.status}")

    doc.title = "Test Document"
    doc.content = "Sample content"
    doc.request_review()
    print(f"After request review: {doc.status}")

    doc.reject()
    print(f"After reject: {doc.status}")

    doc.content += " - updated"
    doc.request_review()
    print(f"After second request review: {doc.status}")

    doc.publish()
    print(f"After publish: {doc.status}")

    try:
        doc.request_review()
        print("Unexpected success")
    except RuntimeError as e:
        print(f"Handled error: {e}")

    doc2 = DocumentProcessor()
    try:
        doc2.request_review()
        print("Unexpected success for empty doc")
    except ValueError as e:
        print(f"Handled empty doc error: {e}")