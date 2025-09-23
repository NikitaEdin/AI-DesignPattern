class Subject:
    def request(self): raise NotImplementedError
class RealService(Subject):
    def __init__(self): self._resource = "Expensive resource"
    def request(self): return f"RealService: using {self._resource}"
class Guard(Subject):
    def __init__(self): self._real = None; self._cache = None
    def request(self):
        if self._cache is not None: return f"Guard: cached -> {self._cache}"
        if self._real is None: self._real = RealService()
        self._cache = self._real.request()
        return f"Guard: fetched -> {self._cache}"
if __name__ == "__main__":
    g = Guard()
    print(g.request())
    print(g.request())