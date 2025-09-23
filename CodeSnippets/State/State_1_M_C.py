from abc import ABC, abstractmethod

class TrafficLightBehavior(ABC):
    @abstractmethod
    def handle_timer(self, context):
        pass
    
    @abstractmethod
    def get_color(self):
        pass

class RedLight(TrafficLightBehavior):
    def handle_timer(self, context):
        context.set_behavior(GreenLight())
    
    def get_color(self):
        return "RED"

class YellowLight(TrafficLightBehavior):
    def handle_timer(self, context):
        context.set_behavior(RedLight())
    
    def get_color(self):
        return "YELLOW"

class GreenLight(TrafficLightBehavior):
    def handle_timer(self, context):
        context.set_behavior(YellowLight())
    
    def get_color(self):
        return "GREEN"

class TrafficLight:
    def __init__(self):
        self._current_behavior = RedLight()
        self._timer_count = 0
    
    def set_behavior(self, behavior):
        if not isinstance(behavior, TrafficLightBehavior):
            raise ValueError("Invalid behavior type")
        self._current_behavior = behavior
        self._timer_count = 0
    
    def tick(self):
        self._timer_count += 1
        if self._timer_count >= 3:
            self._current_behavior.handle_timer(self)
    
    def get_current_color(self):
        return self._current_behavior.get_color()

if __name__ == "__main__":
    light = TrafficLight()
    
    for i in range(12):
        print(f"Time {i+1}: {light.get_current_color()}")
        light.tick()