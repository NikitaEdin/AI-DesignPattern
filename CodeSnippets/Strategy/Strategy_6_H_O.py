import abc
import threading
import concurrent.futures
import statistics
import logging
import time
from typing import Any, Iterable, Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvalidInputError(ValueError):
    pass

class ExecutionError(RuntimeError):
    pass

class BaseProcessor(abc.ABC):
    @abc.abstractmethod
    def process(self, data: Iterable[Any]) -> Any:
        pass

class UniqueSorter(BaseProcessor):
    def process(self, data: Iterable[Any]) -> List[Any]:
        if data is None:
            raise InvalidInputError("data must be provided")
        seq = list(data)
        seen_hashable = set()
        seen_unhashable = []
        result = []
        for item in seq:
            try:
                if item not in seen_hashable:
                    seen_hashable.add(item)
                    result.append(item)
            except TypeError:
                if not any(item == prev for prev in seen_unhashable):
                    seen_unhashable.append(item)
                    result.append(item)
        try:
            return sorted(result)
        except TypeError:
            return result

class StatsCollector(BaseProcessor):
    def process(self, data: Iterable[float]) -> dict:
        if data is None:
            raise InvalidInputError("data must be provided")
        seq = list(data)
        if len(seq) == 0:
            raise InvalidInputError("data must be non-empty")
        mean = statistics.mean(seq)
        med = statistics.median(seq)
        stdev = statistics.pstdev(seq) if len(seq) == 1 else statistics.stdev(seq)
        return {"count": len(seq), "mean": mean, "median": med, "stdev": stdev}

class PauseProcessor(BaseProcessor):
    def __init__(self, delay: float = 1.0):
        self.delay = float(delay)
    def process(self, data: Iterable[Any]) -> Any:
        time.sleep(self.delay)
        return list(data)

class ExecutorHost:
    def __init__(self, processor: BaseProcessor, fallback: Optional[BaseProcessor] = None):
        if not isinstance(processor, BaseProcessor):
            raise TypeError("processor must implement BaseProcessor")
        if fallback is not None and not isinstance(fallback, BaseProcessor):
            raise TypeError("fallback must implement BaseProcessor or be None")
        self._lock = threading.RLock()
        self._processor = processor
        self._fallback = fallback

    def set_processor(self, p: BaseProcessor):
        if not isinstance(p, BaseProcessor):
            raise TypeError("processor must implement BaseProcessor")
        with self._lock:
            self._processor = p

    def set_fallback(self, p: Optional[BaseProcessor]):
        if p is not None and not isinstance(p, BaseProcessor):
            raise TypeError("fallback must implement BaseProcessor or be None")
        with self._lock:
            self._fallback = p

    def process(self, data: Iterable[Any], timeout: Optional[float] = None) -> Any:
        with self._lock:
            primary = self._processor
            fallback = self._fallback
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
            fut_primary = ex.submit(primary.process, data)
            try:
                return fut_primary.result(timeout=timeout)
            except concurrent.futures.TimeoutError as te:
                fut_primary.cancel()
                if fallback is None:
                    raise ExecutionError(f"primary timed out after {timeout}s") from te
                fut_fallback = ex.submit(fallback.process, data)
                try:
                    return fut_fallback.result(timeout=timeout)
                except concurrent.futures.TimeoutError as te2:
                    fut_fallback.cancel()
                    msg = f"primary timed out; fallback also timed out after {timeout}s"
                    raise ExecutionError(msg) from te
                except Exception as fb_exc:
                    msg = f"primary timed out; fallback raised {fb_exc!r}"
                    raise ExecutionError(msg) from te
            except Exception as primary_exc:
                if fallback is None:
                    raise ExecutionError(f"primary raised {primary_exc!r}") from primary_exc
                fut_fallback = ex.submit(fallback.process, data)
                try:
                    return fut_fallback.result(timeout=timeout)
                except Exception as fb_exc:
                    msg = f"primary raised {primary_exc!r}; fallback raised {fb_exc!r}"
                    raise ExecutionError(msg) from primary_exc

class LoggingWrapper(BaseProcessor):
    def __init__(self, wrapped: BaseProcessor):
        if not isinstance(wrapped, BaseProcessor):
            raise TypeError("wrapped must implement BaseProcessor")
        self._wrapped = wrapped

    def process(self, data: Iterable[Any]) -> Any:
        size = "unknown"
        try:
            if hasattr(data, "__len__"):
                size = len(data)
        except Exception:
            size = "unknown"
        logger.info("starting %s with size=%s", type(self._wrapped).__name__, size)
        try:
            result = self._wrapped.process(data)
            logger.info("finished %s successfully", type(self._wrapped).__name__)
            return result
        except Exception:
            logger.exception("error in %s", type(self._wrapped).__name__)
            raise

if __name__ == "__main__":
    primary = PauseProcessor(delay=3.0)
    fallback = UniqueSorter()
    host = ExecutorHost(primary, fallback)
    wrapped_host_processor = LoggingWrapper(primary)
    host.set_processor(wrapped_host_processor)
    try:
        print("Attempt 1 (expect fallback due to timeout):")
        res = host.process([3, 1, 2, 1], timeout=1.0)
        print("Result:", res)
    except ExecutionError as e:
        print("ExecutionError:", e)

    host.set_processor(UniqueSorter())
    host.set_fallback(StatsCollector())
    print("\nAttempt 2 (primary succeeds):")
    print("Result:", host.process([5, 2, 3, 2], timeout=2.0))

    print("\nAttempt 3 (primary raises, fallback used):")
    host.set_processor(StatsCollector())
    host.set_fallback(UniqueSorter())
    try:
        print("Stats on empty -> should raise and fallback dedupe will run:")
        print("Result:", host.process([], timeout=1.0))
    except ExecutionError as e:
        print("ExecutionError:", e)