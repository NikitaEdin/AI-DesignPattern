```python
    class State(object):
      def __init__(self, context):
        self.context = context
      
      def handle_event(self, event):
        pass
      
      def get_state(self):
        return None
  
    class Context(object):
      def __init__(self):
        self.state = None
      
      def change_state(self, state):
        self.state = state
      
      def handle_event(self, event):
        if self.state is not None:
          self.state.handle_event(event)
  
    class ConcreteStateA(State):
      def handle_event(self, event):
        print("Handling event A")
      
      def get_state(self):
        return "A"
  
    class ConcreteStateB(State):
      def handle_event(self, event):
        print("Handling event B")
      
      def get_state(self):
        return "B"
  
    if __name__ == "__main__":
      context = Context()
      state_a = ConcreteStateA(context)
      state_b = ConcreteStateB(context)
      
      context.change_state(state_a)
      context.handle_event("Event A")
      print(context.get_state())
  
      context.change_state(state_b)
      context.handle_event("Event B")
      print(context.get_state())
  ```