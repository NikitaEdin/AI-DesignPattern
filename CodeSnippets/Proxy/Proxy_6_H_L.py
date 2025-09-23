python
class MyProxy:
    def __init__(self, real_object):
        self._real_object = real_object
    
    def __getattr__(self, name):
        return getattr(self._real_object, name)
    
    def __setattr__(self, name, value):
        setattr(self._real_object, name, value)

class MyRealObject:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw(self):
        print("Drawing at", (self.x, self.y))
    
my_real_object = MyRealObject()
my_proxy = MyProxy(my_real_object)

# Usage example within a main section
if __name__ == "__main__":
    my_real_object.draw()  # Output: Drawing at (0, 0)
    my_proxy.x = 10
    my_proxy.y = 20
    my_proxy.draw()  # Output: Drawing at (10, 20)