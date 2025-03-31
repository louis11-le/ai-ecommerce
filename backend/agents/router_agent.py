from agents.faq_agent import get_faq_agent
from agents.order_agent import handle_order_query
from transformers import pipeline

# Initialize the FAQ chain
faq_chain = get_faq_agent()

# Load a pre-trained zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define intents and their descriptions
INTENTS = {
    "order_placement": "Questions about how to place an order or buy a product.",
    "order_management": "Questions about tracking, canceling, or checking the status of an order.",
}


def classify_intent(query: str):
    """
    Classify the intent of the query using zero-shot classification.

    Args:
        query (str): The user's input query.

    Returns:
        str: The classified intent (e.g., "order_placement" or "order_management").
    """
    labels = list(INTENTS.keys())
    result = classifier(query, labels)
    return result["labels"][0]  # Return the top intent


def route_query(query: str):
    """
    Routes the user query to the appropriate agent based on the classified intent.

    Args:
        query (str): The user's input query.

    Returns:
        str: The response from the appropriate agent.
    """

    # Classify the intent of the query
    intent = classify_intent(query)
    if intent == "order_management":
        return handle_order_query(query)
    elif intent == "order_placement":
        response = faq_chain({"query": query})
        return response["result"]
    else:
        return "I'm sorry, I couldn't understand your query."
