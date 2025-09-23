class Document:
    def __init__(self, title="Untitled"):
        self.title = title
        self._current_mode = DraftMode(self)

    def request_review(self):
        try:
            self._current_mode.request_review()
        except Exception as e:
            print(f"Error in request_review: {e}")

    def publish(self):
        try:
            self._current_mode.publish()
        except Exception as e:
            print(f"Error in publish: {e}")

    def reject(self):
        try:
            self._current_mode.reject()
        except Exception as e:
            print(f"Error in reject: {e}")

    def set_mode(self, mode):
        self._current_mode = mode

    def display_status(self):
        print(f"Document '{self.title}' is in {type(self._current_mode).__name__} mode")


class Mode:
    def __init__(self, doc):
        self._doc = doc

    def request_review(self):
        raise NotImplementedError("Subclasses must implement this method")

    def publish(self):
        raise NotImplementedError("Subclasses must implement this method")

    def reject(self):
        raise NotImplementedError("Subclasses must implement this method")


class DraftMode(Mode):
    def request_review(self):
        print("Document sent for review.")
        self._doc.set_mode(ReviewMode(self._doc))

    def publish(self):
        print("Cannot publish a draft directly; review first.")

    def reject(self):
        print("Cannot reject a draft.")


class ReviewMode(Mode):
    def request_review(self):
        print("Document is already under review.")

    def publish(self):
        print("Document published after review.")
        self._doc.set_mode(PublishedMode(self._doc))

    def reject(self):
        print("Review rejected; back to draft.")
        self._doc.set_mode(DraftMode(self._doc))


class PublishedMode(Mode):
    def request_review(self):
        print("Published document cannot be sent for review.")

    def publish(self):
        print("Document is already published.")

    def reject(self):
        print("Cannot reject a published document.")


if __name__ == "__main__":
    doc = Document("Sample Report")
    doc.display_status()
    doc.request_review()
    doc.display_status()
    doc.publish()
    doc.display_status()
    doc.reject()
    doc.display_status()