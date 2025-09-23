class OrderStateMachine:
    def __init__(self):
        self.state = 'created'
    
    def process(self, event):
        if self.state == 'created':
            if event == 'pay':
                self.state = 'paid'
            elif event == 'cancel':
                self.state = 'canceled'
        elif self.state == 'paid':
            if event == 'ship':
                self.state = 'shipped'
        elif self.state == 'canceled':
            pass
        elif self.state == 'shipped':
            if event == 'deliver':
                self.state = 'delivered'
    
    def current_state(self):
        return self.state

class Order:
    def __init__(self, state_machine=None):
        self.state_machine = state_machine or OrderStateMachine()
    
    def process(self, event):
        self.state_machine.process(event)
    
    def current_state(self):
        return self.state_machine.current_state()

# Usage example
if __name__ == '__main__':
    order = Order()
    print(order.current_state()) # created
    order.process('pay')
    print(order.current_state()) # paid
    order.process('ship')
    print(order.current_state()) # shipped
    order.process('deliver')
    print(order.current_state()) # delivered