import abc
import threading
from typing import Any, Callable, Dict, Optional, Union


class BehaviorBase(abc.ABC):
    @property
    @abc.abstractmethod
    def label(self) -> str:
        ...

    @abc.abstractmethod
    def run(self, data: Any) -> Any:
        ...


class CallableAdapter(BehaviorBase):
    def __init__(self, func: Callable[[Any], Any], name: Optional[str] = None) -> None:
        if not callable(func):
            raise TypeError("func must be callable")
        self._func = func
        self._name = name or getattr(func, "__name__", "callable")

    @property
    def label(self) -> str:
        return self._name

    def run(self, data: Any) -> Any:
        return self._func(data)


class UpperCaseBehavior(BehaviorBase):
    @property
    def label(self) -> str:
        return "upper_case"

    def run(self, data: Any) -> Any:
        if not isinstance(data, str):
            raise TypeError("UpperCaseBehavior expects a string")
        return data.upper()


class ReverseBehavior(BehaviorBase):
    @property
    def label(self) -> str:
        return "reverse"

    def run(self, data: Any) -> Any:
        if hasattr(data, "__reversed__") or isinstance(data, (str, list, tuple)):
            return type(data)(reversed(data)) if not isinstance(data, str) else data[::-1]
        raise TypeError("ReverseBehavior expects a sequence")


class ErrorBehavior(BehaviorBase):
    @property
    def label(self) -> str:
        return "error"

    def run(self, data: Any) -> Any:
        raise RuntimeError("intentional failure")


class NoOpBehavior(BehaviorBase):
    @property
    def label(self) -> str:
        return "noop"

    def run(self, data: Any) -> Any:
        return data


class ProcessorContext:
    def __init__(self, initial: Optional[Union[BehaviorBase, Callable[[Any], Any]]] = None) -> None:
        self._lock = threading.RLock()
        self._behavior: BehaviorBase = NoOpBehavior()
        self._fallback: Optional[BehaviorBase] = None
        self._usage: Dict[str, int] = {}
        if initial is not None:
            self.set_behavior(initial)

    def _wrap_if_callable(self, candidate: Union[BehaviorBase, Callable[[Any], Any]]) -> BehaviorBase:
        if isinstance(candidate, BehaviorBase):
            return candidate
        if callable(candidate):
            return CallableAdapter(candidate)
        raise TypeError("behavior must be a BehaviorBase or callable")

    def set_behavior(self, candidate: Union[BehaviorBase, Callable[[Any], Any]]) -> None:
        with self._lock:
            behavior = self._wrap_if_callable(candidate)
            self._behavior = behavior
            self._usage.setdefault(behavior.label, 0)

    def set_fallback(self, candidate: Optional[Union[BehaviorBase, Callable[[Any], Any]]]) -> None:
        with self._lock:
            self._fallback = None if candidate is None else self._wrap_if_callable(candidate)

    def process(self, data: Any) -> Any:
        with self._lock:
            behavior = self._behavior
        try:
            result = behavior.run(data)
            with self._lock:
                self._usage[behavior.label] = self._usage.get(behavior.label, 0) + 1
            return result
        except Exception:
            fallback = None
            with self._lock:
                fallback = self._fallback
            if fallback is not None:
                try:
                    res = fallback.run(data)
                    with self._lock:
                        self._usage[fallback.label] = self._usage.get(fallback.label, 0) + 1
                    return res
                except Exception:
                    raise
            raise

    def current_behavior(self) -> str:
        with self._lock:
            return self._behavior.label

    def usage_stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._usage)


if __name__ == "__main__":
    ctx = ProcessorContext()
    print(ctx.current_behavior(), ctx.process("hello"))

    ctx.set_behavior(UpperCaseBehavior())
    print(ctx.current_behavior(), ctx.process("hello"))

    ctx.set_behavior(ReverseBehavior())
    print(ctx.current_behavior(), ctx.process("hello"))

    def surround(text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("expected string")
        return f"<<{text}>>"

    ctx.set_behavior(surround)
    print(ctx.current_behavior(), ctx.process("hello"))

    ctx.set_behavior(ErrorBehavior())
    ctx.set_fallback(NoOpBehavior())
    try:
        print(ctx.current_behavior(), ctx.process("preserve"))
    except Exception as e:
        print("error propagated:", e)

    ctx.set_fallback(UpperCaseBehavior())
    print("fallback applied:", ctx.process("fallback test"))

    print("usage:", ctx.usage_stats())