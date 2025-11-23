# Docker Quick Start Guide

## Prerequisites

- Docker Desktop installed
- `.env` file with your `GOOGLE_API_KEY`

## One-Command Setup

Start everything (MySQL + Agent):

```bash
docker-compose up
```

This will:
1. ✅ Start MySQL database
2. ✅ Initialize database schema and sample data
3. ✅ Run the inventory agent simulation

## Stop Everything

```bash
docker-compose down
```

## Reset Database

```bash
# Stop and remove volumes
docker-compose down -v

# Start fresh
docker-compose up
```

## Run Interactive Tests

```bash
# Start just MySQL
docker-compose up -d mysql

# Run tests locally (with MySQL backend)
USE_MYSQL=true MYSQL_HOST=localhost uv run python test_agent.py
```

## View Logs

```bash
# All services
docker-compose logs -f

# Just agent
docker-compose logs -f agent

# Just MySQL
docker-compose logs -f mysql
```

## Architecture

```
┌─────────────────┐
│  Docker Host    │
│                 │
│  ┌───────────┐  │
│  │  Agent    │  │ ← Python 3.12 + ADK
│  │ Container │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │  MySQL    │  │ ← MySQL 8.0
│  │ Container │  │
│  └───────────┘  │
│                 │
│  Volume:        │
│  mysql_data     │ ← Persistent storage
└─────────────────┘
```

## Benefits for Students

- ✅ No Python/MySQL installation needed
- ✅ Consistent environment across all machines
- ✅ One command to start everything
- ✅ Easy cleanup with `docker-compose down -v`
- ✅ Portable - works on Mac, Windows, Linux
