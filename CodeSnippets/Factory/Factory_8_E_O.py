class Product:
    def use(self):
        raise NotImplementedError

class Alpha(Product):
    def use(self):
        return "Alpha used"

class Beta(Product):
    def use(self):
        return "Beta used"

class Maker:
    def make(self, kind: str) -> Product:
        if kind == "alpha": return Alpha()
        if kind == "beta": return Beta()
        raise ValueError("Unknown kind")

def main():
    maker = Maker()
    for k in ("alpha", "beta"):
        p = maker.make(k)
        print(p.use())

if __name__ == "__main__":
    main()