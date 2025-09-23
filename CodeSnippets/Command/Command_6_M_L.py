class RemoteControl:
    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def press_button(self, index):
        self.buttons[index].press()

class Button:
    def __init__(self, label):
        self.label = label

    def press(self):
        print(f"Button {self.label} pressed")

if __name__ == "__main__":
    remote_control = RemoteControl()

    # Create some buttons
    button1 = Button("Channel Up")
    button2 = Button("Channel Down")
    button3 = Button("Volume Up")
    button4 = Button("Volume Down")

    # Add the buttons to the remote control
    remote_control.add_button(button1)
    remote_control.add_button(button2)
    remote_control.add_button(button3)
    remote_control.add_button(button4)

    # Press some buttons using their index
    remote_control.press_button(0)
    remote_control.press_button(1)
    remote_control.press_button(2)
    remote_control.press_button(3)