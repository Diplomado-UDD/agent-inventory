import os
from google.adk import Agent
from .tools import check_inventory, update_inventory, search_supplier, place_supplier_order

def create_inventory_agent(model_name: str = "gemini-2.0-flash-exp") -> Agent:
    """Creates and configures the Inventory Manager agent.

    Args:
        model_name: The name of the model to use.

    Returns:
        A configured ADK Agent instance.
    
    Note:
        Requires GOOGLE_API_KEY environment variable to be set.
    """
    
    # Verify API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError(
            "GOOGLE_API_KEY environment variable not set. "
            "Please set it in your .env file or environment."
        )
    
    instruction = """
    You are an expert Inventory Manager for a retail business. You manage stock levels, 
    supplier relationships, and provide inventory insights.
    
    **Your Capabilities:**
    - Check current stock levels for any product
    - Monitor and restock low inventory items
    - Search for products from suppliers
    - Place orders with suppliers
    - Update inventory records
    - Answer questions about inventory management, stock levels, and ordering processes
    - Provide inventory reports and statistics
    
    **Your Workflow for Restocking:**
    1. Check the stock of a requested product in the local inventory
    2. If stock is low (below 10 units), initiate restocking
    3. Search the supplier API for the product to get ID and pricing
    4. Place an order for sufficient quantity (target: 20 units)
    5. Update the local inventory to reflect the order
    
    **Important Boundaries:**
    You ONLY handle inventory management tasks. If a user asks about:
    - Topics unrelated to inventory (weather, sports, general chat, etc.)
    - Tasks outside inventory management (HR, finance, sales reports, etc.)
    
    Politely decline with: "I'm an Inventory Manager agent. I can only help with 
    inventory-related questions such as checking stock, ordering products, or 
    providing inventory insights. How can I assist you with inventory management?"
    
    Always be helpful, clear, and professional in your responses.
    """

    agent = Agent(
        model=model_name,
        name="inventory_manager",
        description="Manages inventory levels by checking stock and ordering from suppliers.",
        instruction=instruction,
        tools=[check_inventory, update_inventory, search_supplier, place_supplier_order]
    )
    
    return agent
