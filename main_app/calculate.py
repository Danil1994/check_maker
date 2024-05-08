from datetime import datetime

from main_app import schemas
from main_app.excaptions import NegativePriceError, InsufficientFundsError


def calculate_product_total_price(item: dict) -> float:
    total_price = item["price"] * item["quantity"]
    if total_price < 0:
        raise NegativePriceError(item['price'], item['quantity'])
    return total_price


def calculate_total_price_for_check(products_list: list) -> float:
    total_sum = 0
    for product in products_list:
        total_sum += product["total"]
    return total_sum


def calculate_change(payment_amount: float, total_price: float) -> float:
    change = payment_amount - total_price
    if change < 0:
        raise InsufficientFundsError(payment_amount, total_price)
    return change


def response_builder(request: schemas.SaleCheckCreate) -> dict:
    response = {"payment": request.payment, "products": request.products}
    for product in response["products"]:
        product["total"] = calculate_product_total_price(product)
    total_price = calculate_total_price_for_check(response["products"])
    response["total"] = total_price
    response["rest"] = calculate_change(response["payment"]["amount"], total_price)
    current_time = datetime.now()
    response["datetime"] = current_time.strftime("%d.%m.%Y %H:%M")
    return response
