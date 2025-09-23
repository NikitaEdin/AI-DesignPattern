class TargetInterface:
    def request(self):
        raise NotImplementedError

class OldService:
    def specific_request(self):
        return "Old result"

class ServiceBridge(TargetInterface):
    def __init__(self, service):
        self._service = service
    def request(self):
        return "Converted: " + self._service.specific_request()

def client_code(target: TargetInterface):
    print(target.request())

if __name__ == "__main__":
    old = OldService()
    bridge = ServiceBridge(old)
    client_code(bridge)