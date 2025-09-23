class TargetInterface:
    def execute(self, data):
        raise NotImplementedError

class LegacyService:
    def specific_request(self, payload):
        return f"legacy-> {payload[::-1]}"

class ServiceBridge(TargetInterface):
    def __init__(self, legacy):
        self.legacy = legacy
    def execute(self, data):
        converted = f"<{data}>"
        return self.legacy.specific_request(converted)

def main():
    legacy = LegacyService()
    client = ServiceBridge(legacy)
    print(client.execute("hello"))

if __name__ == "__main__":
    main()