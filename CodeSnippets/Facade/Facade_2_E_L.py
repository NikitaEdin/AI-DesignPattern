```python
class Car(object):
    def __init__(self):
        self.color = "black"
        self.make = "Toyota"
        self.model = "Camry"

class GarageDoorOpener(object):
    def __init__(self, car):
        self.car = car

    def up(self):
        print("Garage door opener is moving up")

    def down(self):
        print("Garage door opener is moving down")

class RemoteControl(object):
    def __init__(self, garage_door_opener):
        self.garage_door_opener = garage_door_opener

    def press_button(self):
        self.garage_door_opener.up()

if __name__ == "__main__":
    car = Car()
    garage_door_opener = GarageDoorOpener(car)
    remote_control = RemoteControl(garage_door_opener)

    print("Opening garage door")
    remote_control.press_button()
  ```