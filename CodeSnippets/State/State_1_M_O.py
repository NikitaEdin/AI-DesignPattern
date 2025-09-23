import abc, datetime

class ModeTransitionError(Exception): pass

class ModeBase(abc.ABC):
    def on_enter(self, ctrl): pass
    def on_exit(self, ctrl): pass
    @abc.abstractmethod
    def handle(self, ctrl, event): raise NotImplementedError

class IdleMode(ModeBase):
    def handle(self, ctrl, event):
        if event == 'start': ctrl.switch_mode(ActiveMode())
        else: raise ModeTransitionError(f"Idle cannot handle {event!r}")

class ActiveMode(ModeBase):
    def on_enter(self, ctrl): ctrl.last_active = datetime.datetime.utcnow()
    def handle(self, ctrl, event):
        if event == 'pause': ctrl.switch_mode(PausedMode())
        elif event == 'stop': ctrl.switch_mode(IdleMode())
        else: raise ModeTransitionError(f"Active cannot handle {event!r}")

class PausedMode(ModeBase):
    def handle(self, ctrl, event):
        if event == 'resume': ctrl.switch_mode(ActiveMode())
        elif event == 'stop': ctrl.switch_mode(IdleMode())
        else: raise ModeTransitionError(f"Paused cannot handle {event!r}")

class MachineController:
    def __init__(self, initial):
        self.history = []
        self.current = None
        self.last_active = None
        self.switch_mode(initial)

    def switch_mode(self, new):
        if new is None: raise ValueError("new mode required")
        if self.current and type(self.current) is type(new): raise ModeTransitionError("Already in that mode")
        if self.current: self.current.on_exit(self)
        try:
            new.on_enter(self)
            self.current = new
            self.history.append((new.__class__.__name__, datetime.datetime.utcnow()))
        except Exception as exc:
            raise ModeTransitionError("enter failed: " + str(exc))

    def handle(self, event):
        if not self.current: raise ModeTransitionError("No current mode")
        self.current.handle(self, event)

    def revert(self):
        if len(self.history) < 2: raise ModeTransitionError("No previous mode")
        self.history.pop()
        prev_name = self.history[-1][0]
        mapping = {'IdleMode': IdleMode, 'ActiveMode': ActiveMode, 'PausedMode': PausedMode}
        cls = mapping.get(prev_name)
        if not cls: raise ModeTransitionError("Unknown previous mode")
        self.switch_mode(cls())

if __name__ == '__main__':
    ctrl = MachineController(IdleMode())
    for ev in ['start', 'pause', 'resume', 'stop', 'stop']:
        try:
            ctrl.handle(ev)
            print('Event', ev, '->', ctrl.current.__class__.__name__)
        except Exception as e:
            print('Error processing', ev, ':', e)
    print('History:')
    for name, ts in ctrl.history:
        print('-', name, '@', ts.isoformat())
    try:
        ctrl.revert()
        print('Reverted to', ctrl.current.__class__.__name__)
    except Exception as e:
        print('Revert failed:', e)