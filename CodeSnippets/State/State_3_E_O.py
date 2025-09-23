class ModeBase:
    def handle(self, ctx):
        raise NotImplementedError
class IdleMode(ModeBase):
    def handle(self, ctx):
        print("Idle: preparing to run")
        ctx.set_mode(ActiveMode())
class ActiveMode(ModeBase):
    def handle(self, ctx):
        print("Active: working")
        ctx.set_mode(IdleMode())
class Device:
    def __init__(self, mode):
        self.mode = mode
    def set_mode(self, mode):
        self.mode = mode
    def request(self):
        self.mode.handle(self)
if __name__ == '__main__':
    d = Device(IdleMode())
    for _ in range(4):
        d.request()