import copy
class Widget:
    def __init__(self,name,config):
        self.name=name
        self.config=config
    def duplicate(self):
        return copy.deepcopy(self)
class Registry:
    def __init__(self):
        self._items={}
    def register(self,key,item):
        self._items[key]=item
    def create(self,key):
        item=self._items.get(key)
        return item.duplicate() if item else None
if __name__=="__main__":
    r=Registry()
    original=Widget("Button",{"color":"red","size":(100,50)})
    r.register("red_button",original)
    copy1=r.create("red_button")
    copy1.config["color"]="blue"
    print(original.name,original.config)
    print(copy1.name,copy1.config)