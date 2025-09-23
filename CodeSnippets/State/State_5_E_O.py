class Mode:
    def handle(self, device, event): raise NotImplementedError
class Locked(Mode):
    def handle(self, device, event):
        if event == 'coin': print('Unlocked'); device.set_mode(Unlocked())
        elif event == 'push': print('Alarm')
class Unlocked(Mode):
    def handle(self, device, event):
        if event == 'push': print('Locked'); device.set_mode(Locked())
        elif event == 'coin': print('Thanks')
class Machine:
    def __init__(self, initial): self.current = initial
    def set_mode(self, new): self.current = new
    def on_event(self, event): self.current.handle(self, event)
if __name__ == '__main__':
    m = Machine(Locked())
    m.on_event('push'); m.on_event('coin'); m.on_event('coin'); m.on_event('push')