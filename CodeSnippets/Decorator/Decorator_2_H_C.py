from abc import ABC, abstractmethod
from typing import Callable, Any

class TextProcessor(ABC):
    @abstractmethod
    def process(self, text: str) -> str:
        pass

class BasicTextProcessor(TextProcessor):
    def process(self, text: str) -> str:
        return text

class TextEnhancer(TextProcessor):
    def __init__(self, processor: TextProcessor):
        self._processor = processor
    
    def process(self, text: str) -> str:
        return self._processor.process(text)

class UppercaseEnhancer(TextEnhancer):
    def process(self, text: str) -> str:
        result = super().process(text)
        return result.upper()

class BoldEnhancer(TextEnhancer):
    def process(self, text: str) -> str:
        result = super().process(text)
        return f"**{result}**"

class PrefixEnhancer(TextEnhancer):
    def __init__(self, processor: TextProcessor, prefix: str):
        super().__init__(processor)
        self._prefix = prefix
    
    def process(self, text: str) -> str:
        result = super().process(text)
        return f"{self._prefix}{result}"

class ConditionalEnhancer(TextEnhancer):
    def __init__(self, processor: TextProcessor, condition: Callable[[str], bool], 
                 enhancer_func: Callable[[str], str]):
        super().__init__(processor)
        self._condition = condition
        self._enhancer_func = enhancer_func
    
    def process(self, text: str) -> str:
        result = super().process(text)
        if self._condition(result):
            return self._enhancer_func(result)
        return result

class DynamicEnhancer(TextEnhancer):
    def __init__(self, processor: TextProcessor):
        super().__init__(processor)
        self._operations = []
    
    def add_operation(self, operation: Callable[[str], str]) -> 'DynamicEnhancer':
        self._operations.append(operation)
        return self
    
    def process(self, text: str) -> str:
        result = super().process(text)
        for operation in self._operations:
            result = operation(result)
        return result

class SmartEnhancer(TextEnhancer):
    def __init__(self, processor: TextProcessor):
        super().__init__(processor)
        self._enhancement_rules = {}
    
    def add_rule(self, keyword: str, enhancement: Callable[[str], str]) -> 'SmartEnhancer':
        self._enhancement_rules[keyword.lower()] = enhancement
        return self
    
    def process(self, text: str) -> str:
        result = super().process(text)
        for keyword, enhancement in self._enhancement_rules.items():
            if keyword in result.lower():
                result = enhancement(result)
                break
        return result

if __name__ == "__main__":
    basic = BasicTextProcessor()
    print(f"Basic: '{basic.process('hello world')}'")
    
    enhanced = UppercaseEnhancer(BoldEnhancer(PrefixEnhancer(basic, ">>> ")))
    print(f"Multi-enhanced: '{enhanced.process('hello world')}'")
    
    conditional = ConditionalEnhancer(
        basic, 
        lambda x: len(x) > 10,
        lambda x: f"[LONG TEXT: {x}]"
    )
    print(f"Conditional short: '{conditional.process('short')}'")
    print(f"Conditional long: '{conditional.process('this is a very long text')}'")
    
    dynamic = DynamicEnhancer(basic)
    dynamic.add_operation(str.upper).add_operation(lambda x: f"<<<{x}>>>")
    print(f"Dynamic: '{dynamic.process('flexible')}'")
    
    smart = SmartEnhancer(basic)
    smart.add_rule("error", lambda x: f"🚨 {x} 🚨").add_rule("success", lambda x: f"✅ {x} ✅")
    print(f"Smart error: '{smart.process('An error occurred')}'")
    print(f"Smart success: '{smart.process('Operation success')}'")
    print(f"Smart neutral: '{smart.process('Just normal text')}'")