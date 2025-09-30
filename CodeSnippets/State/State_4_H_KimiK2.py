import threading
import time
from typing import Dict, List, Callable, Any

class WorkflowContext:
    __slots__ = ['_lock', '_journal', '_cfg', '_mode']
    def __init__(self, cfg: Dict[str, Any]):
        self._lock = threading.RLock()
        self._journal: List[str] = []
        self._cfg = cfg
        self._mode = InitMode(self)
    def record(self, entry: str):
        with self._lock:
            self._journal.append(entry)
    def backtrack(self) -> bool:
        with self._lock:
            if len(self._journal) < 2:
                return False
            self._journal.pop()
            last_mode = self._journal.pop()
            self._mode = ReplayingMode(self, last_mode)
            return True
    def mode(self):
        return self._mode
    def shift(self, new_mode):
        with self._lock:
            self._mode.exit_hook()
            self._mode = new_mode
            self._mode.enter_hook()

class InitMode:
    def __init__(self, ctx: WorkflowContext):
        self._ctx = ctx
    def enter_hook(self):
        self._ctx.record("init")
    def exit_hook(self):
        pass
    def proceed(self):
        max_ops = self._ctx._cfg.get("max_ops", 10)
        self._ctx.shift(OperatingMode(self._ctx, max_ops))

class OperatingMode:
    def __init__(self, ctx: WorkflowContext, remaining: int):
        self._ctx = ctx
        self._remaining = remaining
    def enter_hook(self):
        self._ctx.record("operating")
    def exit_hook(self):
        pass
    def work(self):
        if self._remaining <= 0:
            self._ctx.shift(ShutdownMode(self._ctx))
        else:
            self._remaining -= 1
            self._ctx.record(f"work-{self._remaining}")
            if self._remaining % 3 == 0:
                self._ctx.shift(PauseMode(self._ctx, self))

class PauseMode:
    def __init__(self, ctx: WorkflowContext, prev):
        self._ctx = ctx
        self._prev = prev
    def enter_hook(self):
        self._ctx.record("paused")
    def exit_hook(self):
        pass
    def resume(self):
        self._ctx.shift(self._prev)

class ShutdownMode:
    def __init__(self, ctx: WorkflowContext):
        self._ctx = ctx
    def enter_hook(self):
        self._ctx.record("shutdown")
    def exit_hook(self):
        pass

class ReplayingMode:
    def __init__(self, ctx: WorkflowContext, last_entry: str):
        self._ctx = ctx
        self._last = last_entry
    def enter_hook(self):
        self._ctx.record("replay")
    def exit_hook(self):
        pass
    def fix(self):
        if self._last.startswith("work-"):
            self._ctx.shift(OperatingMode(self._ctx, 0))
        else:
            self._ctx.shift(InitMode(self._ctx))

def run_async(ctx: WorkflowContext, cycles: int):
    def runner():
        for _ in range(cycles):
            mode = ctx.mode()
            if isinstance(mode, InitMode):
                mode.proceed()
            elif isinstance(mode, OperatingMode):
                mode.work()
            elif isinstance(mode, PauseMode):
                mode.resume()
            elif isinstance(mode, ReplayingMode):
                mode.fix()
            time.sleep(0.01)
    t = threading.Thread(target=runner, daemon=True)
    t.start()
    return t

if __name__ == "__main__":
    cfg = {"max_ops": 7}
    ctx = WorkflowContext(cfg)
    t1 = run_async(ctx, 20)
    t2 = run_async(ctx, 5)
    t1.join(); t2.join()
    for e in ctx._journal:
        print(e)
    if ctx.backtrack():
        print("->backtracked")
        run_async(ctx, 4).join()
        for e in ctx._journal:
            print(e)