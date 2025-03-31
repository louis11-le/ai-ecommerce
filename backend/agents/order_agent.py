import re

from tools.order_tool import track_order


def handle_order_query(query: str):
    # Use regex to extract the numeric order ID after '#'
    match = re.search(r"#(\d+)", query)
    if match:
        order_id = match.group(1)  # Extract only the numeric part
        return track_order(order_id)

    return "Please provide a valid order ID (e.g., #12345)."
