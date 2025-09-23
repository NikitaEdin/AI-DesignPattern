class BaseMode:
    def __init__(self, name: str):
        self.name = name

    def on_enter(self, controller):
        raise NotImplementedError

    def on_exit(self, controller):
        raise NotImplementedError

    def handle_timer(self, controller):
        raise NotImplementedError


class RedMode(BaseMode):
    def __init__(self):
        super().__init__("RED")

    def on_enter(self, controller):
        print("Entering RED")

    def on_exit(self, controller):
        print("Exiting RED")

    def handle_timer(self, controller):
        controller.set_mode(GreenMode())


class GreenMode(BaseMode):
    def __init__(self):
        super().__init__("GREEN")

    def on_enter(self, controller):
        print("Entering GREEN")

    def on_exit(self, controller):
        print("Exiting GREEN")

    def handle_timer(self, controller):
        controller.set_mode(YellowMode())


class YellowMode(BaseMode):
    def __init__(self):
        super().__init__("YELLOW")

    def on_enter(self, controller):
        print("Entering YELLOW")

    def on_exit(self, controller):
        print("Exiting YELLOW")

    def handle_timer(self, controller):
        controller.set_mode(RedMode())


class TrafficLightController:
    def __init__(self, initial_mode: BaseMode | None = None):
        self.current_mode: BaseMode | None = None
        self.history: list[BaseMode] = []
        if initial_mode:
            self.set_mode(initial_mode)

    def set_mode(self, new_mode: BaseMode):
        if not isinstance(new_mode, BaseMode):
            raise TypeError("Expected a mode object")
        if self.current_mode is new_mode:
            print(f"Already in {new_mode.name}")
            return
        if self.current_mode:
            try:
                self.current_mode.on_exit(self)
            except Exception as e:
                print(f"Error during exit: {e}")
            self.history.append(self.current_mode)
        self.current_mode = new_mode
        try:
            self.current_mode.on_enter(self)
        except Exception as e:
            print(f"Error during enter: {e}")

    def revert_mode(self):
        if not self.history:
            raise ValueError("No previous mode to revert to")
        try:
            if self.current_mode:
                self.current_mode.on_exit(self)
        except Exception as e:
            print(f"Error during exit: {e}")
        self.current_mode = self.history.pop()
        try:
            self.current_mode.on_enter(self)
        except Exception as e:
            print(f"Error during enter: {e}")

    def perform_tick(self):
        if not self.current_mode:
            raise RuntimeError("No current mode set")
        try:
            self.current_mode.handle_timer(self)
        except Exception as e:
            print(f"Error handling timer: {e}")


if __name__ == "__main__":
    controller = TrafficLightController(RedMode())
    for _ in range(6):
        controller.perform_tick()
    try:
        controller.revert_mode()
        controller.revert_mode()
    except Exception as exc:
        print(f"Revert failed: {exc}")