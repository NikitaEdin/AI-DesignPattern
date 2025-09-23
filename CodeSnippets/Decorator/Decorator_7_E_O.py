class Component:
    def operation(self):
        raise NotImplementedError
class BasicMessage(Component):
    def __init__(self, text):
        self.text = text
    def operation(self):
        return self.text
class WrapperBase(Component):
    def __init__(self, component):
        self.component = component
    def operation(self):
        return self.component.operation()
class Exclaim(WrapperBase):
    def operation(self):
        return self.component.operation() + "!"
class Upper(WrapperBase):
    def operation(self):
        return self.component.operation().upper()
if __name__ == "__main__":
    msg = BasicMessage("hello")
    wrapped = Exclaim(Upper(msg))
    print(msg.operation())
    print(wrapped.operation())