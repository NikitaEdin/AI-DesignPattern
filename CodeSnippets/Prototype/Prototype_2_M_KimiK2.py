import copy

class BaseConfig:
    def __init__(self, name, settings):
        self.name = name
        self.settings = settings

    def duplicate(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, settings={self.settings})"


class AppConfig(BaseConfig):
    def __init__(self, name, settings, environment):
        super().__init__(name, settings)
        self.environment = environment

    def duplicate(self):
        return copy.deepcopy(self)


class DbConfig(BaseConfig):
    def __init__(self, name, settings, credentials):
        super().__init__(name, settings)
        self.credentials = credentials

    def duplicate(self):
        return copy.deepcopy(self)


if __name__ == "__main__":
    original_app = AppConfig("webapp", {"debug": True}, "development")
    cloned_app = original_app.duplicate()
    cloned_app.name = "webapp-clone"

    original_db = DbConfig("main_db", {"pool_size": 10}, {"user": "admin"})
    cloned_db = original_db.duplicate()
    cloned_db.settings["pool_size"] = 20

    print(original_app)
    print(cloned_app)
    print(original_db)
    print(cloned_db)