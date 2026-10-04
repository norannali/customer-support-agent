from schemas import CustomerSupportResponse


response = {
    "intent": "refund_inquiry",
    "message": "Yes. Order ORD103 is eligible for a refund of 1000 EGP.",
    "orders": [
        {
            "order_id": "ORD103",
            "product": "Keyboard",
            "status": "Delivered",
            "tracking_number": "TRK789",
            "delivery_date": "2026-09-15",
            "refund_eligible": True,
            "refund_amount": 1000,
            "refund_reason": None
        }
    ]
}


result = CustomerSupportResponse.model_validate(response)

print("Structured validation PASSED!")
print(result)