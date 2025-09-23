```python
class Light(object):
    def __init__(self):
        self.state = "off"

    def turn_on(self):
        if self.state == "off":
            self.state = "on"
            print("Light is on.")
        else:
            print("The light is already on.")

    def turn_off(self):
        if self.state == "on":
            self.state = "off"
            print("Light is off.")
        else:
            print("The light is already off.")

    def get_state(self):
        return self.state

# Usage example
if __name__ == '__main__':
    light = Light()
    light.turn_on()
    print(light.get_state())  # Output: "Light is on."
    light.turn_off()
    print(light.get_state())  # Output: "Light is off."
 ```