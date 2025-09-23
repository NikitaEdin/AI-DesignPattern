class Prototype:
    def __init__(self, name):
        self.name = name

    def clone(self):
        return Prototype(self.name)

def main():
    prototype1 = Prototype("prototype1")
    prototype2 = prototype1.clone()

    print(f"prototype1: {prototype1.name}")
    print(f"prototype2: {prototype2.name}")

if __name__ == "__main__":
    main()