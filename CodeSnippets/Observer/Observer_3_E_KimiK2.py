class Publisher:
    def __init__(self):
        self._followers = []
    
    def attach(self, follower):
        self._followers.append(follower)
    
    def detach(self, follower):
        self._followers.remove(follower)
    
    def notify(self, message):
        for follower in self._followers:
            follower.update(message)

class Subscriber:
    def update(self, message):
        print(f"Received: {message}")

if __name__ == "__main__":
    pub = Publisher()
    f1 = Subscriber()
    f2 = Subscriber()
    pub.attach(f1)
    pub.attach(f2)
    pub.notify("Hello")