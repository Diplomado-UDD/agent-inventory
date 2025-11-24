import requests
from typing import Dict, Optional
from .database import _inventory_backend

def list_products() -> str:
    """Lists all products available in the inventory with their current stock levels.
    
    Returns:
        A formatted string listing all products and quantities.
    """
    # Get list from backend
    if hasattr(_inventory_backend, '_db'):
        # In-memory backend
        products = _inventory_backend._db
    else:
        # MySQL backend - we'll need to add a method to get all products
        # For now, return the known products
        products = {"Laptop": 5, "Smartphone": 20, "Headphones": 50}
    
    result = "Available Products:\n"
    for product, qty in products.items():
        result += f"- {product}: {qty} units\n"
    return result

def check_inventory(product_name: str) -> str:
    """Checks the local inventory for a product's stock level.

    Args:
        product_name: The name of the product to check.
    """
    return _inventory_backend.check_stock(product_name)

def update_inventory(product_name: str, quantity: int) -> str:
    """Updates the local inventory stock.

    Args:
        product_name: The name of the product.
        quantity: The amount to add (positive) or remove (negative).
    """
    return _inventory_backend.update_stock(product_name, quantity)

def search_supplier(query: str) -> str:
    """Searches for products from an external supplier API to check availability and price.

    Args:
        query: The product name to search for.
    """
    try:
        response = requests.get(f"https://dummyjson.com/products/search?q={query}")
        response.raise_for_status()
        data = response.json()
        products = data.get('products', [])
        if not products:
            return f"No products found for '{query}' at supplier."
        
        # Return top 3 results
        result_str = "Supplier Results:\n"
        for p in products[:3]:
            result_str += f"- {p['title']} (ID: {p['id']}): ${p['price']} - Stock: {p['stock']}\n"
        return result_str
    except Exception as e:
        return f"Error contacting supplier: {e}"

def place_supplier_order(product_id: int, quantity: int) -> str:
    """Places an order with the supplier.

    Args:
        product_id: The ID of the product to order (found via search_supplier).
        quantity: The quantity to order.
    """
    # In a real app, this would POST to an API. Here we mock it.
    return f"Order placed successfully for Product ID {product_id}, Quantity: {quantity}. Estimated delivery: 2 days."
