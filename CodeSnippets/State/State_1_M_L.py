class TrafficLight:
    def __init__(self):
        self._state = "red"

    @property
    def state(self):
        return self._state

    def change_state(self):
        if self._state == "red":
            self._state = "green"
        else:
            self._state = "red"

if __name__ == "__main__":
    traffic_light = TrafficLight()

    print("Initial state:", traffic_light.state)

    for i in range(3):
        traffic_light.change_state()
        print("State after iteration {}:".format(i + 1), traffic_light.state)