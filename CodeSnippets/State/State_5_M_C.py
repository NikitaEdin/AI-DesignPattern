from abc import ABC, abstractmethod

class MoodHandler(ABC):
    @abstractmethod
    def handle_compliment(self, person):
        pass
    
    @abstractmethod
    def handle_criticism(self, person):
        pass
    
    @abstractmethod
    def get_response(self):
        pass

class HappyMood(MoodHandler):
    def handle_compliment(self, person):
        person.current_mood = CheerfulMood()
        return "That makes me feel amazing!"
    
    def handle_criticism(self, person):
        person.current_mood = SadMood()
        return "That hurts a bit..."
    
    def get_response(self):
        return "I'm feeling pretty good!"

class SadMood(MoodHandler):
    def handle_compliment(self, person):
        person.current_mood = HappyMood()
        return "Thank you, that helps!"
    
    def handle_criticism(self, person):
        person.current_mood = AngryMood()
        return "Why are you being so mean?"
    
    def get_response(self):
        return "I'm feeling down today..."

class CheerfulMood(MoodHandler):
    def handle_compliment(self, person):
        return "You're so kind! I'm on cloud nine!"
    
    def handle_criticism(self, person):
        person.current_mood = HappyMood()
        return "I won't let that bring me down!"
    
    def get_response(self):
        return "Life is wonderful!"

class AngryMood(MoodHandler):
    def handle_compliment(self, person):
        person.current_mood = SadMood()
        return "I appreciate that... sorry for being upset"
    
    def handle_criticism(self, person):
        return "I don't want to hear it right now!"
    
    def get_response(self):
        return "I'm really frustrated!"

class Person:
    def __init__(self):
        self.current_mood = HappyMood()
    
    def receive_compliment(self):
        return self.current_mood.handle_compliment(self)
    
    def receive_criticism(self):
        return self.current_mood.handle_criticism(self)
    
    def express_feelings(self):
        return self.current_mood.get_response()

if __name__ == "__main__":
    person = Person()
    print(person.express_feelings())
    print(person.receive_compliment())
    print(person.express_feelings())
    print(person.receive_criticism())
    print(person.express_feelings())
    print(person.receive_criticism())
    print(person.express_feelings())