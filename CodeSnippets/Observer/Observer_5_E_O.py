class Subject:
    def __init__(self):
        self._subs=[]
        self._state=None
    def attach(self,s): self._subs.append(s)
    def detach(self,s): self._subs.remove(s)
    def set_state(self,state):
        self._state=state; self.notify_all()
    def notify_all(self):
        for s in list(self._subs): s.notify(self._state)
class Subscriber:
    def __init__(self,name): self.name=name
    def notify(self,state): print(f"{self.name} received: {state}")
if __name__=="__main__":
    s=Subject()
    a=Subscriber("A"); b=Subscriber("B")
    s.attach(a); s.attach(b)
    s.set_state("first")
    s.detach(a)
    s.set_state("second")