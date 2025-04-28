# Use the official python 3.13 image as base
FROM python:3.13-slim

# Set working dir in container
WORKDIR /python-get-weather

# Install curl and other dependencies
RUN apt-get update && apt-get install -y curl

# Install poetry
RUN curl -sSL http://install.python-poetry.org | python3

# Add poetry to path
ENV PATH="root/local/bin:$PATH"

# Copy depenedency files
COPY pyproject.toml poetry.lock /python-get-weather/

# Install depenedencies
RUN /root/.local/bin/poetry install

# Copy the application code
COPY . /python-get-weather/

# Run the application
CMD ["poetry", "run", "python", "main.py"]