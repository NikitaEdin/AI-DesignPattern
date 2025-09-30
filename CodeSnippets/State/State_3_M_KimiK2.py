class Locked:
    def toggle(self, door): door.context = Unlocked()

class Unlocked:
    def toggle(self, door): door.context = Locked()

class SecurityDoor:
    def __init__(self): self.context = Locked()
    def toggle(self): self.context.toggle(self)
    def __str__(s): return "Locked" if type(s.context) == Locked else "Unlocked"

if __name__ == "__main__":
    door = SecurityDoor()
    print(door, end="")
    for _ in range(3): door.toggle(); print(" ->", end=" " + str(door))