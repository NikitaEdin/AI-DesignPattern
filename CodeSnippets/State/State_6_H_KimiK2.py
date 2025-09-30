from abc import ABC, abstractmethod

class Profile(ABC):
    @abstractmethod
    def react(self, ctx): pass
    
    def __str__(self): return self.__class__.__name__

class Greenhorn(Profile):
    def react(self, ctx):
        ctx.earn(5)
        if ctx.cache > 20:
            ctx.switch(Explorer())

class Explorer(Profile):
    def react(self, ctx):
        ctx.earn(10)
        if ctx.cache > 100:
            ctx.switch(Veteran())
        elif ctx.cache < 10:
            ctx.switch(Greenhorn())

class Veteran(Profile):
    def react(self, ctx):
        ctx.earn(20)
        ctx.tax(5)
        if ctx.cache < 50:
            ctx.switch(Explorer())

class Session:
    def __init__(self):
        self.cache = 0
        self.profile = Greenhorn()
    
    def switch(self, new):
        self.profile = new
    
    def earn(self, amt):
        self.cache += amt
    
    def tax(self, amt):
        self.cache = max(0, self.cache - amt)
    
    def update(self):
        self.profile.react(self)
    
    def __str__(self):
        return f"{self.profile}({self.cache})"

if __name__ == "__main__":
    s = Session()
    for _ in range(20):
        print(s)
        s.update()