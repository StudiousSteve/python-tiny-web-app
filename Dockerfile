# Use the official python 3.13 image as base
FROM python:3.13-slim

# Set working dir in container
WORKDIR /python-tiny-web-app

# Install curl and other dependencies
RUN apt-get update && apt-get install -y curl

# Install poetry
RUN curl -sSL http://install.python-poetry.org | python3

# Add poetry to path
ENV PATH="/root/.local/bin:$PATH"

# Copy depenedency files
COPY pyproject.toml poetry.lock /python-tiny-web-app/

# Install depenedencies
RUN /root/.local/bin/poetry install

# Copy the application code
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI app
CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
