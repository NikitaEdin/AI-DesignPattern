class DataInterface:
    def request(self): pass

class RealData(DataInterface):
    def request(self):
        return "real data"

class StandInData(DataInterface):
    def __init__(self):
        self._subject = None
    def request(self):
        if self._subject is None:
            self._subject = RealData()
        return self._subject.request()

if __name__ == "__main__":
    s = StandInData()
    print(s.request())