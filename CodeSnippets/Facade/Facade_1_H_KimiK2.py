import time
from enum import Enum
from typing import Optional

class LightMode(Enum):
    OFF = 0
    DIM = 1
    NORMAL = 2
    BRIGHT = 3

class ClimateMode(Enum):
    OFF = 0
    COOL = 1
    HEAT = 2
    AUTO = 3

class SecurityLevel(Enum):
    DISARMED = 0
    ARMED_STAY = 1
    ARMED_AWAY = 2

class Lighting:
    def __init__(self):
        self.mode = LightMode.OFF
        self.brightness = 0
        
    def set_mode(self, mode: LightMode):
        self.mode = mode
        self.brightness = mode.value * 33
        time.sleep(0.1)
        
    def get_status(self) -> dict:
        return {"mode": self.mode.name, "brightness": self.brightness}

class ClimateControl:
    def __init__(self):
        self.mode = ClimateMode.OFF
        self.temperature = 22
        
    def set_mode(self, mode: ClimateMode):
        self.mode = mode
        if mode == ClimateMode.COOL:
            self.temperature = 20
        elif mode == ClimateMode.HEAT:
            self.temperature = 24
        time.sleep(0.2)
        
    def get_status(self) -> dict:
        return {"mode": self.mode.name, "temperature": self.temperature}

class Security:
    def __init__(self):
        self.level = SecurityLevel.DISARMED
        self.cameras_active = False
        
    def set_level(self, level: SecurityLevel):
        self.level = level
        self.cameras_active = level != SecurityLevel.DISARMED
        time.sleep(0.15)
        
    def get_status(self) -> dict:
        return {"level": self.level.name, "cameras": self.cameras_active}

class HomeManager:
    def __init__(self):
        self.lighting = Lighting()
        self.climate = ClimateControl()
        self.security = Security()
        
    def activate_sleep_mode(self):
        self.lighting.set_mode(LightMode.OFF)
        self.climate.set_mode(ClimateMode.OFF)
        self.security.set_level(SecurityLevel.ARMED_STAY)
        
    def activate_away_mode(self):
        self.lighting.set_mode(LightMode.OFF)
        self.climate.set_mode(ClimateMode.AUTO)
        self.security.set_level(SecurityLevel.ARMED_AWAY)
        
    def activate_evening_mode(self):
        self.lighting.set_mode(LightMode.DIM)
        self.climate.set_mode(ClimateMode.HEAT)
        self.security.set_level(SecurityLevel.ARMED_STAY)
        
    def activate_party_mode(self):
        self.lighting.set_mode(LightMode.BRIGHT)
        self.climate.set_mode(ClimateMode.COOL)
        self.security.set_level(SecurityLevel.DISARMED)
        
    def get_full_status(self) -> dict:
        return {
            "lighting": self.lighting.get_status(),
            "climate": self.climate.get_status(),
            "security": self.security.get_status()
        }

if __name__ == "__main__":
    home = HomeManager()
    
    home.activate_evening_mode()
    print("Evening mode activated:", home.get_full_status())
    
    time.sleep(0.5)
    
    home.activate_sleep_mode()
    print("Sleep mode activated:", home.get_full_status())