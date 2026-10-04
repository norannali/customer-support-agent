# data.py

customers = {
    "C001": {
        "name": "Noran",
        "email": "noran@example.com",
        "orders": ["ORD101", "ORD102"]
    },
    "C002": {
        "name": "Ahmed",
        "email": "ahmed@example.com",
        "orders": ["ORD103"]
    }
}


orders = {
    "ORD101": {
        "customer_id": "C001",
        "product": "Laptop",
        "price": 20000,
        "status": "Shipped",
        "tracking_number": "TRK123",
        "delivery_date": "2026-10-05",
        "return_days": 30,
        "returned": False
    },

    "ORD102": {
        "customer_id": "C001",
        "product": "Headphones",
        "price": 1500,
        "status": "Delivered",
        "tracking_number": "TRK456",
        "delivery_date": "2026-09-20",
        "return_days": 30,
        "returned": False,
        "refund_status": "Processing",
        "refund_requested": True
    },

    "ORD103": {
        "customer_id": "C002",
        "product": "Keyboard",
        "price": 1000,
        "status": "Delivered",
        "tracking_number": "TRK789",
        "delivery_date": "2026-09-15",
        "returned": False
    }
}