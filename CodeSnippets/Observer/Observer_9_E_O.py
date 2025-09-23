class Subject:
    def __init__(self): self._listeners=[]; self._state=None
    def add(self,l): self._listeners.append(l)
    def remove(self,l): self._listeners.remove(l)
    def set(self,s): self._state=s; self._notify()
    def _notify(self):
        for l in list(self._listeners): l.update(self._state)
class Listener:
    def update(self,state): raise NotImplementedError
class PrintListener(Listener):
    def __init__(self,name): self.name=name
    def update(self,state): print(f"{self.name} received: {state}")
if __name__=="__main__":
    s=Subject()
    a=PrintListener("A"); b=PrintListener("B")
    s.add(a); s.add(b)
    s.set(1)
    s.remove(a)
    s.set(2)