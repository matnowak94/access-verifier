# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy files
COPY app .

# Install Poetry and dependencies
RUN pip install poetry && poetry install --no-root

# Run application
ENTRYPOINT ["poetry", "run", "python", "python/main.py"]