def track_order(order_id: str) -> str:
    mock_orders = {
        "12345": "In transit — expected delivery in 2 days.",
        "67890": "Delivered on March 15th.",
    }
    get_order = mock_orders.get(order_id, "Order ID not found.")
    return get_order
