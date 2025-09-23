```python
class Director:
    def __init__(self, builder):
        self.builder = builder

    def construct(self):
        self.builder.build_preparation()
        self.builder.build_frame()
        self.builder.build_roof()
        self.builder.build_windows()
        return self.builder.get_result()

class HouseBuilder:
    def __init__(self):
        self.parts = []

    def build_preparation(self):
        print("Building preparation.")

    def build_frame(self):
        print("Building frame.")
        self.parts.append("frame")

    def build_roof(self):
        print("Building roof.")
        self.parts.append("roof")

    def build_windows(self):
        print("Building windows.")
        self.parts.append("windows")

    def get_result(self):
        return self.parts

def main():
    house = HouseBuilder()
    director = Director(house)
    result = director.construct()
    print(f"House built with {len(result)} parts: {', '.join(result)}")

if __name__ == "__main__":
    main()
  ```