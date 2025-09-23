from abc import ABC, abstractmethod

class TrafficBehavior(ABC):
    @abstractmethod
    def proceed(self, light):
        pass
    
    @abstractmethod
    def get_duration(self):
        pass

class RedBehavior(TrafficBehavior):
    def proceed(self, light):
        light.current_behavior = GreenBehavior()
        return "Changed to GREEN"
    
    def get_duration(self):
        return 30

class GreenBehavior(TrafficBehavior):
    def proceed(self, light):
        light.current_behavior = YellowBehavior()
        return "Changed to YELLOW"
    
    def get_duration(self):
        return 45

class YellowBehavior(TrafficBehavior):
    def proceed(self, light):
        light.current_behavior = RedBehavior()
        return "Changed to RED"
    
    def get_duration(self):
        return 5

class TrafficLight:
    def __init__(self):
        self.current_behavior = RedBehavior()
    
    def next_phase(self):
        try:
            return self.current_behavior.proceed(self)
        except Exception as e:
            return f"Error: {e}"
    
    def get_current_duration(self):
        return self.current_behavior.get_duration()
    
    def get_current_phase(self):
        return self.current_behavior.__class__.__name__.replace('Behavior', '').upper()

if __name__ == "__main__":
    traffic_light = TrafficLight()
    
    for cycle in range(6):
        phase = traffic_light.get_current_phase()
        duration = traffic_light.get_current_duration()
        print(f"Current: {phase} (Duration: {duration}s)")
        result = traffic_light.next_phase()
        print(f"Action: {result}\n")