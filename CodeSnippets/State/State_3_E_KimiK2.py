class Light:
    def __init__(self):
        self.current = Off()
    
    def change(self):
        self.current.switch(self)

class Off:
    def switch(self, light):
        light.current = On()
        print("Light turned on")

class On:
    def switch(self, light):
        light.current = Off()
        print("Light turned off")

if __name__ == "__main__":
    lamp = Light()
    lamp.change()
    lamp.change()