# Your code here
class Target:
    def request(self):
        pass

class AdapterOne:
    def __init__(self, legacy_class_one):
        self.legacy_class_one = legacy_class_one
    
    def request(self):
        return self.legacy_class_one.request()

class AdapterTwo:
    def __init__(self, legacy_class_two):
        self.legacy_class_two = legacy_class_two
    
    def request(self):
        return self.legacy_class_two.request()

if __name__ == "__main__":
    legacy_class_one = LegacyClassOne()
    adapter_one = AdapterOne(legacy_class_one)
    adapter_one.request()

    legacy_class_two = LegacyClassTwo()
    adapter_two = AdapterTwo(legacy_class_two)
    adapter_two.request()