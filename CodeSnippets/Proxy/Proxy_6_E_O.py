class Subject:
    def request(self): raise NotImplementedError
class RealService(Subject):
    def __init__(self, data): self.data = data
    def request(self): return f"Real result: {self.data}"
class AccessController(Subject):
    def __init__(self, user, real=None):
        self.user = user; self._real = real
    def request(self):
        if self.user != "admin": return "Access denied"
        if self._real is None: self._real = RealService("sensitive")
        return self._real.request()
def main():
    admin = AccessController("admin")
    guest = AccessController("guest")
    print(admin.request())
    print(guest.request())
if __name__ == "__main__":
    main()