# tools.py

from langchain.tools import tool
from data import customers, orders
from datetime import date

# TOOL 1: Get Customer Information
@tool
def get_customer(customer_id: str) -> dict:
    """Get customer information using their customer ID."""

    customer = customers.get(customer_id)

    if not customer:
        return {"error": "Customer not found"}

    return customer


# TOOL 2: Get Order Information
@tool
def get_order(customer_id: str, order_id: str = "") -> dict:
    """
    Get order information.
    Use customer_id to verify ownership.
    If order_id is not provided, retrieve the customer's latest order.
    """

    customer = customers.get(customer_id)

    if not customer:
        return {"error": "Customer not found"}

    if not order_id:
        order_id = customer["orders"][-1]

    order = orders.get(order_id)

    if not order:
        return {"error": "Order not found"}

    if order["customer_id"] != customer_id:
        return {"error": "This order does not belong to this customer"}

    return {"order_id": order_id, **order}

#TOOL 2.1: Get All Orders for a Customer

@tool
def get_customer_orders(customer_id: str) -> list:
    """Get all orders belonging to a specific customer."""

    customer = customers.get(customer_id)

    if not customer:
        return [{"error": "Customer not found"}]

    result = []

    for order_id in customer["orders"]:

        order = orders.get(order_id)

        if order:
            result.append({
                "order_id": order_id,
                **order
            })

    return result

# TOOL 3: Search Refund Policy
@tool
def search_policy(topic: str) -> str:
    """Search the company refund policy for information about a topic."""

    with open("policies/refund_policy.txt", "r", encoding="utf-8") as file:
        policy = file.read()

    return policy


# TOOL 4: Calculate Refund
@tool
def calculate_refund(order_id: str, customer_id: str) -> dict:
    """Check refund eligibility or return the status of an existing refund."""

    order = orders.get(order_id)

    if not order:
        return {"error": "Order not found"}

    if order["customer_id"] != customer_id:
        return {"error": "Unauthorized order access"}

    order_context = {
        "order_id": order_id,
        "product": order["product"],
        "status": order["status"],
        "tracking_number": order.get("tracking_number"),
        "delivery_date": order.get("delivery_date")
    }

    # Existing refund request
    if order.get("refund_requested"):
        return {
            **order_context,
            "refund_requested": True,
            "refund_status": order.get("refund_status"),
            "refund_amount": order["price"],
            "currency": "EGP"
        }

    # New refund eligibility
    if order["status"] != "Delivered":
        return {
            **order_context,
            "eligible": False,
            "reason": "Order has not been delivered yet"
        }
    delivery_date = date.fromisoformat(order["delivery_date"])
    today = date.today()

    days_since_delivery = (today - delivery_date).days

    if days_since_delivery > 30:
        return {
            **order_context,
            "eligible": False,
            "reason": "The refund request is outside the 30-day refund window"
        }

    if order["returned"]:
        return {
            **order_context,
            "eligible": False,
            "reason": "This order has already been refunded"
        }

    return {
        **order_context,
        "eligible": True,
        "refund_amount": order["price"],
        "currency": "EGP"
    }
    
# TOOL 5: Check All Refunds for a Customer
@tool
def check_all_refunds(customer_id: str) -> list:
    """Check refund eligibility for all orders of a customer."""

    customer = customers.get(customer_id)

    if not customer:
        return [{"error": "Customer not found"}]

    results = []

    for order_id in customer["orders"]:

        result = calculate_refund.invoke({
            "order_id": order_id,
            "customer_id": customer_id
        })

        results.append(result)

    return results