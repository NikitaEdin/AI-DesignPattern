from abc import ABC, abstractmethod
from functools import wraps
import time

class Component(ABC):
    @abstractmethod
    def process(self, data):
        pass
    
    @abstractmethod
    def get_cost(self):
        pass

class BaseDataProcessor(Component):
    def __init__(self, name="Basic Processor"):
        self.name = name
        self.base_cost = 10.0
    
    def process(self, data):
        return f"Processing: {data}"
    
    def get_cost(self):
        return self.base_cost

class Enhancement(Component):
    def __init__(self, component):
        self._component = component
        self._enhancement_cost = 0.0
    
    def process(self, data):
        return self._component.process(data)
    
    def get_cost(self):
        return self._component.get_cost() + self._enhancement_cost

class CompressionEnhancement(Enhancement):
    def __init__(self, component, compression_level=1):
        super().__init__(component)
        self.compression_level = max(1, min(compression_level, 10))
        self._enhancement_cost = self.compression_level * 5.0
    
    def process(self, data):
        base_result = self._component.process(data)
        compressed_size = len(data) // (self.compression_level + 1)
        return f"{base_result} -> Compressed to {compressed_size} bytes (level {self.compression_level})"

class EncryptionEnhancement(Enhancement):
    def __init__(self, component, algorithm="AES"):
        super().__init__(component)
        self.algorithm = algorithm
        self._enhancement_cost = 15.0 if algorithm == "AES" else 8.0
    
    def process(self, data):
        base_result = self._component.process(data)
        encrypted_hash = hash(data + self.algorithm) % 10000
        return f"{base_result} -> Encrypted with {self.algorithm} (hash: {encrypted_hash})"

class PerformanceEnhancement(Enhancement):
    def __init__(self, component, enable_caching=True):
        super().__init__(component)
        self.enable_caching = enable_caching
        self._enhancement_cost = 12.0
        self._cache = {} if enable_caching else None
    
    def process(self, data):
        if self.enable_caching and data in self._cache:
            return f"[CACHED] {self._cache[data]}"
        
        start_time = time.time()
        base_result = self._component.process(data)
        processing_time = round((time.time() - start_time) * 1000, 2)
        
        enhanced_result = f"{base_result} -> Optimized (took {processing_time}ms)"
        
        if self.enable_caching:
            self._cache[data] = enhanced_result
        
        return enhanced_result

if __name__ == "__main__":
    base_processor = BaseDataProcessor("Advanced Processor")
    print(f"Base: {base_processor.process('sample_data.txt')} | Cost: ${base_processor.get_cost()}")
    
    compressed = CompressionEnhancement(base_processor, compression_level=5)
    print(f"With compression: {compressed.process('sample_data.txt')} | Cost: ${compressed.get_cost()}")
    
    encrypted_compressed = EncryptionEnhancement(compressed, "AES")
    print(f"With encryption: {encrypted_compressed.process('sample_data.txt')} | Cost: ${encrypted_compressed.get_cost()}")
    
    fully_enhanced = PerformanceEnhancement(encrypted_compressed, enable_caching=True)
    print(f"Fully enhanced: {fully_enhanced.process('sample_data.txt')} | Cost: ${fully_enhanced.get_cost()}")
    
    print(f"Cached call: {fully_enhanced.process('sample_data.txt')}")
    
    alternative_build = PerformanceEnhancement(
        EncryptionEnhancement(
            CompressionEnhancement(BaseDataProcessor(), compression_level=3),
            "RSA"
        )
    )
    print(f"Alternative build: {alternative_build.process('test.dat')} | Cost: ${alternative_build.get_cost()}")