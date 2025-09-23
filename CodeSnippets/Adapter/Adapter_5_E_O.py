class DesiredService:
    def request(self):
        return "Standard result"

class LegacyService:
    def specific_request(self):
        return "legacy: 42"

class Converter:
    def __init__(self, legacy):
        self.legacy = legacy
    def request(self):
        data = self.legacy.specific_request()
        return f"Converted({data})"

def main():
    standard = DesiredService()
    legacy = LegacyService()
    wrapper = Converter(legacy)
    for service in (standard, wrapper):
        print(service.request())

if __name__ == "__main__":
    main()