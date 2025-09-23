import abc

class Executable(abc.ABC):
    @abc.abstractmethod
    def perform(self):
        pass

    @abc.abstractmethod
    def reverse(self):
        pass

class Light:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        print("Light turned on")

    def turn_off(self):
        self.is_on = False
        print("Light turned off")

class Stereo:
    def __init__(self):
        self.is_on = False
        self.volume = 0

    def turn_on(self):
        self.is_on = True
        print("Stereo turned on")

    def turn_off(self):
        self.is_on = False
        print("Stereo turned off")

    def set_volume(self, volume):
        if 0 <= volume <= 10:
            self.volume = volume
            print(f"Volume set to {volume}")
        else:
            raise ValueError("Volume must be between 0 and 10")

class LightOn(Executable):
    def __init__(self, light):
        self.light = light
        self.was_on = light.is_on

    def perform(self):
        self.light.turn_on()

    def reverse(self):
        if self.was_on:
            self.light.turn_on()
        else:
            self.light.turn_off()

class LightOff(Executable):
    def __init__(self, light):
        self.light = light
        self.was_on = light.is_on

    def perform(self):
        self.light.turn_off()

    def reverse(self):
        if self.was_on:
            self.light.turn_on()
        else:
            self.light.turn_off()

class StereoOn(Executable):
    def __init__(self, stereo):
        self.stereo = stereo
        self.was_on = stereo.is_on

    def perform(self):
        self.stereo.turn_on()

    def reverse(self):
        if self.was_on:
            self.stereo.turn_on()
        else:
            self.stereo.turn_off()

class StereoVolume(Executable):
    def __init__(self, stereo, volume):
        self.stereo = stereo
        self.volume = volume
        self.previous_volume = stereo.volume

    def perform(self):
        self.stereo.set_volume(self.volume)

    def reverse(self):
        self.stereo.set_volume(self.previous_volume)

class Sequence(Executable):
    def __init__(self, actions):
        self.actions = actions or []
        self.previous_states = []

    def perform(self):
        if not self.actions:
            print("No actions to perform")
            return
        for action in self.actions:
            try:
                action.perform()
                self.previous_states.append(action)
            except Exception as e:
                print(f"Failed to perform action: {e}")
                for prev in reversed(self.previous_states):
                    try:
                        prev.reverse()
                    except Exception:
                        pass
                self.previous_states.clear()
                raise

    def reverse(self):
        for action in reversed(self.previous_states):
            try:
                action.reverse()
            except Exception:
                pass
        self.previous_states.clear()

class Remote:
    def __init__(self):
        self.current_action = None
        self.history = []

    def assign_action(self, action):
        if action is None:
            raise ValueError("Action cannot be None")
        self.current_action = action

    def execute(self):
        if self.current_action is None:
            print("No action assigned")
            return
        try:
            self.current_action.perform()
            self.history.append(self.current_action)
        except Exception as e:
            print(f"Execution failed: {e}")

    def revert_last(self):
        if not self.history:
            print("No actions to revert")
            return
        last_action = self.history.pop()
        try:
            last_action.reverse()
        except Exception as e:
            print(f"Revert failed: {e}")
            self.history.append(last_action)

if __name__ == "__main__":
    light = Light()
    stereo = Stereo()

    light_on = LightOn(light)
    light_off = LightOff(light)
    stereo_on = StereoOn(stereo)
    volume_up = StereoVolume(stereo, 5)

    simple_sequence = Sequence([light_on, stereo_on])
    complex_sequence = Sequence([light_on, volume_up, light_off])

    remote = Remote()

    remote.assign_action(light_on)
    remote.execute()
    remote.revert_last()

    remote.assign_action(simple_sequence)
    remote.execute()

    remote.assign_action(volume_up)
    remote.execute()
    remote.revert_last()

    remote.assign_action(complex_sequence)
    remote.execute()
    remote.revert_last()

    empty_sequence = Sequence([])
    remote.assign_action(empty_sequence)
    remote.execute()