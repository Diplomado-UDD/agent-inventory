# MySQL Setup for Inventory Agent

This guide shows how to set up MySQL as the backend for the inventory agent.

## Option 1: Using Docker (Recommended)

```bash
# Start MySQL container
docker run --name mysql-inventory \
  -e MYSQL_ROOT_PASSWORD=inventory123 \
  -e MYSQL_DATABASE=inventory_db \
  -p 3306:3306 \
  -d mysql:8.0

# Wait a few seconds for MySQL to start
sleep 10
```

## Option 2: Local MySQL Installation

Install MySQL 8.0+ on your system and ensure it's running.

## Configuration

1. **Update `.env` file:**
```bash
# Enable MySQL backend
USE_MYSQL=true

# MySQL connection details
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=inventory123
MYSQL_DATABASE=inventory_db
MYSQL_PORT=3306
```

2. **Initialize the database:**
```bash
uv run python -m inventory_system.init_db
```

This will:
- Create the `inventory_db` database
- Create the `products` table
- Populate with sample data (Laptop, Smartphone, Headphones, etc.)

## Verification

```bash
# Run the agent
uv run python -m inventory_system.main
```

You should see: `📊 Using MySQL backend`

## Switching Back to In-Memory

Simply set in `.env`:
```bash
USE_MYSQL=false
```

## Database Schema

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL UNIQUE,
    quantity INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_product_name (product_name)
);
```

## Stopping MySQL Container

```bash
docker stop mysql-inventory
docker rm mysql-inventory
```
