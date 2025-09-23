class LightOnCommand(object):
    def __init__(self, light):
        self._light = light

    def execute(self):
        self._light.on()

class LightOffCommand(object):
    def __init__(self, light):
        self._light = light

    def execute(self):
        self._light.off()

class RemoteControl(object):
    def __init__(self):
        self._on_button = None
        self._off_button = None
        self._undo_button = None

    def set_on_button(self, button):
        self._on_button = button

    def set_off_button(self, button):
        self._off_button = button

    def set_undo_button(self, button):
        self._undo_button = button

    def on_button_pressed(self):
        self._on_button.execute()

    def off_button_pressed(self):
        self._off_button.execute()

    def undo_button_pressed(self):
        self._undo_button.undo()

class Light(object):
    def __init__(self, name):
        self._name = name
        self._on = False

    @property
    def on(self):
        return self._on

    def on(self):
        self._on = True

    def off(self):
        self._on = False

class GarageDoor(object):
    def __init__(self, name):
        self._name = name
        self._open = False

    @property
    def open(self):
        return self._open

    def open(self):
        self._open = True

    def close(self):
        self._open = False

class RemoteControlExample:
    def __init__(self):
        self._remote_control = None

    def create_remote_control(self):
        light1 = Light("Living Room")
        light2 = Light("Kitchen")
        garage_door = GarageDoor("Main House")

        on_light1_command = LightOnCommand(light1)
        off_light1_command = LightOffCommand(light1)
        open_garage_door_command = GarageDoorOpenCommand(garage_door)
        close_garage_door_command = GarageDoorCloseCommand(garage_door)

        self._remote_control = RemoteControl()
        self._remote_control.set_on_button(on_light1_command)
        self._remote_control.set_off_button(off_light1_command)
        self._remote_control.set_open_button(open_garage_door_command)
        self._remote_control.set_close_button(close_garage_door_command)

    def use_remote_control(self):
        self._remote_control.on_button_pressed()
        print("Living Room Light is on")
        self._remote_control.off_button_pressed()
        print("Living Room Light is off")
        self._remote_control.open_button_pressed()
        print("Main House Garage Door is open")
        self._remote_control.close_button_pressed()
        print("Main House Garage Door is closed")