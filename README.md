# ADK Inventory Agent

An intelligent inventory management agent built with Google's Agent Development Kit (ADK) using Python 3.12.

## Features

- **ReAct Pattern**: Reasoning + Acting for autonomous decision-making
- **Custom Tools**: Local inventory management with in-memory or MySQL backend
- **Product Listing**: Automatically shows available products at conversation start
- **MySQL Support**: Optional MySQL backend for persistent storage
- **Conversation Logging**: All interactions logged to MySQL for analysis
- **External API**: Integration with dummyjson.com for supplier data
- **Q&A Capabilities**: Answers inventory-related questions in multiple languages
- **Guard Rails**: Politely rejects off-topic requests
- **Evaluation Sets**: Pre-built test cases for systematic agent testing
- **Web Interface**: Full ADK web UI for interactive testing and debugging
- **Docker Support**: One-command deployment with Docker Compose
- **Full ADK Implementation**: Uses Google's official Agent Development Kit

## Prerequisites

- Python 3.12+ (or Docker - see below)
- `uv` package manager (or Docker)
- Google AI API Key ([Get one here](https://aistudio.google.com/app/apikey))

## Quick Start with Docker 🐳 (Recommended for Students)

**Easiest way - One command:**

```bash
# Add your API key to .env
echo "GOOGLE_API_KEY=your-key" > .env

# Start everything (MySQL + Agent)
docker-compose up
```

See [DOCKER.md](DOCKER.md) for details.

## Manual Setup

1. **Initialize the project with uv:**
```bash
uv init
uv add google-adk requests python-dotenv
```

2. **Set your API key in `.env` file:**
```bash
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

## Optional: MySQL Backend

By default, the agent uses in-memory storage. For persistent storage with MySQL:

1. **Start MySQL** (using Docker):
```bash
docker run --name mysql-inventory \
  -e MYSQL_ROOT_PASSWORD=inventory123 \
  -e MYSQL_DATABASE=inventory_db \
  -p 3306:3306 -d mysql:8.0
```

2. **Configure .env**:
```bash
USE_MYSQL=true
MYSQL_PASSWORD=inventory123
```

3. **Initialize database**:
```bash
uv run python -m inventory_system.init_db
```

See [MYSQL_SETUP.md](MYSQL_SETUP.md) for detailed instructions.

## Running the Simulation

Execute the main script:

```bash
uv run python -m inventory_system.main
```

## ADK Web Interface 🌐

### Launch the Interactive UI

**One simple command:**
```bash
uv run python -m google.adk.cli web
```

**Access:** http://127.0.0.1:8000

The web interface provides:
- ✅ Visual chat interface with your inventory agent
- ✅ Real-time tool execution visualization
- ✅ Session management and history
- ✅ Evaluation testing UI
- ✅ Automatic MySQL conversation logging (when enabled)

### Using the Interface

1. **Select Agent**: Choose `inventory_system` from dropdown
2. **Start Chatting**: Say "hello" to see product list automatically
3. **Ask Questions**: "How many laptops?" or "Check smartphone stock"
4. **Test Workflows**: "Check laptop stock and restock if needed"
5. **Run Evals**: Click "Eval" tab to run test cases

See [ADK_WEB_UI.md](ADK_WEB_UI.md) for more details.

## Evaluation Sets

Test your agent systematically with pre-built eval sets.

**Run evaluations:**
```bash
# Via command line
uv run python -m google.adk.cli eval inventory_system

# Or use the Eval tab in web UI
```

See [EVAL_GUIDE.md](EVAL_GUIDE.md) for creating custom eval sets.

## ADK Web Interface 🌐

**Visual interactive UI** for chatting with your agent.

**Setup** (one-time):
```bash
# Already cloned in adk-web/ directory
cd adk-web
npm install  # Already done
```

**Run** (two terminals):
```bash
# Terminal 1: API Server
uv run adk start -port 8000

# Terminal 2: Web UI  
cd adk-web && npm run serve --backend=http://localhost:8000
```

**Access:** http://localhost:4200

See [ADK_WEB_UI.md](ADK_WEB_UI.md) for details.

## Running the Agent

```bash
# Run simulation
uv run python -m inventory_system.main

# Run test suite
uv run python test_agent.py
```

## MySQL Conversation Persistence ✅

When `USE_MYSQL=true`, **all conversations are automatically logged** to the `conversations` table:
- User questions
- Agent reasoning
- Agent responses  
- Tools used

View conversation history:
```sql
-- See all conversations
SELECT * FROM conversations ORDER BY created_at DESC;

-- See conversations by session
SELECT user_message, agent_response, tools_used 
FROM conversations 
WHERE session_id = 'your-session-id'
ORDER BY created_at;
```

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
│   ├── database.py    # Backend abstraction (in-memory/MySQL)
│   ├── init_db.py     # MySQL database initialization
│   ├── tools.py       # Inventory & Supplier tools
│   └── main.py        # Simulation runner
├── test_agent.py      # Test script with multiple scenarios
├── Dockerfile         # Container image definition
├── docker-compose.yml # Multi-container orchestration
├── DOCKER.md          # Docker setup guide
├── MYSQL_SETUP.md     # MySQL configuration guide
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

