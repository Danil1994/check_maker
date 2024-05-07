from datetime import datetime

from typing import Dict

response_template = {
    "products": [
    ],
    "payment": {
        "type": "type_payment",
        "amount": "amount"
    },
    "total": 0,
    "rest": 0,
    "created_at": "datetime"
}


def calculate_product_total_price(item: Dict) -> float:
    total_price = item["price"] * item["quantity"]
    if total_price < 0:
        print(f"Invalid price{item['price']}, {item['quantity']}")
    return total_price


def calculate_total_price_for_product(dict_of_products: Dict) -> Dict:
    dict_with_total = {
        "name": dict_of_products["name"],
        "price": dict_of_products["price"],
        "quantity": dict_of_products["quantity"],
        "total": 0
    }
    product_sum = calculate_product_total_price(dict_of_products)
    dict_with_total["total"] = product_sum

    return dict_with_total


def calculate_total_price_for_check(products_list):
    total_sum = 0
    for products in products_list:
        total_sum += products["total"]
    if total_sum < 0:
        return {"Not enough money ": f"missing {total_sum}!"}
    return total_sum


def calculate_change(payment_amount: float, total_price: float) -> float:
    change = payment_amount - total_price
    if change < 0:
        print(f"Not enoght money missing {change}!")
    return change


def response_builder(products_list: list[dict], payment: dict):
    response = response_template
    response["payment"]["type"] = payment["type"]
    response["payment"]["amount"] = payment["amount"]
    for dict_el in products_list:
        prod_with_total = calculate_total_price_for_product(dict_el)
        response["products"].append(prod_with_total)
    total_price = calculate_total_price_for_check(response["products"])
    response["total"] = total_price
    response["rest"] = calculate_change(payment["amount"], total_price)
    current_time = datetime.now()
    response["datetime"] = current_time.strftime("%d.%m.%Y %H:%M")
    return response
