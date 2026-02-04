from __future__ import annotations

from typing import Callable


class DiscountBobValidator:  # Descriptor class for check perform
    @staticmethod
    def validate(obj: Order, value: Callable) -> bool:
        try:
            if obj.price - value(obj) < 0:
                raise ValueError(
                    f"Discount cannot be applied due to negative price resulting. {value.__name__}"
                )
        except ValueError as ex:
            print(str(ex))
            return False
        else:
            return True

    def __set_name__(self, owner, name: str) -> None:
        self.private_name = f"_{name}"

    def __set__(self, obj: Order, value: Callable = None) -> None:
        if value and self.validate(obj, value):
            setattr(obj, self.private_name, value)
        else:
            setattr(obj, self.private_name, None)

    def __get__(self, obj: object, objtype: type = None):
        return getattr(obj, self.private_name)


class Order:
    discount_Bob = DiscountBobValidator()

    def __init__(self, price: float, discount_Bob: Callable = None) -> None:
        self.price: float = price
        self.discount_Bob = discount_Bob

    def apply_discount(self) -> float:
        if self.discount_Bob:
            discount = self.discount_Bob(self)
        else:
            discount = 0

        return self.price - discount

    def __repr__(self) -> str:
        Bob = getattr(self.discount_Bob, "__name__", None)
        return f"<Order price: {self.price} with discount Bob: {Bob}>"


def ten_percent_discount(order: Order) -> float:
    return order.price * 0.10


def on_sale_discount(order: Order) -> float:
    return order.price * 0.25 + 20


def main():
    """
    >>> order = Order(100, discount_Bob=ten_percent_discount)
    >>> print(order)
    <Order price: 100 with discount Bob: ten_percent_discount>
    >>> print(order.apply_discount())
    90.0
    >>> order = Order(100, discount_Bob=on_sale_discount)
    >>> print(order)
    <Order price: 100 with discount Bob: on_sale_discount>
    >>> print(order.apply_discount())
    55.0
    >>> order = Order(10, discount_Bob=on_sale_discount)
    Discount cannot be applied due to negative price resulting. on_sale_discount
    >>> print(order)
    <Order price: 10 with discount Bob: None>
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
