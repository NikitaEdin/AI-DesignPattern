from abc import ABC, abstractmethod
import uuid

class OrderManager:
    def __init__(self, order_id=None):
        self._order_id = order_id or str(uuid.uuid4())
        self._handler = PendingHandler(self)
        self._history = []

    def set_handler(self, handler):
        if handler != self._handler:
            self._handler = handler
            self._history.append(type(handler).__name__)

    def start_processing(self):
        try:
            self._handler.start_processing()
        except ValueError as e:
            print(f"Error: {e}")

    def dispatch(self):
        try:
            self._handler.dispatch()
        except ValueError as e:
            print(f"Error: {e}")

    def complete_delivery(self):
        try:
            self._handler.complete_delivery()
        except ValueError as e:
            print(f"Error: {e}")

    def cancel(self):
        try:
            self._handler.cancel()
        except ValueError as e:
            print(f"Error: {e}")

    def get_history(self):
        return self._history

class WorkflowHandler(ABC):
    def __init__(self, manager):
        self._manager = manager

    @abstractmethod
    def start_processing(self):
        pass

    @abstractmethod
    def dispatch(self):
        pass

    @abstractmethod
    def complete_delivery(self):
        pass

    @abstractmethod
    def cancel(self):
        pass

class PendingHandler(WorkflowHandler):
    def start_processing(self):
        print(f"Order {self._manager._order_id}: Initiating processing.")
        self._manager.set_handler(ProcessingHandler(self._manager))

    def dispatch(self):
        raise ValueError("Cannot dispatch a pending order.")

    def complete_delivery(self):
        raise ValueError("Cannot complete delivery for a pending order.")

    def cancel(self):
        print(f"Order {self._manager._order_id}: Cancelled while pending.")
        self._manager.set_handler(CancelledHandler(self._manager))

class ProcessingHandler(WorkflowHandler):
    def start_processing(self):
        raise ValueError("Order is already being processed.")

    def dispatch(self):
        print(f"Order {self._manager._order_id}: Dispatching to delivery.")
        self._manager.set_handler(ShippedHandler(self._manager))

    def complete_delivery(self):
        raise ValueError("Cannot complete delivery while processing.")

    def cancel(self):
        print(f"Order {self._manager._order_id}: Cancelled during processing.")
        self._manager.set_handler(CancelledHandler(self._manager))

class ShippedHandler(WorkflowHandler):
    def start_processing(self):
        raise ValueError("Order is already shipped; processing complete.")

    def dispatch(self):
        raise ValueError("Order is already dispatched.")

    def complete_delivery(self):
        print(f"Order {self._manager._order_id}: Delivery completed.")
        self._manager.set_handler(DeliveredHandler(self._manager))

    def cancel(self):
        raise ValueError("Cannot cancel a shipped order.")

class DeliveredHandler(WorkflowHandler):
    def start_processing(self):
        raise ValueError("Order is already delivered.")

    def dispatch(self):
        raise ValueError("Order is already delivered.")

    def complete_delivery(self):
        raise ValueError("Delivery already completed.")

    def cancel(self):
        raise ValueError("Cannot cancel a delivered order.")

class CancelledHandler(WorkflowHandler):
    def start_processing(self):
        raise ValueError("Cancelled order cannot be processed.")

    def dispatch(self):
        raise ValueError("Cancelled order cannot be dispatched.")

    def complete_delivery(self):
        raise ValueError("Cancelled order cannot be delivered.")

    def cancel(self):
        print(f"Order {self._manager._order_id}: Already cancelled.")

if __name__ == "__main__":
    order1 = OrderManager("ORD-001")
    print("Processing order1:")
    order1.start_processing()
    order1.dispatch()
    order1.complete_delivery()
    print(f"History: {order1.get_history()}")

    print("\nEdge case - Cancel shipped order:")
    order2 = OrderManager("ORD-002")
    order2.start_processing()
    order2.dispatch()
    order2.cancel()  # Should raise error

    print("\nValid cancel from pending:")
    order3 = OrderManager("ORD-003")
    order3.cancel()
    print(f"History: {order3.get_history()}")