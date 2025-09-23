class DesiredService:
    def perform(self):
        raise NotImplementedError

class LegacyService:
    def old_operation(self):
        return "legacy result"

class Translator(DesiredService):
    def __init__(self, legacy):
        self.legacy = legacy
    def perform(self):
        result = self.legacy.old_operation()
        return f"translated({result})"

if __name__ == "__main__":
    legacy = LegacyService()
    service = Translator(legacy)
    print(service.perform())