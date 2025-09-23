class Phase:
    def publish(self, post):
        pass

class DraftPhase(Phase):
    def publish(self, post):
        print("Document is being published.")
        post.current_phase = PublishedPhase()

class PublishedPhase(Phase):
    def publish(self, post):
        print("Document is already published.")

class Post:
    def __init__(self):
        self.current_phase = DraftPhase()

    def publish(self):
        self.current_phase.publish(self)

if __name__ == "__main__":
    doc = Post()
    doc.publish()
    doc.publish()