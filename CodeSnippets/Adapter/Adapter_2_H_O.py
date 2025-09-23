import abc
import typing as t
import time
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceInterface(abc.ABC):
    @abc.abstractmethod
    def send(self, document: dict) -> bool:
        pass

class LegacyPrinterA:
    def print_bytes(self, data: bytes) -> int:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Expected bytes")
        if len(data) == 0:
            raise ValueError("No data to print")
        time.sleep(0.1)
        return len(data)

class LegacyPrinterB:
    def send_text(self, text: str, encoding: str = "utf-8") -> dict:
        if not isinstance(text, str):
            raise TypeError("Expected string")
        if not text.strip():
            raise ValueError("Empty text")
        encoded = text.encode(encoding)
        time.sleep(0.05)
        return {"status": "ok", "written": len(encoded)}

class UnsupportedServiceError(Exception):
    pass

class TransmissionError(Exception):
    pass

class CompatibilityLayer(ServiceInterface):
    def __init__(
        self,
        service_obj: object,
        timeout: float = 2.0,
        retries: int = 2,
        backoff_factor: float = 0.2,
    ):
        self._service = service_obj
        self._timeout = float(timeout)
        self._retries = max(0, int(retries))
        self._backoff = float(backoff_factor)
        self._executor = ThreadPoolExecutor(max_workers=1)

    def send(self, document: dict) -> bool:
        if not isinstance(document, dict):
            raise TypeError("document must be a dict")
        content = self._serialize(document)
        method = self._select_method()
        attempt = 0
        last_exc: t.Optional[Exception] = None
        while attempt <= self._retries:
            try:
                attempt += 1
                future = self._executor.submit(self._invoke_method, method, content)
                result = future.result(timeout=self._timeout)
                success = self._normalize_result(result)
                logger.info("Transmission succeeded on attempt %d: %s", attempt, success)
                return success
            except FutureTimeout:
                last_exc = TimeoutError("Service call timed out")
                logger.warning("Attempt %d timed out", attempt)
            except Exception as exc:
                last_exc = exc
                logger.warning("Attempt %d failed: %s", attempt, exc)
            time.sleep(self._backoff * attempt)
        raise TransmissionError("All transmission attempts failed") from last_exc

    def _serialize(self, document: dict) -> t.Dict[str, t.Any]:
        if "content" not in document:
            raise ValueError("document missing 'content'")
        content = document["content"]
        title = document.get("title", "")
        if not isinstance(title, str):
            title = str(title)
        return {"title": title, "content": content}

    def _select_method(self) -> str:
        candidates = ["print_bytes", "send_text", "send"]
        for name in candidates:
            if hasattr(self._service, name) and callable(getattr(self._service, name)):
                return name
        raise UnsupportedServiceError("No compatible method found on service object")

    def _invoke_method(self, method_name: str, content: dict) -> t.Any:
        if method_name == "print_bytes":
            payload = self._to_bytes(content)
            return getattr(self._service, "print_bytes")(payload)
        if method_name == "send_text":
            text = self._to_text(content)
            return getattr(self._service, "send_text")(text, "utf-8")
        if method_name == "send":
            payload = {"title": content["title"], "body": self._to_text(content)}
            return getattr(self._service, "send")(payload)
        raise UnsupportedServiceError("Method resolution failed")

    def _to_bytes(self, content: dict) -> bytes:
        body = content["content"]
        if isinstance(body, bytes):
            return body
        if isinstance(body, str):
            return body.encode("utf-8")
        if isinstance(body, (bytearray, memoryview)):
            return bytes(body)
        raise TypeError("Unsupported content type for bytes conversion")

    def _to_text(self, content: dict) -> str:
        body = content["content"]
        if isinstance(body, str):
            return body
        if isinstance(body, (bytes, bytearray, memoryview)):
            try:
                return bytes(body).decode("utf-8")
            except Exception as exc:
                raise ValueError("Failed to decode bytes to text") from exc
        return str(body)

    def _normalize_result(self, result: t.Any) -> bool:
        if isinstance(result, bool):
            return result
        if isinstance(result, int):
            return result > 0
        if isinstance(result, dict):
            status = result.get("status")
            if status == "ok":
                written = result.get("written", 0)
                return bool(written)
            return False
        return bool(result)

if __name__ == "__main__":
    doc = {"title": "Report", "content": "This is the content.\nLine 2."}
    legacy_a = LegacyPrinterA()
    legacy_b = LegacyPrinterB()
    wrapper_a = CompatibilityLayer(legacy_a, timeout=1.0, retries=1)
    wrapper_b = CompatibilityLayer(legacy_b, timeout=1.0, retries=1)
    try:
        result_a = wrapper_a.send(doc)
        print("legacy_a result:", result_a)
    except Exception as e:
        print("legacy_a failed:", type(e).__name__, e)
    try:
        result_b = wrapper_b.send(doc)
        print("legacy_b result:", result_b)
    except Exception as e:
        print("legacy_b failed:", type(e).__name__, e)