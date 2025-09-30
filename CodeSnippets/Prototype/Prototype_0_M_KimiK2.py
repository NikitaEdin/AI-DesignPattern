import copy

class ConfigBuilder:
    def __vetkopio(self):
        return copy.deepcopy(self)

    def update(self, **kwargs):
        updated = self.__vetkopio()
        updated.settings.update(kwargs)
        return updated

    def __init__(self, **kwargs):
        self.settings = kwargs

    def __str__(self):
        return str(self.settings)


class ServerConfig(ConfigBuilder):
    def __init__(self):
        super().__init__(host="localhost", port=8080, ssl=True)


if __name__ == "__main__":
    base = ServerConfig()
    staging = base.update(host="staging.api", port=443)
    production = base.update(host="api.example.com", port=443, logging="verbose")
    print("Base:", base)
    print("Staging:", staging)
    print("Production:", production)