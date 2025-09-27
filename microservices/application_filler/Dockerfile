# Use Python 3.10 slim image as the base image
# This provides a lightweight foundation with Python installed
FROM python:3.10-slim

# Install curl for health checks
# curl is used to perform HTTP requests to verify service health
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
# All subsequent commands will be executed relative to this directory
WORKDIR /app

# Copy the requirements file to the container
# This lists all Python dependencies needed for the application
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# --no-cache-dir prevents pip from caching packages, reducing image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application file to the container
# This contains the FastAPI application code
COPY main.py .

# Expose port 8109 to allow external access to the application
# This is the port the service will listen on
EXPOSE 8109

# Define the command to run the application when the container starts
# Uses uvicorn to serve the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8109"]