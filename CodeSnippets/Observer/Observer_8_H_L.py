# Python code for Observer Design Pattern

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_all(self, *args, **kwargs):
        for observer in self._observers:
            observer(*args, **kwargs)

class Observable:
    def __init__(self):
        self._data = None

    def set_data(self, data):
        self._data = data
        self.notify_all()

    def get_data(self):
        return self._data

# Example usage

def main():
    subject = Subject()
    observable = Observable()

    # Attach observer to the subject
    subject.attach(observable)

    # Set data for the observable
    observable.set_data("Hello World")

if __name__ == "__main__":
    main()