class Data:
    def get(self): pass

class RealData(Data):
    def get(self):
        return "sensitive data"

class DataGuard(Data):
    def __init__(self, real):
        self._real = real
    
    def get(self):
        print("checking access")
        return self._real.get()

if __name__ == "__main__":
    guard = DataGuard(RealData())
    print(guard.get())