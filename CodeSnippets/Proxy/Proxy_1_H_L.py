import time

class RealSubject:
    def do_something(self):
        print("Real Subject: Working...")
        time.sleep(2)
        print("Real Subject: Completed.")

class Proxy:
    def __init__(self, real_subject):
        self.real_subject = real_subject

    def do_something(self):
        print("Proxy: Working...")
        self.real_subject.do_something()
        print("Proxy: Completed.")

if __name__ == "__main__":
    real_subject = RealSubject()
    proxy = Proxy(real_subject)
    proxy.do_something()