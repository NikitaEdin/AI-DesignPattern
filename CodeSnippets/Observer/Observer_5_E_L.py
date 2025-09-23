class User:
    def __init__(self, name):
        self.name = name

class NotificationCenter:
    def __init__(self):
        self.observers = set()
    
    def register(self, observer):
        self.observers.add(observer)
    
    def unregister(self, observer):
        self.observers.remove(observer)
    
    def notify(self, message):
        for observer in self.observers:
            observer.update(message)

class TaskManager:
    def __init__(self, task_name, notification_center):
        self.task_name = task_name
        self.notification_center = notification_center
    
    def start(self):
        print(f"Starting {self.task_name}...")
        self.notification_center.notify(f"{self.task_name} started.")
    
    def complete(self):
        print(f"Completing {self.task_name}...")
        self.notification_center.notify(f"{self.task_name} completed.")