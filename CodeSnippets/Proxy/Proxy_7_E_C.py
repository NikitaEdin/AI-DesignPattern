class Subject:
    def request(self):
        return "Real subject handling request"

class Representative:
    def __init__(self):
        self._subject = None
    
    def request(self):
        if self._subject is None:
            self._subject = Subject()
        return f"Representative: {self._subject.request()}"

if __name__ == "__main__":
    rep = Representative()
    print(rep.request())
    print(rep.request())