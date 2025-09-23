class DeliveryParcel:
    def __init__(self, tracking_number="ABC123"):
        self.tracking_number = tracking_number
        self.current_handler = PendingHandler(self)

    def ship(self):
        self.current_handler.ship()

    def deliver(self):
        self.current_handler.deliver()

    def get_status(self):
        return self.current_handler.get_status()

    def set_handler(self, handler):
        self.current_handler = handler

class PendingHandler:
    def __init__(self, parcel):
        self.parcel = parcel

    def ship(self):
        self.parcel.set_handler(ShippedHandler(self.parcel))
        print("Parcel has been shipped.")

    def deliver(self):
        print("Cannot deliver a pending parcel.")

    def get_status(self):
        return f"Pending - Tracking: {self.parcel.tracking_number}"

class ShippedHandler:
    def __init__(self, parcel):
        self.parcel = parcel

    def ship(self):
        print("Parcel is already shipped.")

    def deliver(self):
        self.parcel.set_handler(DeliveredHandler(self.parcel))
        print("Parcel has been delivered.")

    def get_status(self):
        return f"Shipped - Tracking: {self.parcel.tracking_number}"

class DeliveredHandler:
    def __init__(self, parcel):
        self.parcel = parcel

    def ship(self):
        print("Cannot ship a delivered parcel.")

    def deliver(self):
        print("Parcel is already delivered.")

    def get_status(self):
        return f"Delivered - Tracking: {self.parcel.tracking_number}"

if __name__ == "__main__":
    parcel = DeliveryParcel()
    print(parcel.get_status())
    parcel.ship()
    print(parcel.get_status())
    parcel.deliver()
    print(parcel.get_status())
    parcel.ship()