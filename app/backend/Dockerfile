# Use an official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy the requirements file and install dependencies
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync

# Copy the rest of the application code
COPY . .

EXPOSE 8000

# Start the Python application
CMD ["fastapi", "run", "main:app"]
