# Use Python 3.12 slim image
FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY inventory_system ./inventory_system
COPY .env .env

# Default command
CMD ["python", "-m", "inventory_system.main"]
