from abc import ABC, abstractmethod

class DataService(ABC):
    @abstractmethod
    def fetch_data(self, key):
        pass

class DataAccess(DataService):
    def fetch_data(self, key):
        return f"Data for {key}"

class SecureDataAccess(DataService):
    def __init__(self, data_access, user_role):
        self._data_access = data_access
        self.user_role = user_role
    
    def fetch_data(self, key):
        if not self._is_allowed():
            raise PermissionError("Access denied")
        return self._data_access.fetch_data(key)
    
    def _is_allowed(self):
        return self.user_role == "admin"

if __name__ == "__main__":
    real_service = DataAccess()
    secure_service = SecureDataAccess(real_service, "admin")
    print(secure_service.fetch_data("user123"))