class Service:
    def execute(self, data, **kwargs):
        raise NotImplementedError

class BasicService(Service):
    def execute(self, data, **kwargs):
        if not isinstance(data, str): raise TypeError("data must be a string")
        return f"Processed: {data}"

class ServiceWrapper(Service):
    def __init__(self, service):
        if not isinstance(service, Service): raise TypeError("service must implement Service")
        self._service = service
    def execute(self, data, **kwargs):
        return self._service.execute(data, **kwargs)

class AuthWrapper(ServiceWrapper):
    def __init__(self, service, required_token):
        super().__init__(service); self._required_token = required_token
    def execute(self, data, **kwargs):
        token = kwargs.get("token")
        if token != self._required_token: raise PermissionError("invalid or missing token")
        return super().execute(data, **kwargs)

class AuditWrapper(ServiceWrapper):
    def __init__(self, service, enabled=True):
        super().__init__(service); self.enabled = bool(enabled); self.log = []
    def execute(self, data, **kwargs):
        try:
            result = super().execute(data, **kwargs)
            status = "ok"
            return result
        finally:
            if self.enabled:
                entry = {"input": data, "status": locals().get("status", "error")}
                self.log.append(entry)

if __name__ == "__main__":
    core = BasicService()
    audited = AuditWrapper(core, enabled=True)
    secured = AuthWrapper(audited, required_token="secr3t")
    try:
        print(secured.execute("hello world", token="secr3t"))
    except Exception as e:
        print("Error:", e)
    try:
        print(secured.execute("bad call", token="wrong"))
    except Exception as e:
        print("Error:", e)
    print("Audit log:", audited.log)