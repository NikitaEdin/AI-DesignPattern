class NotificationCenter:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_all(self, message):
        for observer in self.observers:
            observer.update(message)

class TaskManager:
    def __init__(self):
        self.task_list = []
        self.notification_center = NotificationCenter()

    def add_task(self, task):
        self.task_list.append(task)
        self.notification_center.add_observer(task)

    def remove_task(self, task):
        self.task_list.remove(task)
        self.notification_center.remove_observer(task)

class Task:
    def __init__(self, name):
        self.name = name
        self.notification_center = NotificationCenter()

    def update(self, message):
        print(f"Task {self.name} received message: {message}")

if __name__ == "__main__":
    task_manager = TaskManager()

    task1 = Task("First Task")
    task2 = Task("Second Task")

    task_manager.add_task(task1)
    task_manager.add_task(task2)

    message = "Hello from the task manager!"
    task_manager.notification_center.notify_all(message)