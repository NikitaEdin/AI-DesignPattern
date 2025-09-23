class RealService:
    def request(self):
        return "Real service response"

class ServiceGateway:
    def __init__(self):
        self._real_service = None
    
    def request(self):
        if self._real_service is None:
            self._real_service = RealService()
        return self._real_service.request()

if __name__ == "__main__":
    gateway = ServiceGateway()
    print(gateway.request())
    print(gateway.request())