from abc import ABC, abstractmethod

class Mode(ABC):
    @abstractmethod
    def move(self):
        pass

class ModeA(Mode):
    def move(self):
        return "Moving in Mode A"

class ModeB(Mode):
    def move(self):
        return "Moving in Mode B"

class Person:
    def __init__(self):
        self._mode = ModeA()
    
    def change(self):
        self._mode = ModeB()
    
    def move(self):
        return self._mode.move()

if __name__ == "__main__":
    p = Person()
    print(p.move())
    p.change()
    print(p.move())