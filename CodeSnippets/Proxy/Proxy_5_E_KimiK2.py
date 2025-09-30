class RealService:
    def request(self):
        return "RealService: handling request"

class ServiceWrapper:
    def __init__(self):
        self._real = RealService()
    
    def request(self):
        print("ServiceWrapper: checking access")
        return self._real.request()

if __name__ == "__main__":
    service = ServiceWrapper()
    print(service.request())