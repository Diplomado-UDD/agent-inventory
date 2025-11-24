# ADK Web Interface - Quick Start ✅

## Start the Web Interface

**One simple command:**
```bash
uv run python -m google.adk.cli web
```

**Access:** http://127.0.0.1:8000

That's it! The command automatically:
- Discovers your agents in `inventory_system/`
- Starts FastAPI server with embedded web UI
- Enables session management
- Provides evaluation testing interface
- Logs all conversations to MySQL (when `USE_MYSQL=true`)

## What You Get

✅ **Visual Chat Interface** - Interactive conversations with the inventory agent  
✅ **Tool Execution Visualization** - See tool calls in real-time  
✅ **Session Management** - Multiple conversations, saved history  
✅ **Evaluation Testing** - Run test cases and view results  
✅ **Trace Viewer** - Debug agent reasoning and decisions  
✅ **Automatic MySQL Logging** - All conversations persisted (when enabled)

## Using the Interface

### 1. Select Your Agent
At the top-left, select `inventory_system` from the dropdown

### 2. Start a Conversation
- Say "hello" or "hola" - the agent will automatically show available products
- Ask "How many laptops?" - agent checks inventory
- Request "Check laptop stock and restock if needed" - full workflow

### 3. View Tool Calls
Click the **Trace** tab to see:
- Agent reasoning
- Tool calls made
- Tool responses
- Final answer

### 4. Run Evaluations
Click **Eval** tab to:
- View existing eval sets
- Run systematic tests
- See pass/fail results
- Compare performance

## MySQL Conversation Logging

When `USE_MYSQL=true` in `.env`, every interaction is automatically logged to the `conversations` table:
- User messages
- Agent reasoning
- Tool calls
- Responses
- Timestamps
- Session IDs

Query your data:
```sql
SELECT user_message, agent_response, tools_used, created_at
FROM conversations 
ORDER BY created_at DESC 
LIMIT 10;
```

## Stopping the Server

Press `Ctrl+C` in the terminal where the web server is running.

## Troubleshooting

**"No root_agent found"**
- Make sure `inventory_system/agent.py` exports `root_agent` at module level
- Restart the server after code changes

**"Connection refused"**
- Check that port 8000 is not already in use
- Verify firewall settings

**Agent not responding**
- Check server logs for errors
- Verify `GOOGLE_API_KEY` is set in `.env`
- Ensure all dependencies are installed: `uv sync`

