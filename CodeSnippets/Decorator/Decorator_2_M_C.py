class TextMessage:
    def __init__(self, content):
        self.content = content
    
    def get_content(self):
        return self.content
    
    def get_cost(self):
        return 1.0

class MessageWrapper:
    def __init__(self, message):
        if not hasattr(message, 'get_content') or not hasattr(message, 'get_cost'):
            raise ValueError("Invalid message object")
        self._message = message
    
    def get_content(self):
        return self._message.get_content()
    
    def get_cost(self):
        return self._message.get_cost()

class EncryptionWrapper(MessageWrapper):
    def get_content(self):
        return f"[ENCRYPTED]{super().get_content()}[/ENCRYPTED]"
    
    def get_cost(self):
        return super().get_cost() + 2.0

class CompressionWrapper(MessageWrapper):
    def get_content(self):
        return f"[COMPRESSED]{super().get_content()}[/COMPRESSED]"
    
    def get_cost(self):
        return super().get_cost() + 1.5

class SignatureWrapper(MessageWrapper):
    def get_content(self):
        return f"{super().get_content()}\n--Digital Signature--"
    
    def get_cost(self):
        return super().get_cost() + 0.5

if __name__ == "__main__":
    basic_message = TextMessage("Hello World!")
    
    encrypted_message = EncryptionWrapper(basic_message)
    compressed_encrypted = CompressionWrapper(encrypted_message)
    final_message = SignatureWrapper(compressed_encrypted)
    
    print(f"Content: {final_message.get_content()}")
    print(f"Total Cost: ${final_message.get_cost():.1f}")