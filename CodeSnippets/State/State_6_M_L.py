python
class Order:
    def __init__(self, status):
        self.status = status

    def change_status(self, new_status):
        if self.status == "PENDING":
            if new_status == "APPROVED":
                self.status = new_status
            elif new_status == "REJECTED":
                self.status = new_status
        elif self.status == "APPROVED":
            if new_status == "SHIPPING":
                self.status = new_status
            elif new_status == "DELIVERED":
                self.status = new_status
        elif self.status == "REJECTED":
            if new_status == "CANCELLED":
                self.status = new_status

class State:
    def __init__(self, name):
        self.name = name

    def transition(self, order):
        if self.name == "PENDING":
            if order.status == "APPROVED":
                return ShippingState()
            elif order.status == "REJECTED":
                return CancelledState()
        elif self.name == "APPROVED":
            if order.status == "SHIPPING":
                return ShippingState()
            elif order.status == "DELIVERED":
                return DeliveredState()
        elif self.name == "REJECTED":
            if order.status == "CANCELLED":
                return CancelledState()

class PendingState(State):
    def transition(self, order):
        if order.status == "APPROVED":
            return ApprovedState()
        elif order.status == "REJECTED":
            return RejectedState()

class ApprovedState(State):
    def transition(self, order):
        if order.status == "SHIPPING":
            return ShippingState()
        elif order.status == "DELIVERED":
            return DeliveredState()

class RejectedState(State):
    def transition(self, order):
        if order.status == "CANCELLED":
            return CancelledState()

class ShippingState(State):
    def transition(self, order):
        if order.status == "DELIVERED":
            return DeliveredState()

class DeliveredState(State):
    def transition(self, order):
        if order.status == "CANCELLED":
            return CancelledState()

class CancelledState(State):
    def transition(self, order):
        pass

if __name__ == "__main__":
    order = Order("PENDING")
    state = PendingState("PENDING")
    while True:
        next_state = state.transition(order)
        if next_state is None:
            break
        else:
            state = next_state
            print("Order status changed to " + order.status)