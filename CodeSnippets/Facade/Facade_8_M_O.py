class Lighting:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False


class Climate:
    def __init__(self, initial_temp: float = 21.0):
        self.temperature = initial_temp

    def set_temperature(self, temp: float):
        if not (10.0 <= temp <= 30.0):
            raise ValueError(f"Temperature {temp} out of range (10-30°C)")
        self.temperature = temp


class Security:
    def __init__(self):
        self.armed = False

    def arm(self):
        self.armed = True

    def disarm(self):
        self.armed = False


class HomeController:
    def __init__(self, lighting: Lighting, climate: Climate, security: Security):
        self.lighting = lighting
        self.climate = climate
        self.security = security
        self.presets = {}

    def leave_home(self):
        try:
            self.lighting.turn_off()
            self.climate.set_temperature(16.0)
            self.security.arm()
        except Exception as exc:
            raise RuntimeError(f"Failed to execute leave sequence: {exc}") from exc

    def arrive_home(self):
        try:
            self.security.disarm()
            self.climate.set_temperature(21.0)
            self.lighting.turn_on()
        except Exception as exc:
            raise RuntimeError(f"Failed to execute arrive sequence: {exc}") from exc

    def set_preset(self, name: str, config: dict):
        allowed_keys = {"lights", "temp", "secure"}
        if not isinstance(config, dict) or not set(config.keys()).issubset(allowed_keys):
            raise ValueError("Preset config must be a dict with keys: lights, temp, secure")
        self.presets[name] = config.copy()

    def apply_preset(self, name: str):
        if name not in self.presets:
            raise KeyError(f"Preset '{name}' not found")
        cfg = self.presets[name]
        if "lights" in cfg:
            if cfg["lights"]:
                self.lighting.turn_on()
            else:
                self.lighting.turn_off()
        if "temp" in cfg:
            self.climate.set_temperature(float(cfg["temp"]))
        if "secure" in cfg:
            if cfg["secure"]:
                self.security.arm()
            else:
                self.security.disarm()

    def run_system_check(self):
        state = {
            "lights_on": self.lighting.is_on,
            "temperature": self.climate.temperature,
            "security_armed": self.security.armed,
        }
        if state["security_armed"] and state["lights_on"]:
            raise RuntimeError("Security is armed while lights are on")
        return state


if __name__ == "__main__":
    lighting = Lighting()
    climate = Climate()
    security = Security()
    controller = HomeController(lighting, climate, security)

    controller.set_preset("evening", {"lights": True, "temp": 20, "secure": False})
    controller.set_preset("away", {"lights": False, "temp": 16, "secure": True})

    try:
        controller.apply_preset("evening")
        print("Evening preset applied:", controller.run_system_check())
        controller.apply_preset("away")
        print("Away preset applied:", controller.run_system_check())
        controller.apply_preset("nonexistent")
    except Exception as e:
        print("Error:", e)