from abc import ABC, abstractmethod
from functools import wraps
import time

class Component(ABC):
    @abstractmethod
    def execute(self):
        pass

class BasicProcessor(Component):
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        return f"Processing: {self.data}"

class Enhancement(Component):
    def __init__(self, component):
        self._component = component
        self._active = True
    
    def execute(self):
        if not self._active:
            return self._component.execute()
        return self._enhance(self._component.execute())
    
    def _enhance(self, result):
        return result
    
    def toggle(self):
        self._active = not self._active
        return self
    
    def __getattr__(self, name):
        return getattr(self._component, name)

class SecurityWrapper(Enhancement):
    def __init__(self, component, security_level=1):
        super().__init__(component)
        self.security_level = security_level
    
    def _enhance(self, result):
        if self.security_level >= 2:
            result = f"[ENCRYPTED] {result} [/ENCRYPTED]"
        return f"[SECURED] {result} [/SECURED]"

class PerformanceMonitor(Enhancement):
    def __init__(self, component, threshold=0.1):
        super().__init__(component)
        self.threshold = threshold
        self.execution_times = []
    
    def _enhance(self, result):
        start_time = time.time()
        time.sleep(0.05)
        execution_time = time.time() - start_time
        self.execution_times.append(execution_time)
        
        status = "SLOW" if execution_time > self.threshold else "FAST"
        return f"[{status}: {execution_time:.3f}s] {result}"
    
    def get_average_time(self):
        return sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0

class LoggingEnhancement(Enhancement):
    def __init__(self, component, log_level="INFO"):
        super().__init__(component)
        self.log_level = log_level
        self.logs = []
    
    def _enhance(self, result):
        log_entry = f"[{self.log_level}] Executed at {time.strftime('%H:%M:%S')}"
        self.logs.append(log_entry)
        return f"{log_entry} | {result}"

class ChainableEnhancer:
    def __init__(self, component):
        self.component = component
    
    def add_security(self, level=1):
        self.component = SecurityWrapper(self.component, level)
        return self
    
    def add_monitoring(self, threshold=0.1):
        self.component = PerformanceMonitor(self.component, threshold)
        return self
    
    def add_logging(self, level="INFO"):
        self.component = LoggingEnhancement(self.component, level)
        return self
    
    def build(self):
        return self.component

if __name__ == "__main__":
    processor = BasicProcessor("user_data.json")
    
    enhanced = (ChainableEnhancer(processor)
                .add_logging("DEBUG")
                .add_monitoring(threshold=0.03)
                .add_security(level=2)
                .build())
    
    print("Enhanced execution:")
    result = enhanced.execute()
    print(result)
    
    print(f"\nAverage execution time: {enhanced.get_average_time():.3f}s")
    
    print("\nToggling security...")
    enhanced.toggle()
    print(enhanced.execute())
    
    print("\nDirect component access:")
    print(f"Original data: {enhanced.data}")