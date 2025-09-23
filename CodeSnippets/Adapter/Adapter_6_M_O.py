import json
from typing import Any, Dict

class IntegrationError(Exception):
    pass

class TargetProcessor:
    def process(self, data: Dict[str, Any]) -> str:
        raise NotImplementedError

class LegacyService:
    def run(self, payload: str) -> bytes:
        if not isinstance(payload, str):
            raise TypeError("payload must be a string")
        processed = {"status": "ok", "received": json.loads(payload)}
        return json.dumps(processed).encode("utf-8")

class ServiceBridge(TargetProcessor):
    def __init__(self, legacy: LegacyService):
        self._legacy = legacy
        self._cache: Dict[str, str] = {}
    def process(self, data: Dict[str, Any]) -> str:
        try:
            key = json.dumps(data, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise IntegrationError("input not serializable") from exc
        if key in self._cache:
            return self._cache[key]
        try:
            raw = self._legacy.run(key)
            result = raw.decode("utf-8")
        except Exception as exc:
            raise IntegrationError("legacy service failed") from exc
        self._cache[key] = result
        return result

if __name__ == "__main__":
    legacy = LegacyService()
    bridge = ServiceBridge(legacy)
    payload = {"user": "alice", "action": "login"}
    print(bridge.process(payload))
    print(bridge.process(payload))
    bad_payload = {"unserializable": set([1,2,3])}
    try:
        bridge.process(bad_payload)
    except IntegrationError as e:
        print("Error:", e)