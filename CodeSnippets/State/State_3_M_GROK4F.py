from abc import ABC, abstractmethod

class OrderPhase(ABC):
    @abstractmethod
    def confirm(self, order):
        pass
    @abstractmethod
    def complete(self, order):
        pass
    @abstractmethod
    def get_description(self):
        pass

class PendingPhase(OrderPhase):
    def confirm(self, order):
        order.current_phase = ConfirmedPhase()
        print(f"Order {order.order_id} confirmed.")
    def complete(self, order):
        raise ValueError("Cannot complete pending order.")
    def get_description(self):
        return "Pending"

class ConfirmedPhase(OrderPhase):
    def confirm(self, order):
        raise ValueError("Order already confirmed.")
    def complete(self, order):
        order.current_phase = CompletedPhase()
        print(f"Order {order.order_id} completed.")
    def get_description(self):
        return "Confirmed"

class CompletedPhase(OrderPhase):
    def confirm(self, order):
        raise ValueError("Cannot confirm completed order.")
    def complete(self, order):
        raise ValueError("Order already completed.")
    def get_description(self):
        return "Completed"

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.current_phase = PendingPhase()

    def confirm(self):
        self.current_phase.confirm(self)

    def complete(self):
        self.current_phase.complete(self)

    def description(self):
        return self.current_phase.get_description()

if __name__ == "__main__":
    test_order = Order("ORD-001")
    print("Initial:", test_order.description())
    test_order.confirm()
    print("After confirm:", test_order.description())
    test_order.complete()
    print("After complete:", test_order.description())
    try:
        test_order.complete()
    except ValueError as e:
        print("Error:", e)