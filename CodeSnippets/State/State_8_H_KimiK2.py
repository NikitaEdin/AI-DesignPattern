class Device:
    def __init__(self):
        self._battery = 100
        self._current = Enabled()
        self._history = []
    
    def press(self):
        self._current.press(self)
    
    def tick(self):
        self._current.tick(self)
    
    def charge(self, amount):
        self._current.charge(self, amount)
    
    def set_behavior(self, behavior):
        self._history.append((type(self._current).__name__, self._battery))
        self._current = behavior
    
    def get_battery(self):
        return max(0, min(100, self._battery))
    
    def adjust_battery(self, delta):
        self._battery += delta
        self._battery = max(0, min(100, self._battery))
    
    def get_history(self):
        return self._history

class Behavior:
    def press(self, device): pass
    def tick(self, device): pass
    def charge(self, device, amount): pass

class Enabled(Behavior):
    def press(self, device):
        device.set_behavior(Active())
    
    def tick(self, device):
        device.adjust_battery(-2)
        if device.get_battery() <= 0:
            device.set_behavior(Depleted())
    
    def charge(self, device, amount):
        device.adjust_battery(amount)

class Active(Behavior):
    def __init__(self):
        self._timer = 0
    
    def press(self, device):
        device.set_behavior(Enabled())
    
    def tick(self, device):
        self._timer += 1
        device.adjust_battery(-5)
        if device.get_battery() <= 20 and self._timer > 3:
            device.set_behavior(PowerSave())
        elif device.get_battery() <= 0:
            device.set_behavior(Depleted())
    
    def charge(self, device, amount):
        device.adjust_battery(amount * 0.5)

class PowerSave(Behavior):
    def press(self, device):
        device.set_behavior(Enabled())
    
    def tick(self, device):
        device.adjust_battery(-1)
        if device.get_battery() <= 0:
            device.set_behavior(Depleted())
    
    def charge(self, device, amount):
        if device.get_battery() + amount > 20:
            device.set_behavior(Enabled())
        device.adjust_battery(amount)

class Depleted(Behavior):
    def press(self, device):
        if device.get_battery() > 5:
            device.set_behavior(Enabled())
    
    def tick(self, device):
        pass
    
    def charge(self, device, amount):
        device.adjust_battery(amount)
        if device.get_battery() > 5:
            device.set_behavior(Enabled())

if __name__ == "__main__":
    phone = Device()
    for _ in range(5):
        phone.tick()
    print(f"Battery: {phone.get_battery()}%")
    phone.press()
    for _ in range(3):
        phone.tick()
    phone.charge(50)
    print(f"Battery: {phone.get_battery()}%")
    print("History:", phone.get_history())