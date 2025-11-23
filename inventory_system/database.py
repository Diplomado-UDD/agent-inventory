"""
Database backend for inventory management.
Supports both in-memory and MySQL storage.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

class InventoryBackend(ABC):
    """Abstract base class for inventory storage backends."""
    
    @abstractmethod
    def check_stock(self, product_name: str) -> str:
        """Check stock level for a product."""
        pass
    
    @abstractmethod
    def update_stock(self, product_name: str, quantity_change: int) -> str:
        """Update stock level for a product."""
        pass

class InMemoryInventory(InventoryBackend):
    """In-memory inventory storage (original implementation)."""
    
    def __init__(self):
        self._db = {
            "Laptop": 5,
            "Smartphone": 20,
            "Headphones": 50
        }
    
    def check_stock(self, product_name: str) -> str:
        quantity = self._db.get(product_name, 0)
        return f"Product: {product_name}, Quantity: {quantity}"
    
    def update_stock(self, product_name: str, quantity_change: int) -> str:
        current = self._db.get(product_name, 0)
        new_quantity = current + quantity_change
        if new_quantity < 0:
            return f"Error: Cannot reduce stock below 0. Current: {current}"
        
        self._db[product_name] = new_quantity
        return f"Updated {product_name}. Old: {current}, New: {new_quantity}"

class MySQLInventory(InventoryBackend):
    """MySQL-based inventory storage."""
    
    def __init__(self):
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', 'inventory_db'),
            'port': int(os.getenv('MYSQL_PORT', 3306))
        }
    
    def _get_connection(self):
        """Create database connection."""
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            raise ConnectionError(f"Failed to connect to MySQL: {e}")
    
    def check_stock(self, product_name: str) -> str:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "SELECT quantity FROM products WHERE product_name = %s"
            cursor.execute(query, (product_name,))
            result = cursor.fetchone()
            
            if result:
                quantity = result[0]
            else:
                quantity = 0
                # Auto-create product with 0 stock
                insert_query = "INSERT INTO products (product_name, quantity) VALUES (%s, 0)"
                cursor.execute(insert_query, (product_name,))
                conn.commit()
            
            cursor.close()
            conn.close()
            
            return f"Product: {product_name}, Quantity: {quantity}"
            
        except Error as e:
            return f"Database error: {e}"
    
    def update_stock(self, product_name: str, quantity_change: int) -> str:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get current quantity
            query = "SELECT quantity FROM products WHERE product_name = %s"
            cursor.execute(query, (product_name,))
            result = cursor.fetchone()
            
            if result:
                current = result[0]
            else:
                current = 0
                # Create product if doesn't exist
                insert_query = "INSERT INTO products (product_name, quantity) VALUES (%s, 0)"
                cursor.execute(insert_query, (product_name,))
            
            new_quantity = current + quantity_change
            if new_quantity < 0:
                cursor.close()
                conn.close()
                return f"Error: Cannot reduce stock below 0. Current: {current}"
            
            # Update quantity
            update_query = """
                INSERT INTO products (product_name, quantity) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE quantity = %s
            """
            cursor.execute(update_query, (product_name, new_quantity, new_quantity))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return f"Updated {product_name}. Old: {current}, New: {new_quantity}"
            
        except Error as e:
            return f"Database error: {e}"

# Choose backend based on environment variable
USE_MYSQL = os.getenv('USE_MYSQL', 'false').lower() == 'true'

if USE_MYSQL:
    print("📊 Using MySQL backend")
    _inventory_backend = MySQLInventory()
else:
    print("💾 Using in-memory backend")
    _inventory_backend = InMemoryInventory()
