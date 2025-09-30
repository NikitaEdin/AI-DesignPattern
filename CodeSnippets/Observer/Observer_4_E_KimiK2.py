class Publisher:
    def __init__(self):
        self._followers = []
    
    def join(self, follower):
        self._followers.append(follower)
    
    def leave(self, follower):
        self._followers.remove(follower)
    
    def broadcast(self, data):
        for f in self._followers:
            f.receive(data)


class Listener:
    def __init__(self, name):
        self.name = name
    
    def receive(self, data):
        print(f"{self.name}: {data}")


if __name__ == "__main__":
    pub = Publisher()
    l1 = Listener("Alice")
    l2 = Listener("Bob")
    pub.join(l1)
    pub.join(l2)
    pub.broadcast("update")