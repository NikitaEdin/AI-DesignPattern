import inspect
import threading

class PaymentPort:
    def process_payment(self, amount: float, currency: str, metadata: dict = None):
        raise NotImplementedError

class LegacyGatewayRich:
    def charge(self, total_cents: int, currency_code: str, meta: dict = None):
        return {"charged_cents": total_cents, "currency": currency_code, "meta": meta}

class LegacyGatewaySimple:
    def pay(self, amount_cents: int) -> bool:
        return amount_cents > 0

class CompatibilityWrapper:
    def __init__(self, service, mapping: dict, enable_cache: bool = True):
        self._service = service
        self._mapping = mapping.copy()
        self._lock = threading.RLock()
        self._cache = {} if enable_cache else None
        self._validate_mapping()

    def _validate_mapping(self):
        for key, value in self._mapping.items():
            if key != "process_payment":
                raise ValueError("Only 'process_payment' is supported by this wrapper")
            if isinstance(value, str):
                if not hasattr(self._service, value) or not callable(getattr(self._service, value)):
                    raise ValueError(f"Service lacks callable method '{value}'")
            elif callable(value):
                pass
            elif isinstance(value, tuple):
                if len(value) != 2:
                    raise ValueError("Tuple mapping must be (method_name:str, transformer:callable|None)")
                method_name, transformer = value
                if not isinstance(method_name, str):
                    raise ValueError("Tuple first element must be method name string")
                if not hasattr(self._service, method_name) or not callable(getattr(self._service, method_name)):
                    raise ValueError(f"Service lacks callable method '{method_name}'")
                if transformer is not None and not callable(transformer):
                    raise ValueError("Transformer must be callable or None")
            else:
                raise ValueError("Mapping value must be a method name, callable, or (method, transformer) tuple")

    def _normalize_canonical(self, amount, currency, metadata):
        cents = int(round(float(amount) * 100))
        return {"cents": cents, "currency": str(currency), "metadata": metadata or {}}

    def _build_cache_key(self, method_label, canonical):
        meta_repr = repr(canonical["metadata"])
        return (method_label, canonical["cents"], canonical["currency"], meta_repr)

    def _map_to_signature(self, func, canonical):
        sig = inspect.signature(func)
        bound_args = {}
        for name, param in sig.parameters.items():
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue
            lname = name.lower()
            if lname in ("total_cents", "amount_cents", "cents", "amount"):
                bound_args[name] = canonical["cents"]
            elif lname in ("currency_code", "currency"):
                bound_args[name] = canonical["currency"]
            elif lname in ("meta", "metadata"):
                bound_args[name] = canonical["metadata"]
            else:
                if param.default is param.empty:
                    raise TypeError(f"Cannot map required parameter '{name}' for {func}")
        return bound_args

    def process_payment(self, amount: float, currency: str, metadata: dict = None):
        canonical = self._normalize_canonical(amount, currency, metadata)
        mapper = self._mapping.get("process_payment")
        method_label = None
        transformer = None

        if isinstance(mapper, tuple):
            method_label, transformer = mapper
        elif isinstance(mapper, str):
            method_label = mapper
        elif callable(mapper):
            method_label = getattr(mapper, "__name__", "callable_mapper")
        else:
            raise RuntimeError("Invalid mapper configuration")

        if self._cache is not None:
            key = self._build_cache_key(method_label, canonical)
            with self._lock:
                if key in self._cache:
                    return self._cache[key]

        if isinstance(mapper, (str, tuple)):
            method_name = method_label
            target = getattr(self._service, method_name)
            call_kwargs = self._map_to_signature(target, canonical)
            result = target(**call_kwargs)
        else:
            func = mapper
            sig = inspect.signature(func)
            params = list(sig.parameters.values())
            if params and params[0].name in ("service", "svc", "gateway"):
                call_kwargs = self._map_to_signature(func, canonical) if len(params) > 1 else {}
                result = func(self._service, **call_kwargs)
            else:
                call_kwargs = self._map_to_signature(func, canonical)
                result = func(**call_kwargs)

        if transformer:
            result = transformer(result)

        if self._cache is not None:
            with self._lock:
                self._cache[key] = result
        return result

if __name__ == "__main__":
    rich = LegacyGatewayRich()
    simple = LegacyGatewaySimple()

    def simple_bridge(service, cents, **kwargs):
        ok = service.pay(cents)
        return {"status": "ok" if ok else "failed", "charged": cents if ok else 0}

    def rich_transform(res):
        return {"status": "ok", "charged": res["charged_cents"], "currency": res["currency"]}

    rich_wrapper = CompatibilityWrapper(rich, {"process_payment": ("charge", rich_transform)})
    simple_wrapper = CompatibilityWrapper(simple, {"process_payment": simple_bridge})

    print(rich_wrapper.process_payment(12.34, "USD", {"order": 1}))
    print(simple_wrapper.process_payment(5.0, "USD"))
    print(rich_wrapper.process_payment(12.34, "USD", {"order": 1}))  # cached