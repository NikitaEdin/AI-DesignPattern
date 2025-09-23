from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def draw(self):
        pass

class WindowsButton(Button):
    def draw(self):
        print("Drawing a Windows-style button")

class MacButton(Button):
    def draw(self):
        print("Drawing a Mac-style button")

class WindowManager(ABC):
    @abstractmethod
    def create_button(self):
        pass

    def render_dialog(self):
        try:
            button = self.create_button()
            button.draw()
        except Exception as e:
            print(f"Error rendering dialog: {e}")

class WindowsWindowManager(WindowManager):
    def create_button(self):
        return WindowsButton()

class MacWindowManager(WindowManager):
    def create_button(self):
        return MacButton()

if __name__ == "__main__":
    manager = WindowsWindowManager()
    manager.render_dialog()

    manager = MacWindowManager()
    manager.render_dialog()