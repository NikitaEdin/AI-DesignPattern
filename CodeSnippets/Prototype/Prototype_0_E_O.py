import copy
class Item:
    def clone(self): return copy.deepcopy(self)
class Circle(Item):
    def __init__(self, r, c): self.r = r; self.c = c
    def __repr__(self): return f"Circle(r={self.r}, c='{self.c}')"
class Rect(Item):
    def __init__(self, w, h, c): self.w = w; self.h = h; self.c = c
    def __repr__(self): return f"Rect(w={self.w}, h={self.h}, c='{self.c}')"
class Registry:
    def __init__(self): self._d = {}
    def register(self, k, obj): self._d[k] = obj
    def create(self, k):
        o = self._d.get(k)
        if o is None: raise KeyError(k)
        return o.clone()
if __name__ == "__main__":
    r = Registry()
    r.register("red_circle", Circle(5, "red"))
    r.register("blue_rect", Rect(2, 3, "blue"))
    a = r.create("red_circle"); b = r.create("red_circle"); b.c = "green"
    c = r.create("blue_rect")
    print(a); print(b); print(c)