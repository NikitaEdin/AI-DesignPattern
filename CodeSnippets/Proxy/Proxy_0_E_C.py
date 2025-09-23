class RealService:
    def request(self):
        return "RealService: Handling request"

class ServiceWrapper:
    def __init__(self):
        self._real_service = None
    
    def request(self):
        if self._real_service is None:
            print("Creating real service...")
            self._real_service = RealService()
        print("Wrapper: Before forwarding request")
        result = self._real_service.request()
        print("Wrapper: After forwarding request")
        return result

if __name__ == "__main__":
    wrapper = ServiceWrapper()
    print(wrapper.request())
    print(wrapper.request())