from abc import ABC, abstractmethod

class Mode(ABC):
    @abstractmethod
    def handle(self, context):
        pass

class StartMode(Mode):
    def handle(self, context):
        print("Starting...")
        context.mode = RunningMode()

class RunningMode(Mode):
    def handle(self, context):
        print("Running...")
        context.mode = EndMode()

class EndMode(Mode):
    def handle(self, context):
        print("Ending.")

class Processor:
    def __init__(self):
        self.mode = StartMode()
    def execute(self):
        self.mode.handle(self)

if __name__ == "__main__":
    proc = Processor()
    proc.execute()
    proc.execute()
    proc.execute()