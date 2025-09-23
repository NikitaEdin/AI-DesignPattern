class Task:
    def execute(self): raise NotImplementedError
class PrintTask(Task):
    def __init__(self, worker, msg): self.worker, self.msg = worker, msg
    def execute(self): self.worker.print_message(self.msg)
class Worker:
    def print_message(self, msg): print(f"Worker: {msg}")
class Manager:
    def __init__(self): self._q = []
    def add(self, task): self._q.append(task)
    def run(self):
        for t in self._q: t.execute()
        self._q.clear()
if __name__ == "__main__":
    w = Worker(); m = Manager()
    m.add(PrintTask(w, "Start")); m.add(PrintTask(w, "Process"))
    m.add(PrintTask(w, "Finish")); m.run()