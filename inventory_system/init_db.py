"""
Database initialization script for MySQL inventory.
Creates the database, table, and populates with sample data.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize MySQL database with inventory schema and sample data."""
    
    # Database configuration from environment
    config = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'port': int(os.getenv('MYSQL_PORT', 3306))
    }
    
    db_name = os.getenv('MYSQL_DATABASE', 'inventory_db')
    
    try:
        # Connect without database
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✓ Database '{db_name}' created/verified")
        
        # Use the database
        cursor.execute(f"USE {db_name}")
        
        # Create table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL UNIQUE,
            quantity INT NOT NULL DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_product_name (product_name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(create_table_query)
        print("✓ Table 'products' created/verified")
        
        # Insert sample data (ignore if already exists)
        sample_data = [
            ('Laptop', 5),
            ('Smartphone', 20),
            ('Headphones', 50),
            ('Monitor', 15),
            ('Keyboard', 30),
            ('Mouse', 40)
        ]
        
        insert_query = """
        INSERT INTO products (product_name, quantity) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE quantity=VALUES(quantity)
        """
        
        cursor.executemany(insert_query, sample_data)
        connection.commit()
        print(f"✓ Inserted {cursor.rowcount} product records")
        
        # Verify data
        cursor.execute("SELECT product_name, quantity FROM products")
        products = cursor.fetchall()
        print("\n📦 Current Inventory:")
        for name, qty in products:
            print(f"   {name}: {qty} units")
        
        print(f"\n✅ Database initialization complete!")
        
        # Initialize conversation logging tables
        from inventory_system.conversation_logger import conversation_logger
        conversation_logger.init_tables()
        
    except Error as e:
        print(f"❌ Error: {e}")
        return False
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

if __name__ == "__main__":
    init_database()
