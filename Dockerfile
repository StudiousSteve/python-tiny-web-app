# Use official Python image
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy only Poetry files first to optimize caching
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN pip install --no-cache-dir poetry && poetry install --no-root

# Ensure Poetry is available in the container's PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy remaining app files
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI app
CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
