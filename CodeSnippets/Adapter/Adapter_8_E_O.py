class ServiceInterface:
    def perform(self) -> str:
        raise NotImplementedError

class OldService:
    def old_action(self) -> str:
        return "legacy result"

class ServiceBridge(ServiceInterface):
    def __init__(self, legacy_service: OldService):
        self._legacy = legacy_service
    def perform(self) -> str:
        legacy_result = self._legacy.old_action()
        return f"converted({legacy_result})"

if __name__ == "__main__":
    legacy = OldService()
    service = ServiceBridge(legacy)
    print(service.perform())