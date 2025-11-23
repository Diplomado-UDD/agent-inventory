import requests
from typing import Dict, Optional

class InventoryDB:
    def __init__(self):
        self._db: Dict[str, int] = {
            "Laptop": 5,
            "Smartphone": 20,
            "Headphones": 50
        }

    def check_stock(self, product_name: str) -> str:
        """Checks the current stock level of a product.

        Args:
            product_name: The name of the product to check.

        Returns:
            A string describing the stock level.
        """
        quantity = self._db.get(product_name, 0)
        return f"Product: {product_name}, Quantity: {quantity}"

    def update_stock(self, product_name: str, quantity_change: int) -> str:
        """Updates the stock level of a product.

        Args:
            product_name: The name of the product.
            quantity_change: The amount to change the stock by (positive to add, negative to remove).

        Returns:
            A confirmation message.
        """
        current = self._db.get(product_name, 0)
        new_quantity = current + quantity_change
        if new_quantity < 0:
            return f"Error: Cannot reduce stock below 0. Current: {current}"
        
        self._db[product_name] = new_quantity
        return f"Updated {product_name}. Old: {current}, New: {new_quantity}"

# Instantiate the DB to be used by the tool
_inventory_db = InventoryDB()

def check_inventory(product_name: str) -> str:
    """Checks the local inventory for a product's stock level.

    Args:
        product_name: The name of the product to check.
    """
    return _inventory_db.check_stock(product_name)

def update_inventory(product_name: str, quantity: int) -> str:
    """Updates the local inventory stock.

    Args:
        product_name: The name of the product.
        quantity: The amount to add (positive) or remove (negative).
    """
    return _inventory_db.update_stock(product_name, quantity)

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
