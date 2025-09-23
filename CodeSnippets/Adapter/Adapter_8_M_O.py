import json
import hashlib
import time


class ReportFormatterInterface:
    def format_report(self, data):
        raise NotImplementedError("format_report must be implemented")


class LegacyReportEngine:
    def generate(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dict")
        time.sleep(0.1)
        try:
            result = {
                "status": "ok",
                "timestamp": time.time(),
                "content": payload
            }
            return json.dumps(result).encode("utf-8")
        except Exception as exc:
            raise RuntimeError("Generation failed") from exc


class ReportServiceConnector(ReportFormatterInterface):
    def __init__(self, legacy_engine):
        if not hasattr(legacy_engine, "generate"):
            raise TypeError("Provided service lacks required method")
        self._engine = legacy_engine
        self._cache = {}

    def _cache_key(self, data):
        raw = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def format_report(self, data):
        if not isinstance(data, (dict, list)):
            raise TypeError("Data must be a dict or list")
        key = self._cache_key(data)
        if key in self._cache:
            return self._cache[key]
        try:
            payload = data if isinstance(data, dict) else {"items": data}
            raw_bytes = self._engine.generate(payload)
            report_text = raw_bytes.decode("utf-8")
            self._cache[key] = report_text
            return report_text
        except Exception as exc:
            raise RuntimeError("Failed to format report") from exc


if __name__ == "__main__":
    engine = LegacyReportEngine()
    connector = ReportServiceConnector(engine)

    sample = {"title": "Sales", "values": [100, 200, 150]}
    print(connector.format_report(sample))
    print(connector.format_report(sample))

    another = ["entry1", "entry2"]
    print(connector.format_report(another))