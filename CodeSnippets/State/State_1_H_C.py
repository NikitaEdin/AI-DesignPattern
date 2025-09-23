from abc import ABC, abstractmethod
from typing import Dict, Any
import json

class MoodInterface(ABC):
    @abstractmethod
    def handle_event(self, context: 'Robot', event: str, data: Dict[str, Any] = None) -> str:
        pass
    
    @abstractmethod
    def get_response_tone(self) -> str:
        pass
    
    @abstractmethod
    def can_transition_to(self, new_mood: str) -> bool:
        pass

class HappyMood(MoodInterface):
    def handle_event(self, context: 'Robot', event: str, data: Dict[str, Any] = None) -> str:
        if event == "compliment":
            context.energy += 10
            return "Thank you! That makes me very happy!"
        elif event == "criticism" and context.energy > 30:
            context.change_mood("neutral")
            return "I'll try to do better."
        elif event == "criticism":
            context.change_mood("sad")
            return "Oh no, I'm sorry I disappointed you..."
        return "I'm feeling great today!"
    
    def get_response_tone(self) -> str:
        return "enthusiastic"
    
    def can_transition_to(self, new_mood: str) -> bool:
        return new_mood in ["neutral", "sad"]

class NeutralMood(MoodInterface):
    def handle_event(self, context: 'Robot', event: str, data: Dict[str, Any] = None) -> str:
        if event == "compliment":
            context.change_mood("happy")
            context.energy += 15
            return "Thank you! I'm starting to feel better!"
        elif event == "criticism":
            context.change_mood("sad")
            return "I understand your concerns."
        elif event == "joke" and context.energy > 20:
            context.change_mood("happy")
            return "Haha! That's funny!"
        return "I'm doing okay."
    
    def get_response_tone(self) -> str:
        return "calm"
    
    def can_transition_to(self, new_mood: str) -> bool:
        return True

class SadMood(MoodInterface):
    def handle_event(self, context: 'Robot', event: str, data: Dict[str, Any] = None) -> str:
        if event == "compliment":
            if context.energy < 20:
                context.change_mood("neutral")
                context.energy += 5
                return "Thank you... that helps a little."
            else:
                context.change_mood("happy")
                context.energy += 20
                return "You really know how to cheer me up!"
        elif event == "criticism":
            context.energy = max(0, context.energy - 10)
            return "I'm trying my best..."
        return "I'm feeling a bit down today."
    
    def get_response_tone(self) -> str:
        return "melancholic"
    
    def can_transition_to(self, new_mood: str) -> bool:
        return new_mood in ["neutral", "happy"]

class Robot:
    def __init__(self):
        self._moods = {
            "happy": HappyMood(),
            "neutral": NeutralMood(),
            "sad": SadMood()
        }
        self._current_mood = self._moods["neutral"]
        self.energy = 50
        self._mood_history = ["neutral"]
    
    def change_mood(self, new_mood: str):
        if new_mood in self._moods and self._current_mood.can_transition_to(new_mood):
            self._current_mood = self._moods[new_mood]
            self._mood_history.append(new_mood)
            if len(self._mood_history) > 10:
                self._mood_history.pop(0)
    
    def interact(self, event: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        response = self._current_mood.handle_event(self, event, data)
        return {
            "response": response,
            "tone": self._current_mood.get_response_tone(),
            "energy": self.energy,
            "current_mood": self.get_current_mood_name()
        }
    
    def get_current_mood_name(self) -> str:
        for name, mood in self._moods.items():
            if mood is self._current_mood:
                return name
        return "unknown"
    
    def get_mood_history(self) -> list:
        return self._mood_history.copy()

if __name__ == "__main__":
    robot = Robot()
    
    events = [
        ("compliment", "You're doing great!"),
        ("joke", "Why did the robot cross the road?"),
        ("criticism", "You made an error"),
        ("compliment", "But you're learning!"),
        ("criticism", "Still not perfect though")
    ]
    
    for event, description in events:
        result = robot.interact(event)
        print(f"Event: {description}")
        print(f"Robot ({result['current_mood']}, energy={result['energy']}): {result['response']}")
        print(f"Tone: {result['tone']}\n")
    
    print(f"Mood history: {' -> '.join(robot.get_mood_history())}")