import logging

logging.basicConfig(level=logging.INFO)

class LightSystem:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        try:
            self.is_on = True
            logging.info("Lights turned on")
        except Exception as e:
            logging.error(f"Failed to turn on lights: {e}")

    def turn_off(self):
        try:
            self.is_on = False
            logging.info("Lights turned off")
        except Exception as e:
            logging.error(f"Failed to turn off lights: {e}")

class Thermostat:
    def __init__(self, default_temp=72):
        self.temperature = default_temp
        self.is_active = False

    def set_temperature(self, temp):
        try:
            if not 50 <= temp <= 90:
                raise ValueError("Temperature out of valid range")
            self.temperature = temp
            logging.info(f"Temperature set to {temp}°F")
        except ValueError as e:
            logging.error(f"Invalid temperature: {e}")
        except Exception as e:
            logging.error(f"Failed to set temperature: {e}")

    def activate(self):
        try:
            self.is_active = True
            logging.info("Thermostat activated")
        except Exception as e:
            logging.error(f"Failed to activate thermostat: {e}")

class SecuritySystem:
    def __init__(self):
        self.is_armed = False

    def arm(self):
        try:
            self.is_armed = True
            logging.info("Security system armed")
        except Exception as e:
            logging.error(f"Failed to arm security: {e}")

    def disarm(self):
        try:
            self.is_armed = False
            logging.info("Security system disarmed")
        except Exception as e:
            logging.error(f"Failed to disarm security: {e}")

class HomeController:
    def __init__(self, light_system=None, thermostat=None, security_system=None):
        self.light_system = light_system or LightSystem()
        self.thermostat = thermostat or Thermostat()
        self.security_system = security_system or SecuritySystem()
        self.config = {"morning_temp": 72, "night_temp": 68}

    def initialize_morning_routine(self):
        try:
            self.security_system.disarm()
            self.thermostat.activate()
            self.thermostat.set_temperature(self.config["morning_temp"])
            self.light_system.turn_on()
            logging.info("Morning routine completed successfully")
        except Exception as e:
            logging.error(f"Morning routine failed: {e}")

    def initialize_night_routine(self):
        try:
            self.light_system.turn_off()
            self.thermostat.set_temperature(self.config["night_temp"])
            self.security_system.arm()
            logging.info("Night routine completed successfully")
        except Exception as e:
            logging.error(f"Night routine failed: {e}")

    def update_config(self, key, value):
        try:
            if key in self.config:
                self.config[key] = value
                logging.info(f"Config updated: {key} = {value}")
            else:
                raise KeyError(f"Unknown config key: {key}")
        except KeyError as e:
            logging.error(f"Config update failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error updating config: {e}")

if __name__ == "__main__":
    controller = HomeController()
    controller.update_config("morning_temp", 75)
    controller.initialize_morning_routine()
    controller.initialize_night_routine()