class NegativePriceError(Exception):

    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity
        super().__init__(f"Invalid price: {price}, quantity: {quantity}")


class InsufficientFundsError(Exception):

    def __init__(self, payment_amount, total_price):
        self.payment_amount = payment_amount
        self.total_price = total_price
        super().__init__(f"Not enough money: missing {total_price - payment_amount}!")
