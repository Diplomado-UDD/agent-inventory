# ADK Inventory Agent

An intelligent inventory management agent built with Google's Agent Development Kit (ADK) using Python 3.12.

## Features

- **ReAct Pattern**: Reasoning + Acting for autonomous decision-making
- **Custom Tools**: Local inventory management (in-memory database)
- **External API**: Integration with dummyjson.com for supplier data
- **Q&A Capabilities**: Answers inventory-related questions
- **Guard Rails**: Politely rejects off-topic requests
- **Full ADK Implementation**: Uses Google's official Agent Development Kit

## Prerequisites

- Python 3.12+
- `uv` package manager
- Google AI API Key ([Get one here](https://aistudio.google.com/app/apikey))

## Setup

1. **Initialize the project with uv:**
```bash
uv init
uv add google-adk requests python-dotenv
```

2. **Set your API key in `.env` file:**
```bash
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

## Running the Simulation

Execute the main script:

```bash
uv run python -m inventory_system.main
```

## Testing the Agent

Test various scenarios including on-topic and off-topic requests:

```bash
uv run python test_agent.py
```

**Test Cases:**
- ✅ Stock queries: "What's the current stock of Smartphone?"
- ✅ Restock requests: "Check laptop stock and restock if needed"
- ✅ Inventory questions: "How many products do we have?"
- ❌ Off-topic (rejected): "What's the weather?" or "Tell me a joke"

## Agent Capabilities

The agent can:
- Check stock levels for specific products
- Automatically restock when inventory is low (< 10 units)
- Search supplier API for product availability and pricing
- Place orders with suppliers
- Update local inventory records
- Answer inventory-related questions
- **Reject off-topic requests** with polite explanations

## Architecture

See [architecture.md](architecture.md) for detailed diagrams and system design.

## Expected Behavior

The agent will:
1. Check stock for requested products
2. Detect low stock (threshold: 10 units)
3. Search dummyjson.com supplier API
4. Place orders to reach target levels (20 units)
5. Update local inventory
6. Answer questions about inventory management
7. Politely decline non-inventory requests

## Project Structure

```
agent-inventory/
├── inventory_system/
│   ├── agent.py       # ADK Agent definition with guard rails
│   ├── tools.py       # Inventory & Supplier tools
│   └── main.py        # Simulation runner
├── test_agent.py      # Test script with multiple scenarios
├── architecture.md    # Mermaid diagrams
└── README.md          # This file
```

## Example Output

```
🤖 Agent: Currently, there are 20 units of Smartphone in stock.

🤖 Agent: I'm an Inventory Manager agent. I can only help with 
inventory-related questions such as checking stock, ordering products, 
or providing inventory insights. How can I assist you with inventory management?
```

