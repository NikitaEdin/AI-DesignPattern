class Processor:
    def execute(self, data):
        raise NotImplementedError

class Upper(Processor):
    def execute(self, data):
        return data.upper()

class Reverse(Processor):
    def execute(self, data):
        return data[::-1]

class Worker:
    def __init__(self, processor):
        self.processor = processor
    def run(self, data):
        return self.processor.execute(data)

if __name__ == "__main__":
    w = Worker(Upper())
    print(w.run("hello"))
    w.processor = Reverse()
    print(w.run("hello"))