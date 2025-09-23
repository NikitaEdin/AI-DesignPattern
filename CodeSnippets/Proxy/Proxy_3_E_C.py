class RealService:
    def request(self):
        return "Processing real request"

class ServiceWrapper:
    def __init__(self):
        self._real_service = None
    
    def request(self):
        if self._real_service is None:
            print("Creating real service")
            self._real_service = RealService()
        print("Wrapper: delegating to real service")
        return self._real_service.request()

if __name__ == "__main__":
    wrapper = ServiceWrapper()
    
    print("First call:")
    result1 = wrapper.request()
    print(result1)
    
    print("\nSecond call:")
    result2 = wrapper.request()
    print(result2)