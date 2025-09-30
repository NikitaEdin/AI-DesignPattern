class Light:
    def turn_on(self): print("Light on")
    def turn_off(self): print("Light off")

class Speaker:
    def start_music(self): print("Music playing")
    def stop_music(self): print("Music stopped")

class Climate:
    def set_temperature(self, t): print(f"Temperature set to {t}")

class HomeManager:
    def __init__(self):
        self.light = Light()
        self.speaker = Speaker()
        self.climate = Climate()
    def evening_mode(self):
        self.light.turn_on()
        self.speaker.start_music()
        self.climate.set_temperature(20)
    def morning_mode(self):
        self.light.turn_on()
        self.speaker.stop_music()
        self.climate.set_temperature(22)
    def leave_mode(self):
        self.light.turn_off()
        self.speaker.stop_music()
        self.climate.set_temperature(25)

if __name__ == "__main__":
    hm = HomeManager()
    hm.evening_mode()
    hm.leave_mode()