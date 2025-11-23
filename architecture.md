# Inventory Agent Architecture

This document describes the architecture of the ADK-based Inventory Agent.

## System Overview

The system consists of a single **Inventory Manager Agent** built with the Google ADK. It follows a **ReAct** (Reasoning + Acting) pattern to autonomously manage inventory levels.

## Architecture Diagram

```mermaid
graph LR
    User[👤 User/<br/>Simulation Script]
    Agent[🤖 Inventory<br/>Manager Agent]
    DB[(💾 Local<br/>Inventory DB)]
    API[🌐 Supplier API<br/>dummyjson.com]
    
    User -->|Request| Agent
    Agent -->|Check/Update| DB
    Agent -->|Search/Order| API
    Agent -->|Response| User
    
    style Agent fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style DB fill:#50C878,stroke:#2E7D4E,color:#fff
    style API fill:#F39C12,stroke:#D68910,color:#fff
    style User fill:#95A5A6,stroke:#7F8C8D,color:#fff
```

## Component Details

### Agent (ReAct Pattern)
- **Reasoning**: Analyzes inventory levels and determines actions
- **Acting**: Executes tools to check stock, search suppliers, place orders
- **Guard Rails**: Rejects off-topic requests with polite explanations

### Tools

#### 1. **Inventory Database** (Configurable Backend)
- **In-Memory Mode** (default): Fast, stateless, perfect for demos
- **MySQL Mode** (optional): Persistent storage, production-ready
- Backend abstraction allows switching via environment variable

#### 2. **Supplier API**
- External API (dummyjson.com) for product search and ordering
- HTTP-based integration with error handling

## Deployment Options

### Option 1: Docker Compose (Recommended)
```mermaid
graph TB
    DC[Docker Compose]
    DC --> AC[Agent Container<br/>Python 3.12 + ADK]
    DC --> MC[MySQL Container<br/>MySQL 8.0]
    AC -->|TCP 3306| MC
    MC --> Vol[(Volume<br/>mysql_data)]
    
    style DC fill:#2496ED,stroke:#1769AA,color:#fff
    style AC fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style MC fill:#00758F,stroke:#004E66,color:#fff
    style Vol fill:#95A5A6,stroke:#7F8C8D,color:#fff
```

**Benefits**: One command setup, consistent environment, easy cleanup

### Option 2: Local Development
- In-memory database (no setup)
- Or connect to external MySQL instance

### Option 3: Production Deployment
- Deploy agent container to cloud (Cloud Run, ECS, etc.)
- Connect to managed MySQL (Cloud SQL, RDS, etc.)



## Sequence Diagram

The following sequence diagram illustrates the flow of the "Check & Restock" simulation scenario.

```mermaid
sequenceDiagram
    participant User
    participant Agent as Inventory Agent
    participant LocalDB as Inventory Tool
    participant Supplier as Supplier API (dummyjson)

    User->>Agent: "Check stock for 'Laptop' and restock if low"
    
    loop ReAct Loop
        Agent->>Agent: Reason: Check local stock first
        Agent->>LocalDB: check_inventory("Laptop")
        LocalDB-->>Agent: "Quantity: 5"
        
        Agent->>Agent: Reason: Stock is 5 (Low). Need to order.
        Agent->>Supplier: search_supplier("Laptop")
        Supplier-->>Agent: "Laptop (ID: 123) - $999 - Stock: 50"
        
        Agent->>Agent: Reason: Found product. Order 15 units.
        Agent->>Supplier: place_supplier_order(123, 15)
        Supplier-->>Agent: "Order placed. Delivery in 2 days."
        
        Agent->>Agent: Reason: Update local records.
        Agent->>LocalDB: update_inventory("Laptop", 15)
        LocalDB-->>Agent: "Updated. New Quantity: 20"
    end
    
    Agent-->>User: "Stock was low (5). Ordered 15 units. New stock is 20."
```
