class A:
    def run(self):
        return "A running"

class B:
    def start(self):
        return "B started"

class C:
    def launch(self):
        return "C launched"

class Manager:
    def __init__(self):
        self._a = A()
        self._b = B()
        self._c = C()
    def go(self):
        return ' | '.join([self._a.run(), self._b.start(), self._c.launch()])

if __name__ == "__main__":
    mgr = Manager()
    print(mgr.go())